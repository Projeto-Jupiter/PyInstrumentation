import numpy as np

from connection import NoDataAvailableException


def update(application):
    connection = application.connection
    try:
        msg = connection.fetch_data()
    except NoDataAvailableException:
        print('No data available')
        return
    pair = msg.split(",")
    if len(pair) == 2:
        time, pforce = pair

        # check data
        pforce = float(pforce)
        force = pforce
        time = float(time) / 1000
        application.forces.append(force)
        application.times.append(time)
        ydata = np.asarray(application.forces)
        xdata = np.asarray(application.times)
        application.plot_pannels['plot2'].plot(xdata, ydata, clear=True, _callSync='off')

        # FORCES = forces
        # TIMES = times
        # now = pg.ptime.time()
        # fps = 1.0 / (now - lastUpdate)
        # lastUpdate = now
        # avgFps = avgFps * 0.8 + fps * 0.2
        # label.setText("Generating %0.2f fps" % avgFps)

        # if rec:
        #    pforces.append(force)
        #    ptimes.append(time - t0)
        #    pydata = np.asarray(pforces)
        #    pxdata = np.asarray(ptimes)
        #    prplt.plot(pxdata, pydata, clear=True, _callSync='off')
