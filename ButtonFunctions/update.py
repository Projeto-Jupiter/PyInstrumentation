def update():
    global label, plt, lastUpdate, avgFps, rpltfunc, rec, forces, times, rcheck, force, pforce, ser
    try:
        if sp:
            msg = ser.readline()[:-2]
        else:
            msg = tn.read_until("\n")[:-2]
    except NoDataAvailableException:
        print('No data available')
        return

    pair = msg.split(",")
    if len(pair) == 2:
        time, pforce = pair

        try:
            pforce = float(pforce)
            force = pforce
        except:
            print("check connection")
        try:
            time = float(time) / 1000
        except:
            print("check connection")

        if time - times[0] > 10:
            times = times[1:]
            forces = forces[1:]
            times.append(time)
            forces.append(force)
        else:
            times.append(time)
            forces.append(force)

        if rec:
            pforces.append(force)
            ptimes.append(time - t0)
            pydata = np.asarray(pforces)
            pxdata = np.asarray(ptimes)
            prplt.plot(pxdata, pydata, clear=True, _callSync='off')

        ydata = np.asarray(forces)
        xdata = np.asarray(tixmes)

        rplt.plot(xdata, ydata, clear=True, _callSync='off')
        now = pg.ptime.time()
        fps = 1.0 / (now - lastUpdate)
        lastUpdate = now
        avgFps = avgFps * 0.8 + fps * 0.2
        label.setText("Generating %0.2f fps" % avgFps)