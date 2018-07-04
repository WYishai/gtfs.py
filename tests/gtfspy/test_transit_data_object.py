import os
import tempfile
import unittest

from gtfspy import TransitData

import constants
from test_utils.gtfs_utils import compare_gtfs_files


class TestTransitDataLoad(unittest.TestCase):
    def test_load_from_file_path(self):
        file_path = constants.GTFS_TEST_FILE_PATH
        td1 = TransitData(gtfs_file=file_path)
        with open(file_path, "rb") as f:
            td2 = TransitData(gtfs_file=f)

        self.assertEqual(td1, td2)

    def test_import_export(self):
        file_path = constants.GTFS_TEST_FILE_PATH
        temp_file_path = tempfile.mktemp() + ".zip"
        try:
            td1 = TransitData(gtfs_file=file_path)
            td1.save(temp_file_path)
            td2 = TransitData(temp_file_path)
            self.assertEqual(td1, td2)

            compare_gtfs_files(file_path, temp_file_path, self)
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


if __name__ == '__main__':
    unittest.main()
