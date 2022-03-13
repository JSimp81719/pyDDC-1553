import DDC, time
from ctypes import byref, c_short, c_ushort, c_uint32, create_string_buffer

#region VARIABLES

# Initalize Arrays
wBuffer = (c_ushort*32)()
aOpCodes = (c_short*10)()

# Important Addresses
RTAddress = 1
SubAddress = 1

# Data Block IDs
DBLK1 = 1

# Message IDs
MSG1 = 1

# OpCode IDs
OP1 = 1
OP2 = 2

# Frame IDs
MNR1 = 1
MJR = 2

# New Msg Struct
RetMsg = DDC.MSGSTRUCT()
MsgCount = c_uint32(0)
MsgLostHBuf = c_uint32(0)

#endregion

#region FUNCTIONS

def DisplayErrorMsg(ErrorCode):
    string_buffer = create_string_buffer(80)
    DDC.aceErrorStr(0, byref(string_buffer), 80)
    return string_buffer.value.decode()

#endregion


# ---------------------------------------------
# ------------ START TEST SEQUENCE ------------
# ---------------------------------------------

# Initialize and configure DDC Device
print("\n\nInitialize DDC Device: ", DDC.aceInitialize(0))
print("Create Data Block:", DDC.aceBCDataBlkCreate(0, DBLK1, DDC.DataBlkType.ACE_BC_DBLK_SINGLE.value, byref(wBuffer), 32))
print("Create RT->BT Msg (Receive):", DDC.aceBCMsgCreateRTtoBC(0, MSG1, DBLK1, RTAddress, SubAddress, 32, 0, DDC.MsgOptions.ACE_BCCTRL_CHL_A.value))
print("Create Msg Execute OpCode:", DDC.aceBCOpCodeCreate(0, OP1, DDC.BcOpCode.ACE_OPCODE_XEQ.value, DDC.BcConditionTest.ACE_CNDTST_ALWAYS.value, MSG1, 0, 0))
print("Create Frame Call OpCode:", DDC.aceBCOpCodeCreate(0, OP2, DDC.BcOpCode.ACE_OPCODE_CAL.value, DDC.BcConditionTest.ACE_CNDTST_ALWAYS.value, MNR1, 0, 0))

# Create Minor Frame to hold RT->BC Msg.
aOpCodes[0] = OP1
print("Create Minor Frame Containing \"Msg Execute\" OpCode:", DDC.aceBCFrameCreate(0, MNR1, DDC.BcFrameType.ACE_FRAME_MINOR.value, aOpCodes, 1, 0, 0))

# Create Major Frame to Hold Minor Frame.
aOpCodes[0] = OP2
print("Create Major Frame Containing the \"Call Minor Frame\" OpCode:", DDC.aceBCFrameCreate(0, MJR, DDC.BcFrameType.ACE_FRAME_MAJOR.value, aOpCodes, 1, 1000, 0))

# Create Hardware buffer to avoid message loss.
print("Create Hardware Buffer:", DDC.aceBCInstallHBuf(0, 32 * 1024))
time.sleep(3)

# Run Major Frame
print("Start Running Major Frame Indefinitely:", DDC.aceBCStart(0, MJR, -1)) # -1 forces Major Frame to run over and over again forever.

# Wait for buffer to begin filling
time.sleep(2)

# Get first message from HW Buffer and decode it.
print("Decode Msg Data:", DDC.aceBCGetHBufMsgDecoded(0, byref(RetMsg), byref(MsgCount), byref(MsgLostHBuf), DDC.BcMsgLoc.ACE_BC_MSGLOC_NEXT_PURGE.value))
print("\nTime Tag of Message:", RetMsg.wTimeTag)
print("Data Words of Message:", list(RetMsg.aDataWrds),"\n")

# useless delay
time.sleep(10)

# Stop DDC device and free all resources
print("Stop Major Frame:", DDC.aceBCStop(0))
print("Close DDC Device and Free Resources:", DDC.aceFree(0),"\n\n")


# ---------------------------------------------
# ------------- END TEST SEQUENCE -------------
# ---------------------------------------------