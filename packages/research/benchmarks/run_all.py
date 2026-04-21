"""Benchmark runner for Hymoex -- runs all 4 benchmark categories and prints a summary table.

Usage:
    uv run python packages/research/benchmarks/run_all.py
"""

import os
import re
import subprocess
import sys
from pathlib import Path

BENCHMARKS_DIR = Path(__file__).parent
REPO_ROOT = BENCHMARKS_DIR.parent.parent.parent
CORE_DIR = REPO_ROOT / "packages" / "hymoex-python"

CATEGORIES: list[tuple[str, str]] = [
    ("Coordination Overhead", "coordination-overhead"),
    ("Expert Selection", "expert-selection"),
    ("Scalability", "scalability"),
    ("Migration Cost", "migration-cost"),
]

# Patterns to extract key metrics from pytest output
METRIC_PATTERNS: dict[str, list[tuple[str, re.Pattern[str]]]] = {
    "coordination-overhead": [
        ("Flat MAS tokens", re.compile(r"Flat MAS.*?:\s*(\d+)\s*coordination tokens")),
        ("Single Supervisor tokens", re.compile(r"Single Supervisor.*?:\s*(\d+)\s*coordination tokens")),
        ("M2 config size", re.compile(r"Hymoex M2.*?config size\s*=\s*(\d+)\s*chars")),
    ],
    "expert-selection": [
        ("MoE Gating accuracy", re.compile(r"MoE Gating Accuracy:\s*([\d.]+)%")),
        ("Rule-based accuracy", re.compile(r"Rule-based Accuracy:\s*([\d.]+)%")),
        ("Random accuracy", re.compile(r"Random Accuracy:\s*([\d.]+)%")),
        ("Round-robin accuracy", re.compile(r"Round-robin Accuracy:\s*([\d.]+)%")),
    ],
    "scalability": [
        ("2 experts latency", re.compile(r"2 experts.*?:\s*([\d.]+)ms")),
        ("5 experts latency", re.compile(r"5 experts.*?:\s*([\d.]+)ms")),
        ("10 experts latency", re.compile(r"10 experts.*?:\s*([\d.]+)ms")),
        ("15 experts latency", re.compile(r"15 experts.*?:\s*([\d.]+)ms")),
        ("Degradation", re.compile(r"Degradation:\s*([\d.]+)%")),
    ],
    "migration-cost": [
        ("M1->M2 preservation", re.compile(r"M1.*?M2:\s*([\d.]+)%\s*preservation")),
        ("M2->M3 preservation", re.compile(r"M2.*?M3:\s*([\d.]+)%\s*preservation")),
    ],
}


def run_benchmark(name: str, subdir: str) -> tuple[bool, str, dict[str, str]]:
    """Run a single benchmark category via pytest.

    Returns (passed, raw_output, extracted_metrics).
    """
    test_dir = BENCHMARKS_DIR / subdir
    if not test_dir.exists():
        return False, f"Directory not found: {test_dir}", {}

    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            str(test_dir), "-v", "-s",
            "--override-ini=addopts=",
            "--tb=short",
        ],
        capture_output=True,
        text=True,
        cwd=str(CORE_DIR),
        timeout=120,
    )

    output = result.stdout + result.stderr
    passed = result.returncode == 0

    # Extract metrics using category-specific patterns
    metrics: dict[str, str] = {}
    patterns = METRIC_PATTERNS.get(subdir, [])
    for metric_name, pattern in patterns:
        match = pattern.search(output)
        if match:
            metrics[metric_name] = match.group(1)

    # Count test results
    n_passed = len(re.findall(r"PASSED", output))
    n_failed = len(re.findall(r"FAILED", output))
    metrics["_tests"] = f"{n_passed} passed" + (f", {n_failed} failed" if n_failed else "")

    return passed, output, metrics


