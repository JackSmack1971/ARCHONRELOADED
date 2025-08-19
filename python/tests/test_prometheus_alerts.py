import asyncio
import pathlib
import shutil
import pytest

class PrometheusLintError(Exception):
    """Raised when Prometheus configuration validation fails."""

async def _run_promtool(args: list[str]) -> None:
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=30)
    except asyncio.TimeoutError as exc:
        process.kill()
        raise PrometheusLintError("promtool check timed out") from exc
    if process.returncode != 0:
        raise PrometheusLintError(stderr.decode())

@pytest.mark.asyncio
async def test_prometheus_config_syntax() -> None:
    if shutil.which("docker") is None:
        pytest.skip("Docker is required for promtool validation")
    root = pathlib.Path(__file__).resolve().parents[2] / "monitoring"
    await _run_promtool([
        "docker",
        "run",
        "--rm",
        "-v",
        f"{root}:/etc/prometheus",
        "prom/prometheus:latest",
        "promtool",
        "check",
        "config",
        "/etc/prometheus/prometheus.yml",
    ])
    await _run_promtool([
        "docker",
        "run",
        "--rm",
        "-v",
        f"{root}:/etc/prometheus",
        "prom/prometheus:latest",
        "promtool",
        "check",
        "rules",
        "/etc/prometheus/alerts.yml",
    ])
