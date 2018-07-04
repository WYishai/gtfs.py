import csv
from zipfile import ZipFile

ignored_keys = []


def clean_row(row):
    for k, v in row.items():
        if v is None or v == '':
            del row[k]
        elif k in ["drop_off_type", "pickup_type"] and v == "0":
            del row[k]

    for ignored_key in ignored_keys:
        if ignored_key in row:
            del row[ignored_key]

    return row


def compare_gtfs_files(gtfs_file1, gtfs_file2, test_case):
    if not isinstance(gtfs_file1, ZipFile):
        with ZipFile(gtfs_file1) as gtfs_file1:
            return compare_gtfs_files(gtfs_file1, gtfs_file2, test_case)
    if not isinstance(gtfs_file2, ZipFile):
        with ZipFile(gtfs_file2) as gtfs_file2:
            return compare_gtfs_files(gtfs_file1, gtfs_file2, test_case)

    files_list1 = gtfs_file1.namelist()
    files_list2 = gtfs_file2.namelist()

    for i, file_name in enumerate(files_list1):
        if file_name not in files_list2:
            print 'File "%s" only on left' % (file_name,)
            del files_list1[i]

    for i, file_name in enumerate(files_list2):
        if file_name not in files_list1:
            print 'File "%s" only on right' % (file_name,)

    for file_name in files_list1:
        print '\nFile: "%s"' % (file_name,)
        with gtfs_file1.open(file_name, "r") as f:
            reader = csv.DictReader(f)
            lines = {tuple(sorted(clean_row(row).iteritems())) for row in reader}

        with gtfs_file2.open(file_name, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row = clean_row(row)
                row = tuple(sorted(row.iteritems()))
                test_case.assertIn(row, lines)
                lines.remove(row)

        test_case.assertEqual(len(lines), 0)

        print "OK"
