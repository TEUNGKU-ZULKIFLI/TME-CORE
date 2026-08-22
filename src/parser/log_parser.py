import re
from typing import Dict, Any, Optional, List

def parse_single_log(log_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    message = log_item.get('message', '')
    log_id = log_item.get('id', '')
    timestamp = log_item.get('time', '')

    pattern_success = r"user\s+(?P<username>\S+)\s+logged in from\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+via\s+(?P<service>\S+)"
    match_success = re.search(pattern_success, message)

    if match_success:
        return {
            'log_id': log_id,
            'timestamp': timestamp,
            'username': match_success.group('username'),
            'ip': match_success.group('ip'),
            'service': match_success.group('service').lower(),
            'status': 'SUCCESS',
            'raw_message': message
        }

    pattern_failed = r"login failure for user\s+(?P<username>\S+)\s+from\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+via\s+(?P<service>\S+)"
    match_failed = re.search(pattern_failed, message)

    if match_failed:
        return {
            'log_id': log_id,
            'timestamp': timestamp,
            'username': match_failed.group('username'),
            'ip': match_failed.group('ip'),
            'service': match_failed.group('service').lower(),
            'status': 'FAILED',
            'raw_message': message
        }

    return None

def fetch_and_parse_logs(api_connection) -> List[Dict[str, Any]]:
    parsed_results = []
    try:
        raw_logs = api_connection.get_resource('/log').get()
        for log in raw_logs:
            parsed_data = parse_single_log(log)
            if parsed_data:
                parsed_results.append(parsed_data)
    except Exception as e:
        print(f"[✗] Error saat mengambil log dari API: {e}")
        
    return parsed_results
