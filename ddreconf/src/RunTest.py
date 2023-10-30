import logging
from Paths import *

from Main import solve

from LoggerConfig import basicConfig


def get_testcases():
    cases: dict[Path, list[Path]] = dict()

    for col in TEST_HOME.glob("**/*.col"):
        col = col.relative_to(TEST_HOME)
        cases[col] = []

    for dat in TEST_HOME.glob("**/*.dat"):
        dat = dat.relative_to(TEST_HOME)
        for col, dats in cases.items():
            if str(dat.with_suffix('')).startswith(str(col.with_suffix(''))):
                dats.append(dat)

    return cases


logger: logging.Logger = logging.getLogger(__name__)


if __name__ == '__main__':
    basicConfig()

    for col, dats in sorted(get_testcases().items()):
        for dat in dats:
            logger.info(f'start solving {dat}')
            solve(
                TEST_HOME / col,
                TEST_HOME / dat,
                out=TEST_OUT / dat.name,
                reorder_edges=True,
                reorder_vertices=True
            )