def print_summary_table(results: dict[str, tuple[bool, dict[str, str]]]) -> None:
    """Print a formatted summary table matching the paper's Table 3 format."""
    w = 72
    print("\n" + "=" * w)
    print("  HYMOEX BENCHMARK RESULTS (Table 3)")
    print("=" * w)

    # --- Table 3a: Coordination Overhead ---
    metrics = results.get("coordination-overhead", (False, {}))[1]
    if metrics:
        print(f"\n  Table 3a: Coordination Overhead (tokens per task)")
        print(f"  {'Topology':<34} {'Tokens':>10}")
        print(f"  {'-' * 46}")
        for label in ["Flat MAS tokens", "Single Supervisor tokens", "M2 config size"]:
            val = metrics.get(label, "N/A")
            print(f"  {label:<34} {val:>10}")

    # --- Table 3b: Expert Selection Accuracy ---
    metrics = results.get("expert-selection", (False, {}))[1]
    if metrics:
        print(f"\n  Table 3b: Expert Selection Accuracy")
        print(f"  {'Method':<34} {'Accuracy':>10}")
        print(f"  {'-' * 46}")
        for label in ["MoE Gating accuracy", "Rule-based accuracy",
                       "Random accuracy", "Round-robin accuracy"]:
            val = metrics.get(label, "N/A")
            suffix = "%" if val != "N/A" else ""
            print(f"  {label:<34} {val + suffix:>10}")

    # --- Table 3c: Scalability ---
    metrics = results.get("scalability", (False, {}))[1]
    if metrics:
        print(f"\n  Table 3c: Scalability (avg latency, mock provider)")
        print(f"  {'Configuration':<34} {'Latency':>10}")
        print(f"  {'-' * 46}")
        for label in ["2 experts latency", "5 experts latency",
                       "10 experts latency", "15 experts latency"]:
            val = metrics.get(label, "N/A")
            suffix = " ms" if val != "N/A" else ""
            print(f"  {label:<34} {val + suffix:>10}")
        deg = metrics.get("Degradation", "N/A")
        deg_suffix = "%" if deg != "N/A" else ""
        print(f"  {'2->10 agent degradation':<34} {deg + deg_suffix:>10}")

    # --- Table 3d: Migration Cost ---
    metrics = results.get("migration-cost", (False, {}))[1]
    if metrics:
        print(f"\n  Table 3d: Migration Cost (agent preservation)")
        print(f"  {'Transition':<34} {'Preserved':>10}")
        print(f"  {'-' * 46}")
        for label in ["M1->M2 preservation", "M2->M3 preservation"]:
            val = metrics.get(label, "N/A")
            suffix = "%" if val != "N/A" else ""
            print(f"  {label:<34} {val + suffix:>10}")

    # --- Overall status ---
    print(f"\n  {'='*46}")
    print(f"  {'Category':<34} {'Status':>10}")
    print(f"  {'-' * 46}")
    for cat_name, subdir in CATEGORIES:
        passed, metrics = results.get(subdir, (False, {}))
        status = "PASS" if passed else "FAIL"
        tests = metrics.get("_tests", "")
        print(f"  {cat_name:<34} {status:>10}  {tests}")

    print("\n" + "=" * w)


def main() -> int:
    """Run all benchmarks and print results."""
    print("=" * 72)
    print("  HYMOEX BENCHMARK SUITE")
    print("=" * 72)
    print(f"\n  Benchmark dir: {BENCHMARKS_DIR}")
    print(f"  Core dir:      {CORE_DIR}\n")

    results: dict[str, tuple[bool, dict[str, str]]] = {}
    all_passed = True

    for name, subdir in CATEGORIES:
        print(f"  [{name}] running...", end=" ", flush=True)
        passed, output, metrics = run_benchmark(name, subdir)
        results[subdir] = (passed, metrics)

        if passed:
            print(f"PASS ({len(metrics) - 1} metrics extracted)")
        else:
            print("FAIL")
            all_passed = False
            for line in output.splitlines():
                if "FAILED" in line or "ERROR" in line:
                    print(f"    {line.strip()}")

    print_summary_table(results)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
