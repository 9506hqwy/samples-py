import unittest
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp


class GroongaTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.lib_path = None
        self.db_base = Path(mkdtemp())
        self.db_path = self.db_base / "test.db"

    def tearDown(self) -> None:
        rmtree(self.db_base)
        self.lib_path = None
