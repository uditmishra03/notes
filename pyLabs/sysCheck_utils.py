#!/usr/bin/env python3
import argparse
import re
import sys
import psutil
import time

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3


def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--cpu-warn", type=float, default=75.0)
    p.add_argument("--cpu-crit", type=float, default=90.0)
    p.add_argument("--mem-warn", type=float, default=75.0)
    p.add_argument("--mem-crit", type=float, default=90.0)
    p.add_argument("--include", type=str, default="cpu,mem")
    p.add_argument("--interval", type=float, default=1.0)
    return p


def validate_args(args):
    """
    Validates command-line arguments for system monitoring thresholds and configuration.
    
    Checks that CPU and memory warning/critical thresholds are valid percentages (0-100),
    that warning thresholds are less than critical thresholds, that the monitoring interval
    is positive, and that the include parameter contains valid and non-duplicate metrics.
    
    Args:
        args: An object with attributes cpu_warn, cpu_crit, mem_warn, mem_crit, interval,
              and include (typically from argparse).
    
    Returns:
        tuple: A tuple of (is_valid, error_message) where is_valid is a boolean indicating
               whether all validations passed, and error_message is a string describing the
               first validation error encountered (empty string if valid).
    
    Raises:
        None
    
    Examples:
        >>> # Assuming args object with valid values
        >>> is_valid, msg = validate_args(args)
        >>> if is_valid:
        ...     print("Arguments are valid")
    """
    for name in ("cpu_warn", "cpu_crit", "mem_warn", "mem_crit"):
        v = getattr(args, name)
        if v < 0 or v > 100:
            return False, name + " must be between 0 and 100"
    if args.cpu_warn >= args.cpu_crit:
        return False, "cpu-warn must be less than cpu-crit"
    if args.mem_warn >= args.mem_crit:
        return False, "mem-warn must be less than mem-crit"
    if args.interval <= 0:
        return False, "interval must be > 0"
    if not re.fullmatch(r"^(cpu|mem)(,(cpu|mem))*$", args.include):
        return False, "include must be cpu, mem, cpu,mem or mem,cpu (no spaces)"
    parts = args.include.split(",")
    if len(set(parts)) != len(parts):
        return False, "include must not contain duplicates"
    return True, ""


def cpu_percent(interval):
    usage = psutil.cpu_percent(interval=interval)
    if usage < 0:
        usage = 0.0
    if usage > 100:
        usage = 100.0
    return float(usage)


def mem_percent():
    usage = psutil.virtual_memory().percent
    if usage < 0:
        usage = 0.0
    if usage > 100:
        usage = 100.0
    return float(usage)


def collect_metrics(include, interval):
    out = {}
    if "cpu" in include:
        out["cpu"] = cpu_percent(interval)
    if "mem" in include:
        out["mem"] = mem_percent()
    return out


def evaluate(metrics, args):
    code = OK
    if "cpu" in metrics:
        v = metrics["cpu"]
        if v >= args.cpu_crit:
            code = CRITICAL
        elif v >= args.cpu_warn and code < WARNING:
            code = WARNING
    if "mem" in metrics:
        v = metrics["mem"]
        if v >= args.mem_crit:
            code = CRITICAL
        elif v >= args.mem_warn and code < WARNING:
            code = WARNING
    return code


def format_line(code, metrics):
    if code == OK:
        label = "OK"
    elif code == WARNING:
        label = "WARNING"
    elif code == CRITICAL:
        label = "CRITICAL"
    else:
        label = "UNKNOWN"
    values = []
    if "cpu" in metrics:
        values.append("cpu={0:.1f}%".format(metrics["cpu"]))
    if "mem" in metrics:
        values.append("mem={0:.1f}%".format(metrics["mem"]))
    return "{0} {1}".format(label, " ".join(values))


# ignore this func
def followup_collect_with_sampling(include, samples, interval):
    cpu_vals = []
    mem_vals = []
    for _ in range(samples):
        if "cpu" in include:
            cpu_vals.append(cpu_percent(interval))
        else:
            time.sleep(interval)
        if "mem" in include:
            mem_vals.append(mem_percent())
    out = {}
    if cpu_vals:
        out["cpu"] = sum(cpu_vals) / len(cpu_vals)
    if mem_vals:
        out["mem"] = sum(mem_vals) / len(mem_vals)
    return out


def main():
    args = build_parser().parse_args()
    ok, err = validate_args(args)
    if not ok:
        print("UNKNOWN invalid args: " + err)
        return UNKNOWN
    include = args.include.split(",")
    try:
        metrics = collect_metrics(include, args.interval)
        print(metrics)
        code = evaluate(metrics, args)
        print(format_line(code, metrics))
        return code
    except Exception as e:
        print("UNKNOWN " + str(e))
        return UNKNOWN


if __name__ == "__main__":
    sys.exit(main())