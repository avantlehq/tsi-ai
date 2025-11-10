"""
EDIFACT writer for SKDUPD and TSDUPD formats

This module handles the conversion of TSI data to EDIFACT formats:
- SKDUPD: Slovak transport data format
- TSDUPD: European transport data format

Generates deterministic EDIFACT messages with proper escaping and segment counting.
Refactored for MERITS validator compliance.

Extracted from tsi-directory repository for microservice integration.
"""

import hashlib
from typing import Dict, Any, List, Union
from dataclasses import dataclass


@dataclass
class Sep:
    """EDIFACT separators from UNA string."""
    comp: str = ':'      # component separator
    elem: str = '+'      # element separator  
    dec: str = '.'       # decimal separator
    rel: str = '?'       # release character
    seg: str = "'"       # segment terminator


def escape(value: str, s: Sep) -> str:
    """
    Escape special EDIFACT characters using release character.
    Only escapes characters in textual fields, not in composites.
    
    Args:
        value: String to escape
        s: EDIFACT separators
        
    Returns:
        Escaped string with special characters prefixed by release character
    """
    if not isinstance(value, str):
        value = str(value)
    
    # Escape release character first, then others
    result = value.replace(s.rel, s.rel + s.rel)
    result = result.replace(s.seg, s.rel + s.seg)
    result = result.replace(s.elem, s.rel + s.elem)
    result = result.replace(s.comp, s.rel + s.comp)
    
    return result


def seg(tag: str, elements: List[Union[str, List[str]]], s: Sep) -> str:
    """
    Build an EDIFACT segment from tag and elements.
    Supports both simple elements and composites.
    
    Args:
        tag: Segment tag (e.g., 'UNB', 'UNH')
        elements: List of segment elements or composites
        s: EDIFACT separators
        
    Returns:
        Complete EDIFACT segment with terminator
    """
    processed_elements = []
    
    for element in elements:
        if isinstance(element, list):
            # Composite: join components with comp separator, no escaping
            composite = s.comp.join(str(comp) for comp in element)
            processed_elements.append(composite)
        else:
            # Simple element: escape special characters
            escaped = escape(str(element), s)
            processed_elements.append(escaped)
    
    return tag + s.elem + s.elem.join(processed_elements) + s.seg


def generate_deterministic_ref(publisher: Dict[str, Any], version: str) -> str:
    """
    Generate deterministic reference ID from publisher data.
    
    Args:
        publisher: Publisher information dictionary
        version: Version identifier
        
    Returns:
        Deterministic reference string (12 characters, uppercase)
    """
    name = publisher.get('name', '')
    url = publisher.get('url', '')
    
    # Build deterministic string for hashing
    hash_input = f"{name}-{url}-{version}"
    hash_hex = hashlib.sha1(hash_input.encode('utf-8')).hexdigest()
    
    # Return first 12 characters in uppercase
    return hash_hex[:12].upper()


def make_unb(sender_id: str, receiver_id: str, interchange_ref: str, 
             timestamp: str = None, s: Sep = None) -> str:
    """
    Generate UNB (Interchange Header) segment.
    
    Args:
        sender_id: Sender identification
        receiver_id: Receiver identification 
        interchange_ref: Interchange reference
        timestamp: Optional timestamp (YYMMDD:HHMM format)
        s: EDIFACT separators
        
    Returns:
        UNB segment string
    """
    if s is None:
        s = Sep()
    
    if timestamp is None:
        timestamp = "240101:0000"  # Default deterministic timestamp
    
    elements = [
        ['UNOC', '3'],              # Syntax identifier (composite)
        sender_id,                   # Sender (simple, will be escaped)
        receiver_id,                 # Receiver (simple, will be escaped)
        timestamp,                   # Date/time (simple, will be escaped)
        interchange_ref              # Interchange control reference (simple, will be escaped)
    ]
    
    return seg("UNB", elements, s)


def make_unh(message_ref: str, message_type: str, version: str = "CURRENT", s: Sep = None) -> str:
    """
    Generate UNH (Message Header) segment.
    
    Args:
        message_ref: Message reference number
        message_type: Message type (SKDUPD or TSDUPD)
        version: Version identifier
        s: EDIFACT separators
        
    Returns:
        UNH segment string
    """
    if s is None:
        s = Sep()
    
    elements = [
        message_ref,                                    # Message reference (simple)
        [message_type, 'D', '03B', 'UN', 'IATA', version]  # Message identifier (composite)
    ]
    
    return seg("UNH", elements, s)


def make_unt(segment_count: int, message_ref: str, s: Sep = None) -> str:
    """
    Generate UNT (Message Trailer) segment.
    
    Args:
        segment_count: Number of segments in message (including UNH and UNT)
        message_ref: Message reference number
        s: EDIFACT separators
        
    Returns:
        UNT segment string
    """
    if s is None:
        s = Sep()
    
    elements = [
        str(segment_count),
        message_ref
    ]
    
    return seg("UNT", elements, s)


