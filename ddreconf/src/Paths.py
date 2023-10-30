from pathlib import Path

SRC_HOME = Path(__file__).parent

DD_RECONF_HOME = SRC_HOME / 'ddreconf'
DD_RECONF_BIN = DD_RECONF_HOME / 'ddreconf'

ROOT = SRC_HOME.parent

TEST_HOME = ROOT / 'test/2022benchmark/benchmark'
TEST_OUT = ROOT / 'test/out'
