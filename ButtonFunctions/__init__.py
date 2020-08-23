import csv


def ignition(application):
    application.connection.write("sup\r\n")


def supress(application):
    application.connection.write("fire\r\n")


def save_curve(application) -> None:
    """Save Curve.

    Saves a curve into a csv format.
    """
    file_path = 'data.csv'
    with open(file_path, 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(application.times)
        wr.writerow(application.forces)
