Python Wrapper for most DDC MIL-STD-1553 USB Devices.

This wraps the DDC emacepl.dll C library for use in python 3.6+ applications.

All of the functions are contained within the DDC.py file for easy re-use as a stand-along library. The Main.py script contains an example of how to configure and use the DDC device and it's library.

If, when designing/developing for your DDC USB device, check to see if the SDK uses the emacepl.dll file. If it does, you can use this to develop MIL-STD-1553 communication within Python.