def make_unz(message_count: int, interchange_ref: str, s: Sep = None) -> str:
    """
    Generate UNZ (Interchange Trailer) segment.
    
    Args:
        message_count: Number of messages in interchange
        interchange_ref: Interchange reference
        s: EDIFACT separators
        
    Returns:
        UNZ segment string
    """
    if s is None:
        s = Sep()
    
    elements = [
        str(message_count),
        interchange_ref
    ]
    
    return seg("UNZ", elements, s)


def map_tsdupd_segments(stations: List[Dict[str, Any]], s: Sep) -> List[str]:
    """
    Map stations data to TSDUPD EDIFACT segments.
    
    Args:
        stations: List of station dictionaries
        s: EDIFACT separators
        
    Returns:
        List of EDIFACT segment strings (without UNH/UNT)
        
    TODO: Implement detailed TSDUPD mapping according to specification.
    Current implementation is a placeholder that generates basic segments.
    """
    segments = []
    
    # TODO: Replace with actual TSDUPD segment group mapping
    # This is a placeholder implementation
    
    for station in stations:
        # Placeholder: Generate a basic LOC (Location) segment for each station
        station_id = station.get('id', '')
        station_name = station.get('name', '')
        lat = station.get('lat', '')
        lon = station.get('lon', '')
        
        # LOC segment - simple elements (will be escaped if needed)
        loc_elements = [
            "88",           # Location qualifier (88 = Place/location)
            station_id,     # Location identification
            "",             # Related location one identification  
            "",             # Related location two identification
            station_name    # Location name (will be escaped)
        ]
        segments.append(seg("LOC", loc_elements, s))
        
        # Add coordinates if available
        if lat and lon:
            gis_elements = [
                "1",        # Processing indicator
                str(lat),   # Latitude
                str(lon)    # Longitude
            ]
            segments.append(seg("GIS", gis_elements, s))
    
    return segments


