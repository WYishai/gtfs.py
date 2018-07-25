import os

RESOURCES_DIR_PATH = os.path.join(os.curdir, "resources")

GTFS_MINI_REAL_FILE = os.path.join(RESOURCES_DIR_PATH, "minimized_real_gtfs.zip")
GTFS_SAMPLE_FILE = os.path.join(RESOURCES_DIR_PATH, "sample_gtfs.zip")
GTFS_TEST_FILES = [GTFS_SAMPLE_FILE, GTFS_MINI_REAL_FILE]
