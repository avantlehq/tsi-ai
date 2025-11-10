"""
Pydantic models for TSI conversion API

These models define the request/response schemas for the conversion endpoints.
"""

from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum


class OutputFormat(str, Enum):
    """Supported output formats."""
    EDIFACT_SKDUPD = "edifact-skdupd"
    EDIFACT_TSDUPD = "edifact-tsdupd"
    GTFS_STATIC = "gtfs"
    GTFS_REALTIME = "gtfs-realtime"


class ValidationLevel(str, Enum):
    """Validation strictness levels."""
    STANDARD = "standard"
    STRICT = "strict"


class ConversionRequest(BaseModel):
    """Request model for data conversion."""
    input_data: Dict[str, Any] = Field(..., description="Transport data in JSON format")
    output_format: OutputFormat = Field(..., description="Desired output format")
    options: Dict[str, Any] = Field(default_factory=dict, description="Conversion options")
    tenant_id: Optional[str] = Field(None, description="Tenant identifier")


class ValidationRequest(BaseModel):
    """Request model for data validation."""
    input_data: Dict[str, Any] = Field(..., description="Transport data to validate")
    format: str = Field(..., description="Input data format")
    validation_level: ValidationLevel = Field(ValidationLevel.STANDARD, description="Validation strictness")
    tenant_id: Optional[str] = Field(None, description="Tenant identifier")


class ConversionResult(BaseModel):
    """Result of a conversion operation."""
    job_id: str = Field(..., description="Unique job identifier")
    input_format: str = Field(..., description="Input data format")
    output_format: str = Field(..., description="Output data format")
    status: str = Field(..., description="Conversion status")
    progress: int = Field(..., description="Completion percentage (0-100)")
    results: Dict[str, Any] = Field(..., description="Conversion statistics")
    output: Union[str, Dict[str, Any]] = Field(..., description="Converted data")
    download_url: Optional[str] = Field(None, description="Download URL for large files")
    metadata: Dict[str, Any] = Field(..., description="Processing metadata")


class ValidationError(BaseModel):
    """Validation error details."""
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    line: Optional[int] = Field(None, description="Line number where error occurred")
    field: Optional[str] = Field(None, description="Field name with error")
    severity: str = Field(..., description="Error severity level")


class ValidationSummary(BaseModel):
    """Summary of validation results."""
    total_records: int = Field(..., description="Total number of records processed")
    valid_records: int = Field(..., description="Number of valid records")
    errors: List[ValidationError] = Field(..., description="Validation errors")
    warnings: List[ValidationError] = Field(..., description="Validation warnings")
    notices: List[ValidationError] = Field(..., description="Validation notices")


class ValidationDetails(BaseModel):
    """Detailed validation results."""
    field_validation: Dict[str, Dict[str, Union[int, float]]] = Field(..., description="Field-level validation stats")
    data_integrity: Dict[str, Dict[str, Union[int, float]]] = Field(..., description="Data integrity checks")


class ValidationResult(BaseModel):
    """Result of a validation operation."""
    job_id: str = Field(..., description="Unique job identifier")
    format: str = Field(..., description="Input data format")
    validation_level: str = Field(..., description="Validation strictness level")
    status: str = Field(..., description="Validation status")
    is_valid: bool = Field(..., description="Overall validation result")
    summary: ValidationSummary = Field(..., description="Validation summary")
    details: ValidationDetails = Field(..., description="Detailed validation results")
    recommendations: List[str] = Field(..., description="Improvement recommendations")
    metadata: Dict[str, Any] = Field(..., description="Processing metadata")


class StatusResponse(BaseModel):
    """Status check response."""
    job_id: str = Field(..., description="Job identifier")
    type: str = Field(..., description="Job type (conversion/validation)")
    status: str = Field(..., description="Current status")
    progress: int = Field(..., description="Completion percentage")
    estimated_time_remaining: Optional[int] = Field(None, description="Estimated time remaining in ms")
    current_step: str = Field(..., description="Current processing step")
    steps: List[Dict[str, Any]] = Field(..., description="Processing steps")
    metrics: Dict[str, Any] = Field(..., description="Processing metrics")
    timestamps: Dict[str, str] = Field(..., description="Processing timestamps")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service health status")
    timestamp: str = Field(..., description="Check timestamp")
    version: str = Field(..., description="Service version")
    dependencies: Dict[str, str] = Field(default_factory=dict, description="Dependency statuses")


class TenantProvisionRequest(BaseModel):
    """Tenant provisioning request."""
    tenant_id: str = Field(..., description="Unique tenant identifier")
    organization_name: str = Field(..., description="Organization name")
    plan: str = Field(..., description="Service plan (starter/professional/enterprise)")


class TenantProvisionResult(BaseModel):
    """Tenant provisioning result."""
    tenant_id: str = Field(..., description="Tenant identifier")
    organization_name: str = Field(..., description="Organization name")
    plan: str = Field(..., description="Service plan")
    status: str = Field(..., description="Provisioning status")
    endpoints: Dict[str, str] = Field(..., description="API endpoints")
    created_at: str = Field(..., description="Creation timestamp")


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")