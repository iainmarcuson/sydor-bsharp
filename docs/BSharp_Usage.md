B# EPICS Usage
==============

Architecture
------------

The B# EPICS IOC communicates via sockets to an intermediate layer called the **socket splitter**.  The socket splitter communicates with the B# hardware over Ethernet.

The B# IOC loads its calibration data at start time, so changes such as connecting or disconnecting an attenuator require restarting the IOC.

Socket Splitter
---------------

The socket splitter is a Python script that sits between the IOC and the hardware.  It gets its name since it can take the single data stream from the B# hardware and split it into separate command and data sockets for EPICS.  This software communicates with the B#.

The socket splitter is located in the base directory of the B# quadEM distribution in file `socket_split_queue.py`.

To use the socket splitter, first edit `socket_split_queue.py` and change the line `BSHARP_ADDR` to contain the IP address of the B#.  Then run the socket splitter with `python3 socket_split_queue.py`

### Known Issues

* If you quit the B# IOC, the socket splitter will need to be reset for the next instance of the B# IOC.  Thus, if you quit the IOC, quit the splitter as well.
* The splitter does not always gracefully release its sockets.  This can result in an error message similar to
      OSError: [Errno 98] Address already in use
  The OS will release the sockets in a short time (generally a minute or so).  

Startup Scenario
----------------

1. Start the socket splitter
   1. `cd <quadEM directory>`
   2. Edit `socket_split_queue.py` line `BSHARP_ADDR` to point to the B#
   3. `python3 socket_split_queue.py` and ensure there are no "Address already in use" errors.
2. Start EPICS
   1. `cd <quadEM directory>/iocBoot/iocBS_EM`
   2. Put the correct calibrations in file `calibration.ini` e.g. `cp calibration_attenuator.ini calibration.ini`  The calibration file format is described in `<quadEM directory>/docs/bsharp_cal_file_format.md`
   3. Edit the parameters in `../../CONFIG.txt`.  **PREFIX** and **RECORD** are set according to your site.  **BROADCAST** needs to point to the IP address of the computer running the socket splitter; "127.0.0.1" if the socket splitter is running on the same computer as EPICS.
   4. `./st.cmd` to start EPICS.

Shutdown Scenario
-----------------

1. Exit EPICS.
2. Ctrl-C on the `python3 socket_split_queue.py` process.