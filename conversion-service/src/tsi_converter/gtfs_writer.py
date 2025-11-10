"""
GTFS writer for transport data conversion

This module handles the conversion of TSI data to GTFS formats:
- GTFS Static: Complete feed with all required files
- GTFS Realtime: Protocol Buffer format (placeholder)

Generates valid GTFS feeds compatible with Google Transit and other systems.
"""

import csv
import io
import zipfile
from typing import Dict, Any, List, Optional
from datetime import datetime


def write_gtfs_static(json_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate GTFS static files from JSON input.
    
    Args:
        json_data: Input JSON data dictionary
        
    Returns:
        Dictionary mapping filename to file content
        
    Raises:
        ValueError: If required data is missing or invalid
    """
    # Validate required data
    if 'agencies' not in json_data:
        raise ValueError("Missing required 'agencies' data")
    if 'stations' not in json_data:
        raise ValueError("Missing required 'stations' data")
    if 'services' not in json_data:
        raise ValueError("Missing required 'services' data")
    
    agencies = json_data['agencies']
    stations = json_data['stations']
    services = json_data['services']
    
    if not agencies or not stations or not services:
        raise ValueError("Agencies, stations, and services cannot be empty")
    
    # Generate GTFS files
    gtfs_files = {}
    
    # Generate agency.txt
    gtfs_files['agency.txt'] = _generate_agency_file(agencies)
    
    # Generate stops.txt  
    gtfs_files['stops.txt'] = _generate_stops_file(stations)
    
    # Generate routes.txt
    gtfs_files['routes.txt'] = _generate_routes_file(services, agencies)
    
    # Generate calendar.txt
    gtfs_files['calendar.txt'] = _generate_calendar_file(services)
    
    # Generate trips.txt
    gtfs_files['trips.txt'] = _generate_trips_file(services)
    
    # Generate stop_times.txt
    gtfs_files['stop_times.txt'] = _generate_stop_times_file(services)
    
    # Optional: Generate feed_info.txt
    gtfs_files['feed_info.txt'] = _generate_feed_info_file(json_data)
    
    return gtfs_files


def _generate_agency_file(agencies: List[Dict[str, Any]]) -> str:
    """Generate agency.txt content."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'agency_id',
        'agency_name', 
        'agency_url',
        'agency_timezone',
        'agency_lang',
        'agency_phone',
        'agency_email'
    ])
    
    # Write agency data
    for agency in agencies:
        writer.writerow([
            agency.get('id', ''),
            agency.get('name', ''),
            agency.get('url', ''),
            agency.get('timezone', 'Europe/Bratislava'),
            agency.get('lang', ''),
            agency.get('phone', ''),
            agency.get('email', '')
        ])
    
    return output.getvalue()


def _generate_stops_file(stations: List[Dict[str, Any]]) -> str:
    """Generate stops.txt content."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'stop_id',
        'stop_code',
        'stop_name',
        'stop_desc',
        'stop_lat',
        'stop_lon',
        'zone_id',
        'stop_url',
        'location_type',
        'parent_station',
        'wheelchair_boarding'
    ])
    
    # Write station data
    for station in stations:
        writer.writerow([
            station.get('id', ''),
            station.get('code', ''),
            station.get('name', ''),
            station.get('desc', ''),
            station.get('lat', ''),
            station.get('lon', ''),
            station.get('zone_id', ''),
            station.get('url', ''),
            station.get('location_type', 0),
            station.get('parent_station', ''),
            station.get('wheelchair_boarding', 0)
        ])
    
    return output.getvalue()


def _generate_routes_file(services: List[Dict[str, Any]], agencies: List[Dict[str, Any]]) -> str:
    """Generate routes.txt content."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'route_id',
        'agency_id',
        'route_short_name',
        'route_long_name',
        'route_desc',
        'route_type',
        'route_url',
        'route_color',
        'route_text_color'
    ])
    
    # Write route data
    for service in services:
        writer.writerow([
            service.get('id', ''),
            service.get('agency_id', ''),
            service.get('route_short_name', ''),
            service.get('route_long_name', ''),
            service.get('route_desc', ''),
            service.get('route_type', 3),  # Default to bus
            service.get('route_url', ''),
            service.get('route_color', ''),
            service.get('route_text_color', '')
        ])
    
    return output.getvalue()


