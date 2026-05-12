import logging
import time
from datetime import datetime
from src.config import get_config
from src.logger import setup_logger
from src.api.mikrotik_client import MikroTikClient
from src.parser.log_parser import LogParser
from src.detection.anomaly_detector import AnomalyDetector
from src.detection.brute_force_detector import BruteForceDetector
from src.exceptions import APIConnectionError, APITimeoutError, BlockingError


logger = setup_logger("engine")

class TMECore:
    def __init__(self):
        config = get_config()
        self.config = config
        
        logger.info("Initializing TME-CORE modules...")
        
        log_file_ssh = config.get('detection', {}).get('log_file_ssh', 'data/logs/514MikroTik.log')
        
        # Initialize modules
        self.api = MikroTikClient(**config['mikrotik'])
        self.parser = LogParser(log_file_ssh)
        
        # Jalur A
        self.detector = BruteForceDetector(
            threshold=config['detection']['brute_force']['threshold'],
            window_seconds=config['detection']['brute_force']['window_seconds']
        )
        
        # JALUR B
        self.detector_anomaly = AnomalyDetector(
            cpu_spike_threshold=config['detection']['anomaly'].get('cpu_spike_threshold', 30),
            window_seconds=config['detection']['anomaly'].get('window_seconds', 60)
        )
        
        self.blocked_ips = set()
        self.metrics = []
        
        logger.info("✅ All modules initialized")
    
    def start(self):
        """Start engine daemon dengan proper error handling"""
        logger.info("🚀 TME-CORE Engine Starting")
        
        try:
            # Connect to API dengan retry
            logger.info("Connecting to MikroTik API...")
            retry_count = 0
            max_retries = 3
            
            while retry_count < max_retries:
                try:
                    self.api.connect()
                    logger.info("✅ API connected")
                    break
                except APIConnectionError as e:
                    retry_count += 1
                    wait_time = 2 ** retry_count  # Exponential backoff
                    logger.warning(f"⚠️ Connection failed (attempt {retry_count}/{max_retries}), retry in {wait_time}s...")
                    if retry_count >= max_retries:
                        raise APIConnectionError(f"Failed to connect after {max_retries} attempts: {e}")
                    time.sleep(wait_time)
            
            # Open log parser
            try:
                self.parser.open()
                logger.info("✅ Log parser opened")
            except Exception as e:
                logger.error(f"❌ Failed to open log parser: {e}")
                raise
            
            # Main loop dengan error handling per event
            logger.info("📡 Listening for events...")
            consecutive_errors = 0
            max_consecutive_errors = 10
            
            for event in self.parser.stream_events():
                logger.debug(f"Event: {event.source_ip} → {event.result}")
                
                # ✅ JALUR A
                is_bf_threat = self.detector.process_event(event)
                
                # ✅ JALUR B - Sample CPU dan check anomaly
                try:
                    cpu_info = self.api.get_router_cpu()
                    self.detector_anomaly.add_cpu_sample(cpu_info['cpu_load'])
                    is_anomaly = self.detector_anomaly.process_login_event(event, cpu_info['cpu_load'])
                except Exception as e:
                    logger.debug(f"Anomaly check error: {e}")
                    is_anomaly = False
                
                # ✅ Combined threat decision
                is_threat = is_bf_threat or is_anomaly
                
                if is_threat and event.source_ip not in self.blocked_ips:
                        try:
                            # BLOCK IP dengan error handling
                            logger.warning(f"🚨 THREAT: {event.source_ip} - BLOCKING...")
                            
                            start_time = time.time()
                            self.api.block_ip(event.source_ip)
                            response_time = (time.time() - start_time) * 1000
                            
                            self.blocked_ips.add(event.source_ip)
                            
                            # Get CPU
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
                            
                            logger.info(f"✅ BLOCKED: {event.source_ip} (response: {response_time:.2f}ms)")
                            consecutive_errors = 0  # Reset on success
                            
                        except APITimeoutError as e:
                            logger.error(f"❌ API timeout saat blocking {event.source_ip}: {e}")
                            # Don't mark as blocked, retry next time
                            consecutive_errors += 1
                        except BlockingError as e:
                            logger.error(f"❌ Blocking failed untuk {event.source_ip}: {e}")
                            consecutive_errors += 1
                        
                        # Check if too many errors
                        if consecutive_errors >= max_consecutive_errors:
                            raise Exception(f"Too many consecutive blocking errors ({consecutive_errors})")
                    
        except Exception as e:
            logger.warning(f"⚠️ Error processing event: {e}")
            consecutive_errors += 1
        except KeyboardInterrupt:
            logger.info("\n⏹️ Shutdown signal received")
        except APIConnectionError as e:
            logger.error(f"❌ Critical API error: {e}")
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}", exc_info=True)
        
        finally:
            logger.info("Cleaning up...")
            try:
                self.parser.close()
                self.api.disconnect()
            except Exception as e:
                logger.warning(f"⚠️ Cleanup error: {e}")
            
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