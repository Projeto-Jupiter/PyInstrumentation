import csv
import os
import time
import matplotlib.pyplot as plt

from constants import LOAD_CELL_REFF, PRESSURE_TRANSDUCER_REF


def ignition(application):
    prompt = application.add_prompt("Warning!", "This will start ignition. Are you sure?\n'O marimbondo vai morder'")
    if prompt:
        application.connection.get_handler(LOAD_CELL_REFF).connection.write("sup\r\n")


def supress(application):
    application.connection.get_handler(LOAD_CELL_REFF).connection.write("fire\r\n")


def save_curve(application) -> None:
    """Save Curve.
    Saves the retrieved data of each of the sensors into csv files.
    Also generates an image of the graph of Data objects with a designated plot.
    All the files are stored in a folder with name indicating timestamp.
    """
    timestr = time.strftime("%Y-%m-%d--%H-%M-%S")
    dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Saves', 'Save--'+timestr)
    os.makedirs(dir_path)

    for sensor in application.sensor_data:
        file_path = os.path.join(dir_path, sensor.name)
        with open(file_path+'.csv', 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL)
            wr.writerows(zip(sensor.times, sensor.data))
        if sensor.plot:
            plt.figure()
            plt.plot(sensor.times, sensor.data)
            plt.xlabel(sensor.xlabel)
            plt.ylabel(sensor.ylabel)
            plt.savefig(file_path+'.png')

def reset(application):
    """Reinitializes all Data objects and clears plot pannels"""
    prompt = application.add_prompt("Warning!", "This will erase all unsaved data. Are you sure?")
    if prompt:
        # application.connection.reset()
        application.data_initialization()
        for key, item in application.plot_pannels.items():
            item.clear()

def data_switch(application, ref):
    """Turns on/off the Update function for a specific Data object.
    The function receives a 'ref', which is the object's name attribute,
    based on the clicked button. This way, it can locate the correct one
    from the list, and set different texts based on the current status of 
    the object.
    """
    sensor = application.get_sensor_info(ref)
    current_value = sensor.updateStatus
    sensor.updateStatus = not current_value
    if not current_value:
         application.buttons[ref+'Switch'].setText("STOP " + ref)
    else:
         application.buttons[ref+'Switch'].setText("&START " + ref)
