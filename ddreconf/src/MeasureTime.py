import logging

from time import perf_counter_ns

logger: logging.Logger = logging.getLogger(__name__)

def measure_time(f, name: str):
    start_ns = perf_counter_ns()
    result = f()
    end_ns = perf_counter_ns()
    elapsed_s = (end_ns - start_ns) // 10 ** 9

    logger.info(f'Time {name: <10}: {elapsed_s} (sec)')

    return result
