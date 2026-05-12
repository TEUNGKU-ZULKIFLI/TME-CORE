"""
Configuration management untuk TME-CORE
Load config dari environment variables atau YAML file
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any

# Local imports
from src.exceptions import ConfigError
from src.logger import setup_logger

logger = setup_logger(__name__)


def load_config_from_env() -> Dict[str, Any]:
    """
    Load configuration dari environment variables (.env file)

    Returns:
        Dictionary dengan konfigurasi

    Raises:
        ConfigError jika required variables tidak ditemukan
    """
    # Load .env file
    env_path = Path(__file__).parent.parent / "config" / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(f"✓ Loaded .env from {env_path}")
    else:
        logger.warning(f"⚠ .env file not found at {env_path}, using system env vars")

    # Define required variables
    required_vars = {
        'MIKROTIK_HOST': '192.168.10.1',
        'MIKROTIK_USERNAME': 'admin',
        'MIKROTIK_PASSWORD': '',  # HARUS ada di .env
        'MIKROTIK_PORT': '8728',
    }

    # Load dari environment
    config_env = {}
    for key, default in required_vars.items():
        value = os.getenv(key, default)
        if key == 'MIKROTIK_PASSWORD' and not value:
            raise ConfigError(f"Missing required env var: {key}")
        config_env[key] = value

    return config_env


def load_config_from_yaml(yaml_path: str = None) -> Dict[str, Any]:
    """
    Load configuration dari YAML file

    Args:
        yaml_path: Path ke YAML file (default: config/app_config.yaml)

    Returns:
        Dictionary dengan konfigurasi

    Raises:
        ConfigError jika file tidak ditemukan atau invalid YAML
    """
    if yaml_path is None:
        yaml_path = Path(__file__).parent.parent / "config" / "app_config.yaml"
    else:
        yaml_path = Path(yaml_path)

    if not yaml_path.exists():
        raise ConfigError(f"Config file not found: {yaml_path}")

    try:
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"✓ Loaded YAML config from {yaml_path}")
        return config
    except yaml.YAMLError as e:
        raise ConfigError(f"Invalid YAML file: {e}")
    except Exception as e:
        raise ConfigError(f"Error reading config file: {e}")


def get_config() -> Dict[str, Any]:
    """
    Load config dengan priority:
    1. Load YAML file (defaults)
    2. Load .env file (secrets & overrides)
    3. Validate all required fields
    4. Return merged config
    
    Example:
        config = get_config()
        print(config['mikrotik']['password'])  # From .env
    """
    try:
        # STEP 1: Load YAML (structure & defaults)
        try:
            yaml_config = load_config_from_yaml()
        except ConfigError:
            logger.warning("YAML config not found, using minimal defaults")
            yaml_config = {
                'app': {'name': 'TME-CORE', 'version': '1.0.0'},
                'mikrotik': {
                    'host': '192.168.10.1',
                    'username': 'admin',
                    'port': 8728,
                    'timeout': 10
                },
                'detection': {
                    'log_file_ssh': '/home/teungku/TME-CORE/data/logs/514MikroTik.log',
                    'brute_force': {'threshold': 10, 'window_seconds': 60},
                    'anomaly': {'cpu_spike_threshold': 30, 'window_seconds': 60}
                }
            }
        
        # STEP 2: Load .env (secrets & production overrides)
        env_vars = load_config_from_env()
        
        # STEP 3: Override YAML dengan ENV (ENV has priority!)
        yaml_config['mikrotik']['host'] = env_vars.get('MIKROTIK_HOST')
        yaml_config['mikrotik']['username'] = env_vars.get('MIKROTIK_USERNAME')
        yaml_config['mikrotik']['password'] = env_vars.get('MIKROTIK_PASSWORD')  # FROM ENV!
        yaml_config['mikrotik']['port'] = int(env_vars.get('MIKROTIK_PORT', '8728'))
        
        # STEP 4: Validate critical fields
        validate_config(yaml_config)
        
        logger.info("✓ Configuration loaded successfully (YAML + ENV merged)")
        return yaml_config
    
    except Exception as e:
        logger.error(f"✗ Failed to load configuration: {e}")
        raise ConfigError(f"Config error: {e}")


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration - STRICT!
    
    Raises: ConfigError if any required field missing
    """
    required = {
        'mikrotik': ['host', 'username', 'password', 'port'],
        'detection': ['log_file_ssh', 'brute_force', 'anomaly']
    }
    
    for section, keys in required.items():
        if section not in config:
            raise ConfigError(f"❌ Missing config section: [{section}]")
        
        for key in keys:
            if key not in config[section]:
                raise ConfigError(f"❌ Missing config [{section}].{key}")
            
            # Special: password MUST come from .env (never empty!)
            if key == 'password' and not config[section][key]:
                raise ConfigError(f"❌ MIKROTIK_PASSWORD not set in .env! (required)")
    
    logger.info("✓ Configuration validated - all required fields present")
    return True


# Contoh penggunaan:
# if __name__ == "__main__":
#     try:
#         config = get_config()
#         validate_config(config)
#         print(config)
#     except ConfigError as e:
#         print(f"Config error: {e}")