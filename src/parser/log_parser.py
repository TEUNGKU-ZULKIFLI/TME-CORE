import re
from datetime import datetime
from dataclasses import dataclass
from typing import Iterator
import logging

logger = logging.getLogger(__name__)

@dataclass
class LoginEvent:
    timestamp: datetime
    source_ip: str
    username: str
    service: str  # 'ssh' or 'ftp'
    result: str   # 'failure' or 'success'

class LogParser:
    def __init__(self, log_file_path: str):
        self.log_file = log_file_path
        self.file_handle = None
        # SSH pattern: "login failure for user admin from 192.168.20.2"
        self.ssh_pattern = r'login failure for user (\w+) from ([\d.]+)'
        # FTP pattern: (akan ditambah kemudian)
        self.ftp_pattern = r'([\d.]+).*LOGIN FAILED'
    
    def open(self):
        """Open log file for streaming"""
        self.file_handle = open(self.log_file, 'r')
        # Seek to end of file untuk new events only
        self.file_handle.seek(0, 2)
        logger.info(f"✓ Log parser opened: {self.log_file}")
    
    def close(self):
        """Close log file"""
        if self.file_handle:
            self.file_handle.close()
            logger.info("✓ Log parser closed")
    
    def stream_events(self) -> Iterator[LoginEvent]:
        """Stream new log events real-time"""
        if not self.file_handle:
            self.open()
        
        while True:
            line = self.file_handle.readline()
            
            if not line:
                # No new lines, wait & retry
                import time
                time.sleep(0.1)
                continue
            
            # Parse line
            event = self._parse_line(line)
            if event:
                yield event
    
    def _parse_line(self, line: str) -> LoginEvent:
        """Parse single log line"""
        try:
            # Format: 2026-05-09T03:52:38.806409-07:00 192.168.10.1 system,error,critical login failure for user admin from 192.168.20.2 via ssh
            
            # Extract timestamp
            timestamp_str = line.split(' ')[0]
            timestamp = datetime.fromisoformat(timestamp_str.replace('-07:00', '+00:00'))
            
            # Try SSH pattern
            match = re.search(self.ssh_pattern, line)
            if match:
                username = match.group(1)
                source_ip = match.group(2)
                return LoginEvent(
                    timestamp=timestamp,
                    source_ip=source_ip,
                    username=username,
                    service='ssh',
                    result='failure'
                )
            
            # Try FTP pattern (future)
            # ... (similar for FTP)
            
            return None
        
        except Exception as e:
            logger.error(f"Parse error: {e}")
            return None


# Test
if __name__ == "__main__":
    parser = LogParser('/home/teungku/TME-CORE/data/logs/514MikroTik.log')
    parser.open()
    
    count = 0
    for event in parser.stream_events():
        print(f"Event: {event.source_ip} → {event.result}")
        count += 1
        if count >= 10:  # Stop after 10 events for test
            break
    
    parser.close()