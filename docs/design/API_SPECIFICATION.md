# API Specification - MikroTik Integration

## 1. Connection Parameters

```yaml
Protocol: RouterOS API (TCP)
Host: 192.168.10.1
Port: 8728
Username: admin
Password: (from .env)
Plaintext login: true
```

## 2. Core Methods

### 2.1 `block_ip(source_ip: str) → dict`

**Purpose:** Add attacker IP to address-list dan trigger firewall DROP

**Implementation:**
```python
def block_ip(self, source_ip: str, list_name: str = "brute_force_block") → dict:
    # 1. Get address-list resource
    # 2. Add entry: {list: brute_force_block, address: source_ip}
    # 3. Return: {success: bool, response_time_ms: float}
```

**MikroTik Commands:**
```mikrotik
/ip firewall address-list
add list=brute_force_block address=192.168.20.2 comment="Auto-blocked by TME-CORE"
```

**Response Example:**
```json
{
  "success": true,
  "source_ip": "192.168.20.2",
  "list_name": "brute_force_block",
  "response_time_ms": 7.03,
  "timestamp": "2026-05-09T08:00:04Z"
}
```

### 2.2 `unblock_ip(source_ip: str) → dict`

**Purpose:** Remove IP dari address-list (untuk auto-unblocking)

**MikroTik Commands:**
```mikrotik
/ip firewall address-list
remove [find address=192.168.20.2 list=brute_force_block]
```

### 2.3 `get_router_cpu() → dict`

**Purpose:** Get real-time CPU metrics untuk Anomaly Detection (Jalur B)

**Response Example:**
```json
{
  "cpu_load": 45,
  "cpu_count": 1,
  "free_memory_mb": 41000,
  "total_memory_mb": 64000,
  "uptime_seconds": 28800
}
```

## 3. Data Models

### LoginEvent
```python
@dataclass
class LoginEvent:
    timestamp: datetime
    source_ip: str
    username: str
    service: str  # 'ssh' | 'ftp'
    result: str   # 'success' | 'failure'
```

### BlockingEvent
```python
@dataclass
class BlockingEvent:
    timestamp: datetime
    source_ip: str
    threat_type: str  # 'brute_force' | 'anomaly'
    action: str       # 'BLOCK'
    response_time_ms: float
    router_cpu_percent: int
    blocked_ips_count: int
```

## 4. Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `ConnectionError` | API unreachable | Retry (exponential backoff) |
| `AuthError` | Invalid credentials | Check .env, abort |
| `AddressListFull` | Max entries | Clean old entries |
| `APITimeout` | Slow response | Log warning, continue |

## 5. Performance Metrics

- **API Connection Time:** <500ms
- **Block Action Time:** 5-10ms
- **Unblock Action Time:** 5-10ms
- **Get CPU Time:** 2-5ms
- **Throughput:** 100+ operations/second