def _generate_calendar_file(services: List[Dict[str, Any]]) -> str:
    """Generate calendar.txt content."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'service_id',
        'monday',
        'tuesday', 
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday',
        'start_date',
        'end_date'
    ])
    
    # Write calendar data from variants
    calendar_services = set()
    for service in services:
        variants = service.get('variants', [])
        for variant in variants:
            calendar = variant.get('calendar', {})
            service_id = variant.get('id', '')
            
            if service_id and service_id not in calendar_services:
                calendar_services.add(service_id)
                writer.writerow([
                    service_id,
                    1 if calendar.get('monday', False) else 0,
                    1 if calendar.get('tuesday', False) else 0,
                    1 if calendar.get('wednesday', False) else 0,
                    1 if calendar.get('thursday', False) else 0,
                    1 if calendar.get('friday', False) else 0,
                    1 if calendar.get('saturday', False) else 0,
                    1 if calendar.get('sunday', False) else 0,
                    calendar.get('start_date', '20240101'),
                    calendar.get('end_date', '20241231')
                ])
    
    return output.getvalue()


def _generate_trips_file(services: List[Dict[str, Any]]) -> str:
    """Generate trips.txt content."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'route_id',
        'service_id',
        'trip_id',
        'trip_headsign',
        'trip_short_name',
        'direction_id',
        'block_id',
        'wheelchair_accessible',
        'bikes_allowed'
    ])
    
    # Write trip data
    trip_counter = 0
    for service in services:
        route_id = service.get('id', '')
        variants = service.get('variants', [])
        
        for variant in variants:
            service_id = variant.get('id', '')
            trip_counter += 1
            trip_id = f"{route_id}_{trip_counter}"
            
            writer.writerow([
                route_id,
                service_id,
                trip_id,
                service.get('route_long_name', ''),
                service.get('route_short_name', ''),
                0,  # direction_id
                '',  # block_id
                0,   # wheelchair_accessible
                0    # bikes_allowed
            ])
    
    return output.getvalue()


def _generate_stop_times_file(services: List[Dict[str, Any]]) -> str:
    """Generate stop_times.txt content."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'trip_id',
        'arrival_time',
        'departure_time',
        'stop_id',
        'stop_sequence',
        'stop_headsign',
        'pickup_type',
        'drop_off_type',
        'timepoint'
    ])
    
    # Write stop times data
    trip_counter = 0
    for service in services:
        route_id = service.get('id', '')
        variants = service.get('variants', [])
        calls = service.get('calls', [])
        
        for variant in variants:
            trip_counter += 1
            trip_id = f"{route_id}_{trip_counter}"
            
            # Write stop times for this trip
            for call in calls:
                writer.writerow([
                    trip_id,
                    call.get('arrival_time', ''),
                    call.get('departure_time', ''),
                    call.get('station_id', ''),
                    call.get('stop_sequence', 1),
                    call.get('stop_headsign', ''),
                    call.get('pickup_type', 0),
                    call.get('drop_off_type', 0),
                    call.get('timepoint', 1)
                ])
    
    return output.getvalue()


def _generate_feed_info_file(json_data: Dict[str, Any]) -> str:
    """Generate feed_info.txt content."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'feed_publisher_name',
        'feed_publisher_url',
        'feed_lang',
        'feed_start_date',
        'feed_end_date',
        'feed_version',
        'feed_contact_email',
        'feed_contact_url'
    ])
    
    publisher = json_data.get('publisher', {})
    
    # Calculate feed date range from services
    start_date = '20240101'
    end_date = '20241231'
    
    for service in json_data.get('services', []):
        for variant in service.get('variants', []):
            calendar = variant.get('calendar', {})
            if calendar.get('start_date'):
                start_date = min(start_date, calendar['start_date'])
            if calendar.get('end_date'):
                end_date = max(end_date, calendar['end_date'])
    
    writer.writerow([
        publisher.get('name', 'TSI Data Publisher'),
        publisher.get('url', ''),
        'en',  # Default language
        start_date,
        end_date,
        datetime.now().strftime('%Y%m%d'),
        publisher.get('email', ''),
        publisher.get('url', '')
    ])
    
    return output.getvalue()


def create_gtfs_zip(gtfs_files: Dict[str, str]) -> bytes:
    """
    Create a ZIP archive containing GTFS files.
    
    Args:
        gtfs_files: Dictionary mapping filename to file content
        
    Returns:
        ZIP file content as bytes
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in gtfs_files.items():
            zip_file.writestr(filename, content)
    
    return zip_buffer.getvalue()


def write_gtfs_realtime(json_data: Dict[str, Any]) -> Dict[str, bytes]:
    """
    Generate GTFS Realtime feeds from JSON input.
    
    Args:
        json_data: Input JSON data dictionary
        
    Returns:
        Dictionary mapping feed type to protobuf content
        
    Note:
        This is a placeholder implementation. 
        Full GTFS-RT implementation requires protobuf compilation.
    """
    # TODO: Implement actual GTFS-Realtime protocol buffer generation
    # This requires gtfs-realtime-bindings and protobuf compilation
    
    feeds = {}
    
    # Mock protobuf data for demonstration
    mock_protobuf = b'\x08\x96\x92\xb3\xa7\x06\x12\x1a\x08\x01\x12\x16\x0a\x04trip\x12\x0e\x0a\x0c\x08\x01\x12\x08test_trip'
    
    feeds['vehicle_positions'] = mock_protobuf
    feeds['trip_updates'] = mock_protobuf  
    feeds['alerts'] = mock_protobuf
    
    return feeds