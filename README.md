# TSI Agent Runtime

Transport Systems Integration (TSI) Agent Runtime Engine for converting JSON transport data to EDIFACT and GTFS formats.

## Overview

TSI Agent is a specialized AI-powered conversion engine that transforms transport data between formats commonly used in European public transport systems. It supports:

- **EDIFACT Generation**: SKDUPD and TSDUPD formats compliant with IATA/European transport standards
- **GTFS Export**: Complete GTFS feeds for Google Maps and transport applications  
- **Real-time Processing**: Fast conversion with live progress updates
- **Smart Validation**: AI-powered validation ensuring format compliance

## Architecture

This is the agent/runtime component of the TSI Platform:

1. **TSI Directory** (marketing site) - Domain: `tsi-directory.avantle.ai` 
2. **TSI Agent Runtime** (this repository) - Domain: `tsi.avantle.ai`

## API Endpoints

### Core Conversion API

```bash
# Convert transport data
POST /api/v1/convert
Content-Type: application/json
Authorization: Bearer <jwt-token>

{
  "inputData": { ... },
  "outputFormat": "edifact-skdupd|edifact-tsdupd|gtfs|gtfs-realtime",
  "options": {},
  "tenantId": "tenant-id"
}
```

### Validation API

```bash
# Validate transport data
POST /api/v1/validate  
Content-Type: application/json
Authorization: Bearer <jwt-token>

{
  "inputData": { ... },
  "format": "json-transport|edifact|gtfs",
  "validationLevel": "standard|strict",
  "tenantId": "tenant-id"
}
```

### Status Monitoring

```bash
# Check job status
GET /api/v1/status?jobId=<job-id>&tenantId=<tenant-id>
Authorization: Bearer <jwt-token>
```

### Tenant Management

```bash
# Provision new tenant
POST /api/provision
Content-Type: application/json

{
  "tenantId": "unique-tenant-id",
  "organizationName": "Organization Name", 
  "plan": "starter|professional|enterprise"
}
```

## Supported Formats

### Input Formats
- JSON transport data
- XML transport schemas
- CSV route/schedule files

### Output Formats

**EDIFACT:**
- SKDUPD (Schedule Update)
- TSDUPD (Time Schedule Update)
- Compliant with IATA D.00B standard

**GTFS:**
- GTFS Static (agency.txt, routes.txt, stops.txt, etc.)
- GTFS Realtime (Protocol Buffer format)

## Development

### Prerequisites
- Node.js 18+
- npm or pnpm
- PostgreSQL (production) or SQLite (development)

### Environment Setup

```bash
# Copy environment template
cp .env.example .env.local

# Install dependencies  
pnpm install

# Start development server
pnpm dev
```

The agent will be available at `http://localhost:3000`

### Environment Variables

Key configuration variables:

```env
# Authentication
JWT_SECRET=your-jwt-secret
ENCRYPTION_KEY=your-encryption-key

# AI/LLM  
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openai-key
LLM_MODEL=gpt-4

# TSI-Specific
TSI_EDIFACT_VERSION=D00B
TSI_GTFS_VERSION=2.0
TSI_VALIDATION_LEVEL=strict

# Database
DATABASE_URL=postgresql://user:pass@host:5432/tsi_agent
```

### Commands

```bash
pnpm dev              # Development server
pnpm build           # Production build  
pnpm start           # Production server
pnpm lint            # Code linting
```

## API Testing

### Example Conversion Request

```bash
curl -X POST http://localhost:3000/api/v1/convert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "inputData": {
      "routes": [
        {
          "route_id": "R1",
          "route_short_name": "1",
          "route_long_name": "Main Line", 
          "route_type": 3
        }
      ]
    },
    "outputFormat": "gtfs",
    "tenantId": "demo-tenant"
  }'
```

### Example Validation Request

```bash
curl -X POST http://localhost:3000/api/v1/validate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "inputData": { ... },
    "format": "json-transport",
    "validationLevel": "standard",
    "tenantId": "demo-tenant"
  }'
```

## Monitoring

Access the agent monitoring dashboard at `/agent` to view:

- Real-time conversion statistics
- API endpoint status  
- Recent processing activity
- System performance metrics

## Security

- JWT-based authentication for all API endpoints
- Rate limiting per tenant (configurable)
- Multi-tenant data isolation
- Audit logging of all operations
- CORS configuration for domain restrictions

## Deployment

### Vercel (Recommended)

The project is configured for Vercel deployment:

```bash
# Deploy to Vercel
vercel

# Set environment variables in Vercel dashboard
# Configure domain: tsi.avantle.ai
```

### Docker

```bash
# Build Docker image
docker build -t tsi-agent .

# Run container
docker run -p 3000:3000 \
  -e DATABASE_URL="..." \
  -e JWT_SECRET="..." \
  tsi-agent
```

## License

Proprietary - Avantle Technologies s.r.o.

## Support

For technical support and integration questions:
- Documentation: https://docs.tsi.avantle.ai
- Support: support@avantle.ai
