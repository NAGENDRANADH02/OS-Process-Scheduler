"""Pure scheduling algorithms. A lower numeric priority is a higher priority."""
from collections import deque
from typing import Callable


def _normalize(processes):
    return sorted([dict(p, remaining=p["burst_time"]) for p in processes], key=lambda p: (p["arrival_time"], p["pid"]))


def _append(segments, pid, start, end):
    if end == start:
        return
    if segments and segments[-1]["pid"] == pid and segments[-1]["end"] == start:
        segments[-1]["end"] = end
    else:
        segments.append({"pid": pid, "start": start, "end": end})


def _result(processes, segments):
    completion = {s["pid"]: s["end"] for s in segments if s["pid"] != "IDLE"}
    metrics = []
    for p in sorted(processes, key=lambda x: x["pid"]):
        turnaround = completion[p["pid"]] - p["arrival_time"]
        metrics.append({"pid": p["pid"], "arrival_time": p["arrival_time"], "burst_time": p["burst_time"],
                        "priority": p.get("priority"), "completion_time": completion[p["pid"]],
                        "turnaround_time": turnaround, "waiting_time": turnaround - p["burst_time"]})
    # The simulator begins at time zero, so initial CPU idle time is included.
    first = 0
    last = max(completion.values())
    busy = sum(s["end"] - s["start"] for s in segments if s["pid"] != "IDLE")
    n = len(processes)
    return {"segments": segments, "metrics": metrics, "aggregate": {
        "average_waiting_time": round(sum(m["waiting_time"] for m in metrics) / n, 2),
        "average_turnaround_time": round(sum(m["turnaround_time"] for m in metrics) / n, 2),
        "cpu_utilization": round((busy / (last - first)) * 100, 2),
        "throughput": round(n / (last - first), 4),
    }}


def fcfs(processes):
    procs, segments, now = _normalize(processes), [], 0
    for p in procs:
        if now < p["arrival_time"]:
            _append(segments, "IDLE", now, p["arrival_time"]); now = p["arrival_time"]
        _append(segments, p["pid"], now, now + p["burst_time"]); now += p["burst_time"]
    return _result(procs, segments)


def sjf_non_preemptive(processes):
    return _non_preemptive(processes, lambda p: (p["burst_time"], p["arrival_time"], p["pid"]))


def priority_non_preemptive(processes):
    return _non_preemptive(processes, lambda p: (p["priority"], p["arrival_time"], p["pid"]))


def _non_preemptive(processes, key: Callable):
    remaining, segments, now = _normalize(processes), [], 0
    while remaining:
        ready = [p for p in remaining if p["arrival_time"] <= now]
        if not ready:
            next_time = min(p["arrival_time"] for p in remaining)
            _append(segments, "IDLE", now, next_time); now = next_time; continue
        p = min(ready, key=key); remaining.remove(p)
        _append(segments, p["pid"], now, now + p["burst_time"]); now += p["burst_time"]
    return _result(processes, segments)


def sjf_preemptive(processes):
    return _preemptive(processes, lambda p: (p["remaining"], p["arrival_time"], p["pid"]))


def priority_preemptive(processes):
    return _preemptive(processes, lambda p: (p["priority"], p["arrival_time"], p["pid"]))


def _preemptive(processes, key: Callable):
    procs, segments, now, done = _normalize(processes), [], 0, 0
    while done < len(procs):
        ready = [p for p in procs if p["arrival_time"] <= now and p["remaining"] > 0]
        if not ready:
            future = min(p["arrival_time"] for p in procs if p["remaining"] > 0)
            _append(segments, "IDLE", now, future); now = future; continue
        p = min(ready, key=key)
        _append(segments, p["pid"], now, now + 1); p["remaining"] -= 1; now += 1
        if p["remaining"] == 0: done += 1
    return _result(processes, segments)


def round_robin(processes, quantum):
    procs, queue, segments, now, i = _normalize(processes), deque(), [], 0, 0
    while queue or i < len(procs):
        if not queue:
            if now < procs[i]["arrival_time"]:
                _append(segments, "IDLE", now, procs[i]["arrival_time"]); now = procs[i]["arrival_time"]
            while i < len(procs) and procs[i]["arrival_time"] <= now: queue.append(procs[i]); i += 1
        current = queue.popleft(); run = min(quantum, current["remaining"])
        _append(segments, current["pid"], now, now + run); now += run; current["remaining"] -= run
        while i < len(procs) and procs[i]["arrival_time"] <= now: queue.append(procs[i]); i += 1
        if current["remaining"] > 0: queue.append(current)
    return _result(processes, segments)


ALGORITHMS = {"fcfs": fcfs, "sjf_non_preemptive": sjf_non_preemptive, "sjf_preemptive": sjf_preemptive,
              "round_robin": round_robin, "priority_non_preemptive": priority_non_preemptive,
              "priority_preemptive": priority_preemptive}
