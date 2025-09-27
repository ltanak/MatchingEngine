import time
import statistics
from typing import Callable, List, Any, Dict


class BenchmarkResult:
    def __init__(self, name: str, timings: List[float], extra: Dict[str, Any] = None):
        self.name = name
        self.timings = timings
        self.extra = extra or {}

    def mean(self):
        return statistics.mean(self.timings)

    def stdev(self):
        return statistics.stdev(self.timings) if len(self.timings) > 1 else 0.0

    def median(self):
        return statistics.median(self.timings)

    def __str__(self):
        return (
            f"{self.name}: mean={self.mean():.4f}s "
            f"stdev={self.stdev():.4f}s median={self.median():.4f}s "
            f"(n={len(self.timings)}) extras={self.extra}"
        )


def bench(fn: Callable, *args, runs: int = 3, **kwargs) -> BenchmarkResult:
    timings = []
    for i in range(runs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        end = time.perf_counter()
        timings.append(end - start)
    return BenchmarkResult(fn.__name__, timings, extra={"args": args, "kwargs": kwargs})


def run_benchmarks(benchmarks: List[BenchmarkResult]):
    print("=" * 40)
    print("Benchmark results")
    print("=" * 40)
    for result in benchmarks:
        print(result)
    print("=" * 40)