def map_skdupd_segments(
    agencies: List[Dict[str, Any]], 
    services: List[Dict[str, Any]], 
    s: Sep,
    *,
    use_placeholders: bool = True
) -> List[str]:
    """
    Map agencies and services data to SKDUPD EDIFACT segments.
    
    Generates SKDUPD body segments using placeholder qualifiers that can be 
    easily customized later for specific SKDUPD specifications.
    
    Args:
        agencies: List of agency dictionaries
        services: List of service dictionaries  
        s: EDIFACT separators
        use_placeholders: Whether to use safe placeholder qualifiers
        
    Returns:
        List of EDIFACT segment strings (without UNH/UNT)
        
    TODO: Replace placeholder qualifiers with orthodox SKDUPD specification.
    Current qualifiers are safe defaults for testing and structure.
    """
    segments = []
    
    # TODO: domain mapping here - replace with actual SKDUPD qualifiers
    
    # Group services by carrier for proper NAD placement
    carriers_used = set()
    
    for service in services:
        carrier_uic = service.get('agency_id', '')
        
        # Generate NAD segment for carrier (only once per carrier)
        if carrier_uic and carrier_uic not in carriers_used:
            carriers_used.add(carrier_uic)
            
            # Find carrier info from agencies
            carrier_name = ""
            for agency in agencies:
                if agency.get('id') == carrier_uic:
                    carrier_name = agency.get('name', '')
                    break
            
            # NAD+CA+<carrier_uic>+<escaped_name>'
            nad_elements = [
                "CA",           # Party qualifier (CA = Carrier) - TODO: adjust per SKDUPD spec
                carrier_uic,    # Carrier UIC
                "",             # Name and address (empty)
                carrier_name    # Carrier name (will be escaped if contains special chars)
            ]
            segments.append(seg("NAD", nad_elements, s))
        
        # TDT+20+<train_number>' - Train/service header
        train_number = service.get('train_number', service.get('route_short_name', service.get('id', '')))
        tdt_elements = [
            "20",           # Transport stage qualifier - TODO: adjust per SKDUPD spec
            train_number    # Train number/service identifier
        ]
        segments.append(seg("TDT", tdt_elements, s))
        
        # Optional FTX for headsign/route_long_name
        headsign = service.get('headsign') or service.get('route_long_name')
        if headsign:
            # FTX+AAI+...+<escaped_headsign>'
            ftx_elements = [
                "AAI",      # Text subject qualifier - TODO: adjust per SKDUPD spec
                "",         # Text function
                "",         # Text reference
                headsign    # Text (will be escaped)
            ]
            segments.append(seg("FTX", ftx_elements, s))
        
        # Process variants for this service
        variants = service.get('variants', [])
        for variant in variants:
            service_id = variant.get('service_id', variant.get('id', ''))
            calendar = variant.get('calendar', {})
            
            # RFF+SRV:<service_id>' - Service reference (composite!)
            if service_id:
                rff_elements = [
                    ['SRV', service_id]  # Composite: SRV:service_id (no escaping)
                ]
                segments.append(seg("RFF", rff_elements, s))
            
            # Calendar period - start date
            start_date = calendar.get('start_date', '')
            if start_date:
                # Convert YYYYMMDD to YYYYMMDD format if needed
                if len(start_date) == 8 and start_date.isdigit():
                    # DTM+324:<YYYYMMDD>:102' (composite!)
                    dtm_start_elements = [
                        ['324', start_date, '102']  # Composite: 324:YYYYMMDD:102
                    ]
                    segments.append(seg("DTM", dtm_start_elements, s))
            
            # Calendar period - end date  
            end_date = calendar.get('end_date', '')
            if end_date:
                # Convert YYYYMMDD to YYYYMMDD format if needed
                if len(end_date) == 8 and end_date.isdigit():
                    # DTM+325:<YYYYMMDD>:102' (composite!)
                    dtm_end_elements = [
                        ['325', end_date, '102']  # Composite: 325:YYYYMMDD:102
                    ]
                    segments.append(seg("DTM", dtm_end_elements, s))
            
            # Optional FTX for day-of-week pattern
            dow_pattern = [
                calendar.get('monday', False),
                calendar.get('tuesday', False), 
                calendar.get('wednesday', False),
                calendar.get('thursday', False),
                calendar.get('friday', False),
                calendar.get('saturday', False),
                calendar.get('sunday', False)
            ]
            if any(dow_pattern):
                # Convert boolean array to string representation
                dow_bits = ''.join('1' if day else '0' for day in dow_pattern)
                # FTX+CDV+...+<dow_representation>' - TODO: adjust format per SKDUPD spec
                ftx_dow_elements = [
                    "CDV",      # Text subject qualifier - TODO: adjust per SKDUPD spec
                    "",         # Text function
                    "",         # Text reference  
                    dow_bits    # Day pattern (will be escaped if needed)
                ]
                segments.append(seg("FTX", ftx_dow_elements, s))
        
        # Process calls (stops) for this service
        calls = service.get('calls', [])
        for call in calls:
            station_uic = call.get('station_id', '')
            arr_time = call.get('arrival_time', '')
            dep_time = call.get('departure_time', '')
            day_offset = call.get('day_offset', 0)
            
            # LOC+92+<station_uic>'
            if station_uic:
                loc_elements = [
                    "92",       # Location qualifier - TODO: adjust per SKDUPD spec
                    station_uic # Station UIC
                ]
                segments.append(seg("LOC", loc_elements, s))
            
            # DTM for arrival time
            if arr_time:
                # Convert time format (remove colons, ensure HHMM or HHMMSS)
                arr_formatted = _format_time_for_dtm(arr_time)
                # DTM+132:<ARR_TIME>:105' (composite!)
                dtm_arr_elements = [
                    ['132', arr_formatted, '105']  # Composite: 132:time:105
                ]
                segments.append(seg("DTM", dtm_arr_elements, s))
            
            # DTM for departure time
            if dep_time:
                # Convert time format (remove colons, ensure HHMM or HHMMSS)
                dep_formatted = _format_time_for_dtm(dep_time)
                # DTM+133:<DEP_TIME>:105' (composite!)
                dtm_dep_elements = [
                    ['133', dep_formatted, '105']  # Composite: 133:time:105
                ]
                segments.append(seg("DTM", dtm_dep_elements, s))
            
            # Optional day offset information
            if day_offset and day_offset > 0:
                # DTM+997:<day_offset>:900' (composite!) - placeholder
                dtm_offset_elements = [
                    ['997', str(day_offset), '900']  # Composite: 997:offset:900
                ]
                segments.append(seg("DTM", dtm_offset_elements, s))
    
    return segments


def _format_time_for_dtm(time_str: str) -> str:
    """
    Format time string for DTM segments.
    Converts HH:MM:SS or HH:MM to HHMMSS or HHMM format.
    
    Args:
        time_str: Time in HH:MM:SS or HH:MM format
        
    Returns:
        Formatted time string without colons
    """
    if not time_str:
        return ""
    
    # Remove colons and return
    formatted = time_str.replace(':', '')
    
    # Ensure we have at least HHMM (4 digits)
    if len(formatted) < 4:
        formatted = formatted.ljust(4, '0')
    
    return formatted


