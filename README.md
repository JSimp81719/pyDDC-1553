Python Wrapper for most DDC MIL-STD-1553 USB Devices.

This wraps the DDC ***emacepl.dll*** C-library for use in python 3.6+ applications.

The most important functions are contained within the DDC.py file for easy re-use as a stand-alone library. The Main.py script contains an example of how to configure and use the DDC device and its library.

If, when designing/developing for your DDC USB device, the SDK uses the ***emacepl.dll*** file, you can use this repo to develop MIL-STD-1553 communication within Python.

Currently Supported Functions:

- General Functions:
```
aceErrorStr
aceInitialize
aceBCStart
aceBCConfigure
aceBCStop
aceFree
```

- Data Block Functions:
```
aceBCDataBlkCreate
aceBCDataBlkDelete
```

- Message Functions:
```
aceBCMsgCreateBCtoRT
aceBCAsyncMsgCreateBCtoRT
aceBCMsgCreateRTtoBC
aceBCMsgDelete
aceBCSendAsyncMsgHP
```

- OpCode Functions
```
aceBCOpCodeCreate
```

- Major / Minor Frame Functions
```
aceBCFrameCreate
```

- Hardware Buffer Functions
```
aceBCInstallHBuf
aceBCGetHBufMsgDecoded
```
