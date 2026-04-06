import typer
from pathlib import Path
import json

from .capture import run_and_capture
from .diff import explain_drift

app = typer.Typer(
    name="drift",
    help="ML Training Drift Forensics CLI - Tell you why your training changed."
)

@app.command()
def run(
    command: str = typer.Argument(..., help="Command to execute, e.g. 'python train.py --epochs 5'"),
    label: str = typer.Option("default", help="Label for this run"),
    output_dir: str = typer.Option("runs", help="Directory to save artifacts")
):
    """Execute training and capture full environment + metrics for forensics."""
    typer.echo(f"🚀 Starting drift capture: {command}")
    run_data = run_and_capture(command, label=label, output_dir=output_dir)
    typer.echo(f"✅ Captured run: {run_data['run_id']}")
    typer.echo(f"   Artifact: runs/run_{run_data['run_id']}.json")

@app.command()
def diff(
    run_a: str = typer.Argument(..., help="Path to first run JSON"),
    run_b: str = typer.Argument(..., help="Path to second run JSON"),
    tolerance: float = typer.Option(1e-4, help="Metric tolerance threshold")
):
    """Compare two runs and explain why they differ (forensic report)."""
    if not Path(run_a).exists() or not Path(run_b).exists():
        typer.echo("❌ One or both run files not found.")
        raise typer.Exit(code=1)
    
    typer.echo("🧪 Analyzing drift...")
    report = explain_drift(run_a, run_b, tolerance=tolerance)
    
    # 簡單 summary
    critical = sum(1 for f in report.get("findings", []) if "CRITICAL" in f.get("priority", ""))
    high = sum(1 for f in report.get("findings", []) if "HIGH" in f.get("priority", ""))
    
    typer.echo(f"\n📊 Summary: {len(report.get('findings', []))} findings "
               f"({critical} critical, {high} high priority)")

@app.command()
def inspect(
    path: str = typer.Argument(..., help="Path to run JSON artifact")
):
    """Pretty-print a single run artifact."""
    if not Path(path).exists():
        typer.echo("❌ File not found.")
        raise typer.Exit(code=1)
    
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    
    typer.echo(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    app()

@app.command()
def patch(
    baseline: str = typer.Argument(...),
    output: str = typer.Option("drift_patch.py")
):
    """Generate environment alignment patch"""
    from .patcher import generate_patch
    generate_patch(baseline, output)
