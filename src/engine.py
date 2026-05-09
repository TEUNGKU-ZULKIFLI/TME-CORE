import logging
import time
from datetime import datetime

from src.config import get_config
from src.logger import setup_logger
from src.api.mikrotik_client import MikroTikClient
from src.parser.log_parser import LogParser
from src.detection.brute_force_detector import BruteForceDetector

logger = setup_logger("engine")

class TMECore:
    def __init__(self):
        config = get_config()
        self.config = config
        
        logger.info("Initializing TME-CORE modules...")
        
        # Get log file path dari config
        log_file_ssh = config.get('detection', {}).get('log_file_ssh', 'data/logs/514MikroTik.log')
        
        # Initialize modules
        self.api = MikroTikClient(**config['mikrotik'])
        self.parser = LogParser(log_file_ssh)  # ✅ USE FROM CONFIG
        self.detector = BruteForceDetector(
            threshold=config['detection']['brute_force']['threshold'],
            window_seconds=config['detection']['brute_force']['window_seconds']
        )
        
        self.blocked_ips = set()
        self.metrics = []
        
        logger.info("✅ All modules initialized")
    
    def start(self):
        """Start engine daemon"""
        logger.info("=" * 60)
        logger.info("🚀 TME-CORE Engine Starting")
        logger.info("=" * 60)
        
        try:
            # Connect to API
            logger.info("Connecting to MikroTik API...")
            self.api.connect()
            logger.info("✅ API connected")
            
            # Open log parser
            self.parser.open()
            logger.info("✅ Log parser opened")
            
            # Main loop
            logger.info("📡 Listening for events...")
            
            for event in self.parser.stream_events():
                logger.debug(f"Event: {event.source_ip} → {event.result} ({event.service})")
                
                # Detect threat
                is_threat = self.detector.process_event(event)
                
                if is_threat and event.source_ip not in self.blocked_ips:
                    # BLOCK IP
                    logger.warning(f"🚨 THREAT: {event.source_ip} - BLOCKING...")
                    
                    start_time = time.time()
                    self.api.block_ip(event.source_ip)
                    response_time = (time.time() - start_time) * 1000
                    
                    self.blocked_ips.add(event.source_ip)
                    
                    # Get CPU at time of block
                    cpu_info = self.api.get_router_cpu()
                    
                    # Record metric
                    metric = {
                        'timestamp': event.timestamp,
                        'source_ip': event.source_ip,
                        'event_type': 'brute_force',
                        'action': 'BLOCK',
                        'response_time_ms': response_time,
                        'router_cpu_percent': cpu_info['cpu_load']
                    }
                    self.metrics.append(metric)
                    
                    logger.info(f"✅ BLOCKED: {event.source_ip} (response: {response_time:.2f}ms, CPU: {cpu_info['cpu_load']}%)")
        
        except KeyboardInterrupt:
            logger.info("\n⏹️ Shutdown signal received")
        
        except Exception as e:
            logger.error(f"❌ Error: {e}", exc_info=True)
        
        finally:
            logger.info("Cleaning up...")
            self.parser.close()
            self.api.disconnect()
            
            # Save metrics
            self._save_metrics()
            
            logger.info("✅ Shutdown complete")
    
    def _save_metrics(self):
        """Save metrics to CSV"""
        import csv
        
        csv_path = 'data/metrics/engine_metrics.csv'
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'source_ip', 'event_type', 'action', 'response_time_ms', 'router_cpu_percent'])
            writer.writeheader()
            writer.writerows(self.metrics)
        
        logger.info(f"✅ Metrics saved: {csv_path} ({len(self.metrics)} events)")

if __name__ == "__main__":
    engine = TMECore()
    engine.start()