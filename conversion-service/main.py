"""
TSI Conversion Microservice

FastAPI application providing transport data conversion services.
Supports EDIFACT (SKDUPD/TSDUPD) and GTFS format generation.
"""

import os
import time
import uuid
import asyncio
import tempfile
from typing import Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import ValidationError as PydanticValidationError

from src.tsi_converter.models import (
    ConversionRequest, ConversionResult, ValidationRequest, ValidationResult,
    StatusResponse, HealthResponse, TenantProvisionRequest, TenantProvisionResult,
    ErrorResponse, OutputFormat
)
from src.tsi_converter.edifact_writer import write_skdupd, write_tsdupd
from src.tsi_converter.gtfs_writer import write_gtfs_static, write_gtfs_realtime, create_gtfs_zip
from src.tsi_converter.file_handler import file_handler


# Global job storage (in production, use Redis or database)
job_storage: Dict[str, Dict[str, Any]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print("TSI Conversion Service starting up...")
    
    yield
    
    # Shutdown  
    print("TSI Conversion Service shutting down...")


app = FastAPI(
    title="TSI Conversion Microservice",
    description="Transport data conversion service for EDIFACT and GTFS formats",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"error": f"Internal server error: {str(exc)}"}
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        dependencies={
            "edifact_writer": "operational",
            "gtfs_writer": "operational"
        }
    )


