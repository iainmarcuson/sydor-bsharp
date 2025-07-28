B# Calibration File Requirements
================================

Invocation
----------

Start the IOC by switching to `<QuadEM directory>/iocBoot/iocBS_EM` and running `./st.cmd`.  This ensures the IOC will look for the calibration file in the correct place.

File Name and Format
--------------------

The calibration file must be called `calibration.ini`.  The format is as follows:

1. There must be range headings with the format
	`[direct_range<n>]`, where `<n>` is 0 to 7.
2. Under each range that is populated, there must be four calibration lines, of the format
	`Channel<c>="<slope>,<offset>"`  `<c>` must be one of "A" through "D".  `<slope>` and `<offset>` are the calculated calibration values.  The quotation marks are mandatory.