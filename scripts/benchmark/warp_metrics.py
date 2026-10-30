"""Conservative parser for Warp analyze --json; unsupported schemas fail closed."""
import math

def numeric(x):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x<0:
        raise ValueError("Invalid metric")
    return float(x)

def extract_metrics(data):
    """Accept only explicit normalized summary metrics; never infer percentiles from unrelated fields.

    Real Warp JSON schema may differ by release. Unsupported structures raise ValueError.
    """
    if not isinstance(data,dict):raise ValueError("Warp JSON must be object")
    # Schema adapters are intentionally explicit and version independent.
    if all(k in data for k in ("ops_per_second","throughput_mib_s","latency_ms")):
        lat=data["latency_ms"]
        if not isinstance(lat,dict) or not all(k in lat for k in ("p50","p95","p99")):
            raise ValueError("Missing latency percentiles")
        return {"ops_per_second":numeric(data["ops_per_second"]),
                "throughput_mib_s":numeric(data["throughput_mib_s"]),
                "p50_ms":numeric(lat["p50"]),"p95_ms":numeric(lat["p95"]),
                "p99_ms":numeric(lat["p99"])}
    raise ValueError("Unrecognized Warp JSON schema; preserve raw analyze output and add tested adapter")
