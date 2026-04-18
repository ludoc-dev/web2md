#!/usr/bin/env python3
import json
import csv
import sys
from pathlib import Path

def analyze_locust_csv(csv_file):
    if not Path(csv_file).exists():
        print(f"⚠️  Arquivo {csv_file} não encontrado")
        return
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        data = list(reader)
    if not data:
        print("❌ Sem dados para analisar")
        return
    total_requests = len(data)
    failures = sum(1 for row in data if row['Success'] == 'False')
    success_rate = (total_requests - failures) / total_requests * 100 if total_requests > 0 else 0
    response_times = [int(row['Request Count']) for row in data if row['Request Count'].isdigit()]
    avg_response = sum(response_times) / len(response_times) if response_times else 0
    print("📊 Performance Analysis")
    print("=" * 50)
    print(f"Total Requests: {total_requests}")
    print(f"Failures: {failures}")
    print(f"Success Rate: {success_rate:.2f}%")
    print(f"Avg Response Time: {avg_response:.2f}ms")
    print("=" * 50)
    if success_rate < 95:
        print("⚠️  ALERT: Success rate abaixo de 95%")
    if avg_response > 5000:
        print("⚠️  ALERT: Response time acima de 5s")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: analyze-performance.py <locust.csv>")
        sys.exit(1)
    analyze_locust_csv(sys.argv[1])
