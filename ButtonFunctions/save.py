import csv
import os
from typing import Any, List


def save_curve(ptimes: List[str], pforces: List[str], filename: str, filepath: str) -> None:
    """Save Curve.

    Saves a curve into a csv format.
    """
    full_file_path = os.path.join(filepath, f'{filename}.csv')
    with open(full_file_path, 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(ptimes)
        wr.writerow(pforces)
