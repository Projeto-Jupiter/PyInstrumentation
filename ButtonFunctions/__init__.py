import csv
import matplotlib.pyplot as plt


def ignition(application):
    application.connection.write("sup\r\n")


def supress(application):
    application.connection.write("fire\r\n")


def save_curve(application) -> None:
    """Save Curve.

    Saves a curve into a csv format.
    """
    file_path = 'data.csv'
    with open(file_path, 'w', newline ='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL)
        for i in range(len(application.times)):
            wr.writerow([application.times[i],application.forces[i]])
    plt.plot(application.times, application.forces)
    plt.xlabel("Time (s)")
    plt.ylabel("Force (N)")
    plt.savefig('data.png')