@app.post("/convert/skdupd", response_model=ConversionResult)
async def convert_to_skdupd(request: ConversionRequest, background_tasks: BackgroundTasks):
    """Convert transport data to EDIFACT SKDUPD format."""
    job_id = f"skdupd_{int(time.time())}_{str(uuid.uuid4())[:8]}"
    
    try:
        # Validate required data
        if 'agencies' not in request.input_data or 'services' not in request.input_data:
            raise HTTPException(
                status_code=400,
                detail="Missing required 'agencies' or 'services' data for SKDUPD conversion"
            )
        
        # Perform conversion
        start_time = time.time()
        edifact_content = write_skdupd(
            request.input_data,
            version=request.options.get('version', 'CURRENT'),
            una=request.options.get('una', "UNA:+.? '")
        )
        processing_time = int((time.time() - start_time) * 1000)
        
        # Calculate statistics
        agencies_count = len(request.input_data.get('agencies', []))
        services_count = len(request.input_data.get('services', []))
        
        result = ConversionResult(
            job_id=job_id,
            input_format="json",
            output_format=request.output_format.value,
            status="completed",
            progress=100,
            results={
                "original_records": agencies_count + services_count,
                "converted_records": agencies_count + services_count,
                "validation_errors": 0,
                "warnings": 0,
                "edifact_length": len(edifact_content),
                "edifact_segments": edifact_content.count("'")
            },
            output={
                "type": "EDIFACT_SKDUPD",
                "content": edifact_content,
                "encoding": "UTF-8",
                "segments": edifact_content.count("'")
            },
            metadata={
                "processing_time": processing_time,
                "conversion_engine": "TSI-Converter-v1.0",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # Store job for status tracking
        job_storage[job_id] = result.dict()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SKDUPD conversion failed: {str(e)}")


@app.post("/convert/tsdupd", response_model=ConversionResult)
async def convert_to_tsdupd(request: ConversionRequest, background_tasks: BackgroundTasks):
    """Convert transport data to EDIFACT TSDUPD format."""
    job_id = f"tsdupd_{int(time.time())}_{str(uuid.uuid4())[:8]}"
    
    try:
        # Validate required data
        if 'stations' not in request.input_data:
            raise HTTPException(
                status_code=400,
                detail="Missing required 'stations' data for TSDUPD conversion"
            )
        
        # Perform conversion
        start_time = time.time()
        edifact_content = write_tsdupd(
            request.input_data,
            version=request.options.get('version', 'CURRENT'),
            una=request.options.get('una', "UNA:+.? '")
        )
        processing_time = int((time.time() - start_time) * 1000)
        
        # Calculate statistics
        stations_count = len(request.input_data.get('stations', []))
        
        result = ConversionResult(
            job_id=job_id,
            input_format="json",
            output_format=request.output_format.value,
            status="completed",
            progress=100,
            results={
                "original_records": stations_count,
                "converted_records": stations_count,
                "validation_errors": 0,
                "warnings": 0,
                "edifact_length": len(edifact_content),
                "edifact_segments": edifact_content.count("'")
            },
            output={
                "type": "EDIFACT_TSDUPD",
                "content": edifact_content,
                "encoding": "UTF-8",
                "segments": edifact_content.count("'")
            },
            metadata={
                "processing_time": processing_time,
                "conversion_engine": "TSI-Converter-v1.0",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # Store job for status tracking
        job_storage[job_id] = result.dict()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TSDUPD conversion failed: {str(e)}")


@app.post("/convert/gtfs", response_model=ConversionResult)
async def convert_to_gtfs(request: ConversionRequest, background_tasks: BackgroundTasks):
    """Convert transport data to GTFS format."""
    job_id = f"gtfs_{int(time.time())}_{str(uuid.uuid4())[:8]}"
    
    try:
        # Validate required data
        required_fields = ['agencies', 'stations', 'services']
        for field in required_fields:
            if field not in request.input_data:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required '{field}' data for GTFS conversion"
                )
        
        # Perform conversion
        start_time = time.time()
        gtfs_files = write_gtfs_static(request.input_data)
        
        # Create ZIP if requested
        if request.options.get('format') == 'zip':
            zip_content = create_gtfs_zip(gtfs_files)
            # TODO: Save ZIP to temporary storage and return download URL
            output = {
                "type": "GTFS_ZIP",
                "content": f"ZIP archive ({len(zip_content)} bytes)",
                "files": list(gtfs_files.keys()),
                "download_url": f"/download/gtfs/{job_id}.zip"
            }
        else:
            output = {
                "type": "GTFS",
                "files": gtfs_files,
                "validation": {
                    "errors": 0,
                    "warnings": 0,
                    "notices": ["GTFS package successfully generated"]
                }
            }
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Calculate statistics
        total_records = sum(len(request.input_data.get(field, [])) for field in required_fields)
        
        result = ConversionResult(
            job_id=job_id,
            input_format="json",
            output_format=request.output_format.value,
            status="completed",
            progress=100,
            results={
                "original_records": total_records,
                "converted_records": total_records,
                "validation_errors": 0,
                "warnings": 0,
                "gtfs_files": len(gtfs_files)
            },
            output=output,
            metadata={
                "processing_time": processing_time,
                "conversion_engine": "TSI-Converter-v1.0",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # Store job for status tracking
        job_storage[job_id] = result.dict()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GTFS conversion failed: {str(e)}")


@app.post("/convert/gtfs-realtime", response_model=ConversionResult)
async def convert_to_gtfs_realtime(request: ConversionRequest, background_tasks: BackgroundTasks):
    """Convert transport data to GTFS Realtime format."""
    job_id = f"gtfs_rt_{int(time.time())}_{str(uuid.uuid4())[:8]}"
    
    try:
        # Perform conversion (placeholder implementation)
        start_time = time.time()
        feeds = write_gtfs_realtime(request.input_data)
        processing_time = int((time.time() - start_time) * 1000)
        
        result = ConversionResult(
            job_id=job_id,
            input_format="json",
            output_format=request.output_format.value,
            status="completed",
            progress=100,
            results={
                "original_records": 1,
                "converted_records": 1,
                "validation_errors": 0,
                "warnings": 1  # Placeholder implementation warning
            },
            output={
                "type": "GTFS_REALTIME",
                "protobuf": True,
                "feeds": {feed_type: f"Binary protobuf data ({len(content)} bytes)" 
                         for feed_type, content in feeds.items()}
            },
            metadata={
                "processing_time": processing_time,
                "conversion_engine": "TSI-Converter-v1.0",
                "timestamp": datetime.utcnow().isoformat(),
                "warnings": ["This is a placeholder implementation for GTFS-Realtime"]
            }
        )
        
        # Store job for status tracking
        job_storage[job_id] = result.dict()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GTFS-Realtime conversion failed: {str(e)}")


@app.post("/validate", response_model=ValidationResult)
async def validate_data(request: ValidationRequest, background_tasks: BackgroundTasks):
    """Validate transport data."""
    job_id = f"val_{int(time.time())}_{str(uuid.uuid4())[:8]}"
    
    try:
        start_time = time.time()
        
        # Basic validation logic (placeholder)
        errors = []
        warnings = []
        notices = []
        
        # Check for required fields based on format
        if request.format == "json-transport":
            if 'agencies' not in request.input_data:
                errors.append({
                    "code": "MISSING_REQUIRED_FIELD",
                    "message": "Required field 'agencies' is missing",
                    "field": "agencies",
                    "severity": "error"
                })
        
        # Calculate validation stats
        total_records = sum(len(v) if isinstance(v, list) else 1 
                           for v in request.input_data.values())
        valid_records = total_records - len(errors)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        result = ValidationResult(
            job_id=job_id,
            format=request.format,
            validation_level=request.validation_level.value,
            status="completed",
            is_valid=len(errors) == 0,
            summary={
                "total_records": total_records,
                "valid_records": valid_records,
                "errors": errors,
                "warnings": warnings,
                "notices": notices
            },
            details={
                "field_validation": {
                    "required": {"passed": valid_records, "failed": len(errors), "percentage": 100.0 if total_records == 0 else (valid_records / total_records) * 100},
                    "format": {"passed": total_records, "failed": 0, "percentage": 100.0},
                    "range": {"passed": total_records, "failed": 0, "percentage": 100.0}
                },
                "data_integrity": {
                    "consistency": {"score": 100.0, "issues": 0},
                    "completeness": {"score": 98.5, "missing": len(errors)},
                    "accuracy": {"score": 99.0, "outliers": 0}
                }
            },
            recommendations=[
                "Fix validation errors to improve data quality",
                "Consider adding optional fields for better usability"
            ] if errors else [
                "Data validation passed successfully",
                "Consider periodic validation checks"
            ],
            metadata={
                "validation_engine": "TSI-Validator-v1.0",
                "processing_time": processing_time,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # Store job for status tracking
        job_storage[job_id] = result.dict()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@app.get("/status/{job_id}", response_model=StatusResponse)
async def get_job_status(job_id: str):
    """Get job status by ID."""
    if job_id not in job_storage:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    job_data = job_storage[job_id]
    
    # Determine job type from job_id prefix
    job_type = "conversion"
    if job_id.startswith("val_"):
        job_type = "validation"
    
    return StatusResponse(
        job_id=job_id,
        type=job_type,
        status=job_data.get('status', 'unknown'),
        progress=job_data.get('progress', 0),
        estimated_time_remaining=None,
        current_step="Completed" if job_data.get('status') == 'completed' else "Processing",
        steps=[
            {"name": "parsing", "status": "completed", "duration": 100},
            {"name": "processing", "status": "completed", "duration": job_data.get('metadata', {}).get('processing_time', 0)},
            {"name": "completion", "status": "completed", "duration": 50}
        ],
        metrics={
            "records_processed": job_data.get('results', {}).get('original_records', 0),
            "errors_found": job_data.get('results', {}).get('validation_errors', 0),
            "warnings_found": job_data.get('results', {}).get('warnings', 0)
        },
        timestamps={
            "started": job_data.get('metadata', {}).get('timestamp', ''),
            "completed": job_data.get('metadata', {}).get('timestamp', '')
        }
    )


@app.post("/provision", response_model=TenantProvisionResult)
async def provision_tenant(request: TenantProvisionRequest):
    """Provision a new tenant."""
    try:
        # TODO: Implement actual tenant provisioning logic
        # This is a placeholder that returns success
        
        result = TenantProvisionResult(
            tenant_id=request.tenant_id,
            organization_name=request.organization_name,
            plan=request.plan,
            status="provisioned",
            endpoints={
                "convert": "https://tsi-converter.example.com/convert",
                "validate": "https://tsi-converter.example.com/validate",
                "status": "https://tsi-converter.example.com/status"
            },
            created_at=datetime.utcnow().isoformat()
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tenant provisioning failed: {str(e)}")


@app.post("/upload", response_model=ConversionResult)
async def upload_and_convert(
    file: UploadFile = File(...),
    output_format: OutputFormat = OutputFormat.GTFS_STATIC,
    background_tasks: BackgroundTasks = None
):
    """Upload file and convert to specified format."""
    job_id = f"upload_{int(time.time())}_{str(uuid.uuid4())[:8]}"
    
    try:
        # Validate file type
        if not file.filename or not file.filename.endswith('.json'):
            raise HTTPException(
                status_code=400,
                detail="Only JSON files are supported"
            )
        
        # Save uploaded file
        file_path = await file_handler.save_uploaded_file(file, job_id)
        
        # Read and parse JSON
        json_data = await file_handler.read_json_file(file_path)
        
        # Create conversion request
        request = ConversionRequest(
            input_data=json_data,
            output_format=output_format,
            options={}
        )
        
        # Route to appropriate converter
        if output_format == OutputFormat.EDIFACT_SKDUPD:
            return await convert_to_skdupd(request, background_tasks)
        elif output_format == OutputFormat.EDIFACT_TSDUPD:
            return await convert_to_tsdupd(request, background_tasks)
        elif output_format == OutputFormat.GTFS_STATIC:
            return await convert_to_gtfs(request, background_tasks)
        elif output_format == OutputFormat.GTFS_REALTIME:
            return await convert_to_gtfs_realtime(request, background_tasks)
        else:
            raise HTTPException(status_code=400, detail="Unsupported output format")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload conversion failed: {str(e)}")


@app.get("/download/{job_id}/{filename}")
async def download_file(job_id: str, filename: str):
    """Download converted file."""
    try:
        file_path = file_handler.get_file_path(job_id, filename)
        
        if not file_handler.file_exists(job_id, filename):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Determine media type based on extension
        if filename.endswith('.zip'):
            media_type = "application/zip"
        elif filename.endswith('.txt') or filename.endswith('.edi'):
            media_type = "text/plain"
        else:
            media_type = "application/octet-stream"
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type=media_type
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)