import csv
import os
from typings import Any, List


def save_curve(ptimes: List[str, Any], pforces: List[str, Any], filename: str, filepath: str) -> None:
    """Save Curve.

    Saves a curve into a csv format.
    """
    full_file_path = os.path.join(filepath, f'{filename}.csv')
    with open(full_file_path, 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(ptimes)
        wr.writerow(pforces)
