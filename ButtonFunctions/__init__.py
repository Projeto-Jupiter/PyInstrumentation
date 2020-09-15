import csv

from constants import LOAD_CELL_REFF, PRESSURE_TRANSDUCER_REF


def ignition(application):
    prompt = application.add_prompt("Warning!", "This will start ignition. Are you sure?\n'O marimbondo vai morder'")
    if prompt:
        application.connection.get_handler(LOAD_CELL_REFF).connection.write("sup\r\n")


def supress(application):
    application.connection.get_handler(LOAD_CELL_REFF).connection.write("fire\r\n")


def save_curve(application) -> None:
    """Save Curve.

    Saves a curve into a csv format.
    """
    file_path = 'data.csv'
    with open(file_path, 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(application.times)
        wr.writerow(application.forces)


def reset(application):
    prompt = application.add_prompt("Warning!", "This will erase all unsaved data. Are you sure?")
    if prompt:
        # application.connection.reset()
        application.data_initialization()
        for key, item in application.plot_pannels.items():
            item.clear()





def start_transducer(application):
    sensor = application.get_sensor_info(PRESSURE_TRANSDUCER_REF)
    current_value = sensor.updateStatus
    sensor.updateStatus = not current_value
    if not current_value:
        application.buttons['start_transducer'].setText("&STOP Transducer")
    else:
        application.buttons['start_transducer'].setText("&START Transducer")


def cell_switch(application):
    sensor = application.get_sensor_info(LOAD_CELL_REFF)
    current_value = sensor.updateStatus
    sensor.updateStatus = not current_value
    if not current_value:
        application.buttons['update_cell'].setText("&STOP Cell")
    else:
        application.buttons['update_cell'].setText("&START Cell")
