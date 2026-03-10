"""Request trace ID generation."""
import uuid


def generate_trace_id() -> str:
    """Generate a trace ID in TRACE-xxx format."""
    return f"TRACE-{uuid.uuid4().hex[:12].upper()}"
