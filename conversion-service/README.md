# TSI Conversion Microservice

FastAPI-based microservice for converting transport data between formats:
- JSON → EDIFACT (SKDUPD, TSDUPD)
- JSON → GTFS (Static, Realtime)

## Features

- **EDIFACT Generation**: Full SKDUPD and TSDUPD format support
- **GTFS Export**: Complete GTFS feeds with validation
- **File Upload/Download**: Support for large file processing
- **Real-time Status**: Job progress monitoring
- **Health Checks**: Built-in health monitoring
- **Docker Support**: Container-ready deployment

## API Endpoints

### Conversion Endpoints

```bash
# Convert to EDIFACT SKDUPD
POST /convert/skdupd

# Convert to EDIFACT TSDUPD  
POST /convert/tsdupd

# Convert to GTFS Static
POST /convert/gtfs

# Convert to GTFS Realtime
POST /convert/gtfs-realtime

# Upload file and convert
POST /upload?output_format=gtfs
```

### Utility Endpoints

```bash
# Validate transport data
POST /validate

# Check job status
GET /status/{job_id}

# Health check
GET /health

# Download results
GET /download/{job_id}/{filename}

# Provision tenant
POST /provision
```

## Quick Start

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py

# Service available at http://localhost:8000
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t tsi-converter .
docker run -p 8000:8000 tsi-converter
```

## Usage Examples

### Convert JSON to EDIFACT SKDUPD

```bash
curl -X POST http://localhost:8000/convert/skdupd \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "publisher": {"name": "Test Transport", "url": "https://test.com"},
      "agencies": [{"id": "agency_1", "name": "Test Agency", "timezone": "Europe/Bratislava"}],
      "services": [{"id": "service_1", "agency_id": "agency_1", "route_type": 3, "variants": [], "calls": []}]
    },
    "output_format": "edifact-skdupd",
    "options": {"version": "CURRENT"}
  }'
```

### Upload File and Convert

```bash
# Upload JSON file and convert to GTFS
curl -X POST http://localhost:8000/upload \
  -F "file=@transport_data.json" \
  -F "output_format=gtfs"
```

### Check Job Status

```bash
curl -X GET http://localhost:8000/status/skdupd_1699123456_abc123def
```

## Input Data Format

The service expects JSON data in TSI format:

```json
{
  "publisher": {
    "id": "publisher_id",
    "name": "Publisher Name", 
    "url": "https://example.com"
  },
  "agencies": [
    {
      "id": "agency_1",
      "name": "Transport Agency",
      "timezone": "Europe/Bratislava"
    }
  ],
  "stations": [
    {
      "id": "station_1",
      "name": "Central Station",
      "lat": 48.1486,
      "lon": 17.1077
    }
  ],
  "services": [
    {
      "id": "service_1",
      "agency_id": "agency_1",
      "route_type": 3,
      "variants": [
        {
          "id": "variant_1",
          "calendar": {
            "service_id": "variant_1",
            "monday": true,
            "tuesday": true,
            "wednesday": true,
            "thursday": true,
            "friday": true,
            "saturday": false,
            "sunday": false,
            "start_date": "20240101",
            "end_date": "20241231"
          }
        }
      ],
      "calls": [
        {
          "station_id": "station_1",
          "arrival_time": "08:00:00",
          "departure_time": "08:00:00",
          "stop_sequence": 1
        }
      ]
    }
  ]
}
```

## Output Formats

### EDIFACT SKDUPD/TSDUPD

Returns EDIFACT message as string:
```
UNA:+.? 'UNB+UNOC:3+Test Transport+RECEIVER+240101:0000+123ABC456DEF'UNH+...
```

### GTFS Static

Returns dictionary of GTFS files:
```json
{
  "files": {
    "agency.txt": "agency_id,agency_name,agency_url,agency_timezone\n...",
    "stops.txt": "stop_id,stop_name,stop_lat,stop_lon\n...",
    "routes.txt": "route_id,agency_id,route_short_name,route_type\n...",
    ...
  }
}
```

## Configuration

Environment variables:

- `STORAGE_PATH`: Temporary file storage path (default: system temp)
- `LOG_LEVEL`: Logging level (default: info)

## Health Monitoring

```bash
# Check service health
curl http://localhost:8000/health

# Response
{
  "status": "healthy",
  "timestamp": "2024-11-10T10:30:00Z",
  "version": "1.0.0",
  "dependencies": {
    "edifact_writer": "operational",
    "gtfs_writer": "operational"
  }
}
```

## Error Handling

All endpoints return structured error responses:

```json
{
  "error": "Missing required 'agencies' data for SKDUPD conversion",
  "code": "VALIDATION_ERROR",
  "details": {
    "field": "agencies",
    "required": true
  }
}
```

## Performance

- **EDIFACT conversion**: ~10ms for typical datasets
- **GTFS generation**: ~50ms for typical datasets  
- **File upload**: Supports files up to 100MB
- **Concurrent processing**: Async/await for non-blocking operations

## Integration

This microservice integrates with the TSI Agent Runtime at:
- Next.js frontend: `http://localhost:3000`
- Main API endpoints: `/api/v1/convert`, `/api/v1/validate`

The microservice runs independently and can be deployed as a separate container or service.