def write_tsdupd(json_data: Dict[str, Any], *, version: str = "CURRENT", una: str = "UNA:+.? '") -> str:
    """
    Generate TSDUPD EDIFACT message from JSON input.
    
    Args:
        json_data: Input JSON data dictionary
        version: Version identifier for message type
        una: UNA service string advisory defining separators
        
    Returns:
        Complete TSDUPD EDIFACT message as string
        
    Raises:
        ValueError: If required data is missing or invalid
    """
    # Parse UNA to get separators
    if len(una) != 9 or not una.startswith('UNA'):
        raise ValueError(f"Invalid UNA string: {una}")
    
    s = Sep(
        comp=una[3],    # component separator
        elem=una[4],    # element separator  
        dec=una[5],     # decimal separator
        rel=una[6],     # release character
        seg=una[8]      # segment terminator
    )
    
    # Validate required data
    if 'stations' not in json_data:
        raise ValueError("Missing required 'stations' data")
    
    stations = json_data['stations']
    if not stations:
        raise ValueError("Stations list cannot be empty")
    
    publisher = json_data.get('publisher', {})
    
    # Generate deterministic references
    interchange_ref = generate_deterministic_ref(publisher, version)
    message_ref = interchange_ref + "01"  # Add message sequence
    
    # Get timestamp from publisher or use deterministic default
    fixed_timestamp = publisher.get('fixed_timestamp')
    timestamp = fixed_timestamp if fixed_timestamp else "240101:0000"
    
    # Build message
    segments = []
    
    # UNA (always include for proper separator definition)
    segments.append(una)
    
    # UNB - Interchange header
    sender_id = publisher.get('name', 'SENDER')[:35]  # Limit length
    receiver_id = "RECEIVER"  # TODO: Make configurable
    segments.append(make_unb(sender_id, receiver_id, interchange_ref, timestamp, s))
    
    # UNH - Message header
    segments.append(make_unh(message_ref, "TSDUPD", version, s))
    
    # Message body segments
    body_segments = map_tsdupd_segments(stations, s)
    segments.extend(body_segments)
    
    # UNT - Message trailer (count includes UNH and UNT)
    segment_count = len(body_segments) + 2
    segments.append(make_unt(segment_count, message_ref, s))
    
    # UNZ - Interchange trailer
    segments.append(make_unz(1, interchange_ref, s))
    
    return ''.join(segments)


def write_skdupd(json_data: Dict[str, Any], *, version: str = "CURRENT", una: str = "UNA:+.? '") -> str:
    """
    Generate SKDUPD EDIFACT message from JSON input.
    
    Args:
        json_data: Input JSON data dictionary
        version: Version identifier for message type
        una: UNA service string advisory defining separators
        
    Returns:
        Complete SKDUPD EDIFACT message as string
        
    Raises:
        ValueError: If required data is missing or invalid
    """
    # Parse UNA to get separators
    if len(una) != 9 or not una.startswith('UNA'):
        raise ValueError(f"Invalid UNA string: {una}")
    
    s = Sep(
        comp=una[3],    # component separator
        elem=una[4],    # element separator  
        dec=una[5],     # decimal separator
        rel=una[6],     # release character
        seg=una[8]      # segment terminator
    )
    
    # Validate required data
    if 'agencies' not in json_data:
        raise ValueError("Missing required 'agencies' data")
    if 'services' not in json_data:
        raise ValueError("Missing required 'services' data")
    
    agencies = json_data['agencies']
    services = json_data['services']
    
    if not agencies:
        raise ValueError("Agencies list cannot be empty")
    if not services:
        raise ValueError("Services list cannot be empty")
    
    publisher = json_data.get('publisher', {})
    
    # Generate deterministic references
    interchange_ref = generate_deterministic_ref(publisher, version)
    message_ref = interchange_ref + "01"  # Add message sequence
    
    # Get timestamp from publisher or use deterministic default
    fixed_timestamp = publisher.get('fixed_timestamp')
    timestamp = fixed_timestamp if fixed_timestamp else "240101:0000"
    
    # Build message
    segments = []
    
    # UNA (always include for proper separator definition)
    segments.append(una)
    
    # UNB - Interchange header
    sender_id = publisher.get('name', 'SENDER')[:35]  # Limit length
    receiver_id = "RECEIVER"  # TODO: Make configurable
    segments.append(make_unb(sender_id, receiver_id, interchange_ref, timestamp, s))
    
    # UNH - Message header
    segments.append(make_unh(message_ref, "SKDUPD", version, s))
    
    # Message body segments
    body_segments = map_skdupd_segments(agencies, services, s)
    segments.extend(body_segments)
    
    # UNT - Message trailer (count includes UNH and UNT)
    segment_count = len(body_segments) + 2
    segments.append(make_unt(segment_count, message_ref, s))
    
    # UNZ - Interchange trailer
    segments.append(make_unz(1, interchange_ref, s))
    
    return ''.join(segments)


def save_text(path: str, content: str) -> None:
    """
    Save EDIFACT content to file.
    
    Args:
        path: File path to save to
        content: EDIFACT content string
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)