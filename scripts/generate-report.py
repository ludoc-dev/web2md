#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime

def generate_html_report():
    pipeline_id = os.getenv("CI_PIPELINE_ID", "unknown")
    pipeline_url = os.getenv("CI_PIPELINE_URL", "#")
    commit_sha = os.getenv("CI_COMMIT_SHORT_SHA", "unknown")
    branch = os.getenv("CI_COMMIT_REF_NAME", "unknown")
    
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>web2md Test Report</title>
</head>
<body>
    <h1>web2md Test Report</h1>
    <p>Pipeline: <a href="{pipeline_url}">#{pipeline_id}</a></p>
    <p>Commit: {commit_sha} | Branch: {branch}</p>
    <p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</body>
</html>"""
    
    output_file = reports_dir / "final-report.html"
    output_file.write_text(html)
    print(f"✅ Relatório gerado: {output_file}")

if __name__ == "__main__":
    generate_html_report()
