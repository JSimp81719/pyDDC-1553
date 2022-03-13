"""
///////////////////////////////////////////////////

#   Title: DDC Python Wrapper for emacepl.dll
#   Version 1.0
#   Joe Simpson
#
#   Description:
#   
#   Supports most DDC 1553 devices. Provides an interface
#   between the C++ DLL and Python to facilitate quick
#   and efficient DDC device programming and calls.

///////////////////////////////////////////////////
"""

from enum import Enum
from ctypes import WINFUNCTYPE, WinDLL, Structure, POINTER, c_buffer, c_char
from ctypes import c_int, c_uint32, c_short, c_ushort, c_uint, byref

# Path to C Dll
aceDll = WinDLL("lib\\emacepl.dll")

# Message Structure used by aceBCGetHBufMsgDecoded
class MSGSTRUCT(Structure):
    _fields_= [
        ("wType", c_ushort),            # Contains the msg type
        ("wBlkSts", c_ushort),          # Contains the block status word
        ("wTimeTag", c_ushort),         # Time tag of message
        ("wCmdWrd1", c_ushort),         # First command word
        ("wCmdWrd2", c_ushort),         # Second command word (RT to RT)
        ("wCmdWrd1Flg", c_ushort),      # Is command word 1 valid?
        ("wCmdWrd2Flg", c_ushort),      # Is command word 2 valid?
        ("wStsWrd1", c_ushort),         # First status word
        ("wStsWrd2", c_ushort),         # Second status word
        ("wStsWrd1Flg", c_ushort),      # Is status word 1 valid?
        ("wStsWrd2Flg", c_ushort),      # Is status word 2 valid?
        ("wWordCount", c_ushort),       # Number of valid data words
        ("aDataWrds", c_ushort*32),     # An array of data words

        # The following are only applicable in BC mode
        ("wBCCtrlWrd", c_ushort),       # Contains the BC control word
        ("wBCGapTime", c_ushort),       # Message gap time word
        ("wBCLoopBack1", c_ushort),     # First looped back word
        ("wTimeTag2", c_ushort),        # wBCLoopBack2 is redefined as TimeTag2
        ("wBCLoopBack1Flg", c_ushort),  # Is loop back 1 valid?
        ("wTimeTag3", c_ushort)         # wBCLoopBack2Flg is redefined as TimeTag3
    ]

# ENUMS
class MsgSize(Enum):
    # RAW message sizes
    ACE_MSGSIZE_RT   = 36
    ACE_MSGSIZE_MT   = 40
    ACE_MSGSIZE_BC   = 42
    ACE_MSGSIZE_RTMT = 42
    ACE_MSGSIZE_MRT  = 40

class MsgOptions(Enum):
    ACE_BCCTRL_CHL_A = 128
    ACE_BCCTRL_CHL_B = 0

class DataBlkType(Enum):
    ACE_BC_DBLK_SINGLE = 32
    ACE_BC_DBLK_DOUBLE = 33

class BcOpCode(Enum):
    ACE_OPCODE_XEQ = 1
    ACE_OPCODE_CAL = 3

class BcConditionTest(Enum):
    ACE_CNDTST_ALWAYS = 15

class BcFrameType(Enum):
    ACE_FRAME_MAJOR = 0
    ACE_FRAME_MINOR = 2

class BcMsgLoc(Enum):
    ACE_BC_MSGLOC_NEXT_PURGE    = 0
    ACE_BC_MSGLOC_NEXT_NPURGE   = 1
    ACE_BC_MSGLOC_LATEST_PURGE  = 2
    ACE_BC_MSGLOC_LATEST_NPURGE = 3

class BcAsyncMode(Enum):
    ACE_BC_ASYNC_LMODE = 1
    ACE_BC_ASYNC_HMODE = 2
    ACE_BC_ASYNC_BOTH  = 3

# ------------------------ FUNCTIONS -----------------------------------

def aceErrorStr(nError, pBuffer, wBufSize):
    """This function returns information describing a particular error."""

    Proto = WINFUNCTYPE(
            c_short,                    #Return
            c_short,                    #nError
            POINTER(c_char*wBufSize),   #pBuffer
            c_ushort)                   #wBufSize

    #Setup initial parameters
    #Params = (1, "p1", 0), (1, "p2", 0), (1, "p3", 0)

    #Setup function using proto
    f_aceErrorStr = Proto(("aceErrorStr", aceDll), None)

    #make DLL Call
    return f_aceErrorStr(c_short(nError), pBuffer, c_ushort(wBufSize))

# ---------------------------------------------------------------------
# ---------- Initialize, Config, Stop Functions -----------------------
# ---------------------------------------------------------------------

def aceInitialize(DevNum):
    """Initialize DDC Device as a particular bus mode."""

    Proto = WINFUNCTYPE(
            c_short,         #Return
            c_short,         #DevNum
            c_ushort,        #Config Access (CARD)
            c_ushort,        #Configure mode (BC, RT)
            c_uint,          #MemWrdSize (Not used by CARD)
            c_uint,          #RegAddr (Not used by CARD)
            c_uint)          #MemAddr (Not used by CARD)

    #Setup initial parameters
    myApiParams = (1, "p1", 0), (1, "p2", 0), (1, "p3", 1), (1, "p4", 0), (1, "p5", 0), (1, "p6", 0)

    #Setup function using proto
    f_aceInitialize = Proto(("aceInitialize", aceDll), myApiParams)

    #make DLL Call
    return f_aceInitialize(c_short(DevNum), c_ushort(0), c_ushort(1), c_uint(0), c_uint(0), c_uint(0))

def aceBCStart(DevNum, nMjrFrmID, iMjrFrmCount):
    """Start running the frames on the DDC device."""

    Proto = WINFUNCTYPE(
                c_short,    # Return 
                c_short,    # Device Number
                c_short,    # nMjrFrmID
                c_int)      # iMjrFrmCount

    #Setup initial parameters
    Params = (1, "p1", 0), (1, "p2", 0), (1, "p3", 0)

    #Setup function using proto
    f_aceBCStart = Proto(("aceBCStart", aceDll), Params)

    #make DLL Call
    return f_aceBCStart(c_short(DevNum), c_short(nMjrFrmID), c_int(iMjrFrmCount))

def aceBCConfigure(DevNum, dwOptions):
    """Configure the DDC device with special options."""

    Proto = WINFUNCTYPE(
                c_short,    # Return 
                c_short,    # Device Number
                c_uint)     # dwOptions

    #Setup initial parameters
    Params = (1, "p1", 0), (1, "p2", 0)

    #Setup function using proto
    f_aceBCConfigure = Proto(("aceBCConfigure", aceDll), Params)

    #make DLL Call
    return f_aceBCConfigure(c_short(DevNum), c_uint(dwOptions))

def aceBCStop(DevNum):
    """Stop running the frames on the DDC device."""

    Proto = WINFUNCTYPE(
                c_short,    # Return 
                c_short)    # Device Number

    #Setup function using proto
    f_aceBCStop = Proto(("aceBCStop", aceDll), None)

    #make DLL Call
    return f_aceBCStop(c_short(DevNum))

def aceFree(DevNum):
    """Close DDC device connection and free all resources."""

    Proto = WINFUNCTYPE(
                    c_short,    # Return 
                    c_short)    # Device Number

    f_aceFree = Proto(("aceFree", aceDll), None)

    return f_aceFree(c_short(DevNum))

# ---------------------------------------------------------------------
# ------------------- Data Block Functions ----------------------------
# ---------------------------------------------------------------------

def aceBCDataBlkCreate(DevNum, nDataBlkID, wDataBlkType, pBuffer, wBufferSize):
    """Create a data block to hold Rx/Tx data."""
    Proto = WINFUNCTYPE(
            c_short,                        #Return
            c_short,                        #DevNum
            c_short,                        #nDataBlkID
            c_ushort,                       #wDataBlkType
            POINTER(c_ushort*wBufferSize),  #pBuffer
            c_ushort)                       #wBufferSize

    #Setup initial parameters
    #Params = (1, "p1", 0), (1, "p2", 1), (1, "p3", DataBlkType.ACE_BC_DBLK_SINGLE.value), (1, "p4", 0), (1, "p5", 32)

    #Setup function using proto
    f_aceBCDataBlkCreate = Proto(("aceBCDataBlkCreate", aceDll), None)

    #make DLL Call
    return f_aceBCDataBlkCreate(c_short(DevNum), c_short(nDataBlkID), c_ushort(wDataBlkType), pBuffer, c_ushort(wBufferSize))

def aceBCDataBlkDelete(DevNum, mMjrFrmID):
    """Delete a data block used to hold Rx/Tx Data."""

    Proto = WINFUNCTYPE(
                c_short,    # Return 
                c_short,    # Device Number
                c_short)    # mMjrFrmID

    #Setup initial parameters
    Params = (1, "p1", 0), (1, "p2", 0)

    #Setup function using proto
    f_aceBCDataBlkDelete = Proto(("aceBCDataBlkDelete", aceDll), Params)

    #make DLL Call
    return f_aceBCDataBlkDelete(c_short(DevNum), c_short(mMjrFrmID))

# ---------------------------------------------------------------------
# -------------------- Message Functions ------------------------------
# ---------------------------------------------------------------------

def aceBCMsgCreateBCtoRT(DevNum, nMsgBlkID, nDataBlkID, wRT, wSA, wWC, wMsgGapTime, dwMsgOptions):
    """Create a synchronous message to send to a R.T. device."""
    Proto = WINFUNCTYPE(
            c_short,        #Return
            c_short,        #DevNum
            c_short,        #nMsgBlkID
            c_short,        #nDataBlkID
            c_ushort,       #wRT
            c_ushort,       #wSA
            c_ushort,       #wWC
            c_ushort,       #wMsgGaptTime
            c_uint)         #dwMsgOptions

    #Setup initial parameters
    Params = (1, "p1", 0), (1, "p2", 0x0001), (1, "p3", 0x0001), (1, "p4", 0x0001), (1, "p5", 0x0001), (1, "p6", 0x0020), (1, "p7", 0), (1, "p8", MsgOptions.ACE_BCCTRL_CHL_A.value)

    #Setup function using proto
    f_aceBCMsgCreateBCtoRT = Proto(("aceBCMsgCreateBCtoRT", aceDll), Params)

    #make DLL Call
    return f_aceBCMsgCreateBCtoRT(c_short(DevNum), c_short(nMsgBlkID), c_short(nDataBlkID), c_ushort(wRT), c_ushort(wSA), c_ushort(wWC), c_ushort(wMsgGapTime), c_uint(dwMsgOptions))

def aceBCAsyncMsgCreateBCtoRT(DevNum, nMsgBlkID, nDataBlkID, wRT, wSA, wWC, wMsgGapTime, dwMsgOptions, pBuffer):
    """Create an Asynchronous message to later send to a R.T. device."""
    Proto = WINFUNCTYPE(
            c_short,                # Return
            c_short,                # DevNum
            c_short,                # nMsgBlkID
            c_short,                # nDataBlkID
            c_ushort,               # wRT
            c_ushort,               # wSA
            c_ushort,               # wWC
            c_ushort,               # wMsgGaptTime
            c_uint,                 # dwMsgOptions
            POINTER(c_ushort*32))   # pBuffer

    #Setup initial parameters
    #Params = (1, "p1", 0), (1, "p2", 0x0001), (1, "p3", 0x0001), (1, "p4", 0x0001), (1, "p5", 0x0001), (1, "p6", 0x0020), (1, "p7", 0), (1, "p8", MsgOptions.ACE_BCCTRL_CHL_A.value), (1, "p9", None)

    #Setup function using proto
    f_aceBCAsyncMsgCreateBCtoRT = Proto(("aceBCAsyncMsgCreateBCtoRT", aceDll), None)

    #make DLL Call
    return f_aceBCAsyncMsgCreateBCtoRT(c_short(DevNum), c_short(nMsgBlkID), c_short(nDataBlkID), c_ushort(wRT), c_ushort(wSA), c_ushort(wWC), c_ushort(wMsgGapTime), c_uint(dwMsgOptions), pBuffer)

def aceBCMsgCreateRTtoBC(DevNum, nMsgBlkID, nDataBlkID, wRT, wSA, wWC, wMsgGapTime, dwMsgOptions):
    """Create a Synchronous message to receieve from a R.T. device."""
    Proto = WINFUNCTYPE(
            c_short,        #Return
            c_short,        #DevNum
            c_short,        #nMsgBlkID
            c_short,        #nDataBlkID
            c_ushort,       #wRT
            c_ushort,       #wSA
            c_ushort,       #wWC
            c_ushort,       #wMsgGaptTime
            c_uint)         #dwMsgOptions

    #Setup initial parameters
    Params = (1, "p1", 0), (1, "p2", 0x0001), (1, "p3", 0x0001), (1, "p4", 0x0001), (1, "p5", 0x0001), (1, "p6", 0x0020), (1, "p7", 0), (1, "p8", MsgOptions.ACE_BCCTRL_CHL_A.value)

    #Setup function using proto
    f_aceBCMsgCreateRTtoBC = Proto(("aceBCMsgCreateRTtoBC", aceDll), Params)

    #make DLL Call
    return f_aceBCMsgCreateRTtoBC(c_short(DevNum), c_short(nMsgBlkID), c_short(nDataBlkID), c_ushort(wRT), c_ushort(wSA), c_ushort(wWC), c_ushort(wMsgGapTime), c_uint(dwMsgOptions))

def aceBCMsgDelete(DevNum, mMsgBlkID):
    """Delete a data block used to hold Rx/Tx Data."""

    Proto = WINFUNCTYPE(
                c_short,    # Return 
                c_short,    # Device Number
                c_short)    # mMsgBlkID

    #Setup initial parameters
    Params = (1, "p1", 0), (1, "p2", 0)

    #Setup function using proto
    f_aceBCMsgDelete = Proto(("aceBCMsgDelete", aceDll), Params)

    #make DLL Call
    return f_aceBCMsgDelete(c_short(DevNum), c_short(mMsgBlkID))

def aceBCSendAsyncMsgHP(DevNum, nMsgID, wTimeFactor):
    """Start running the frames on the DDC device."""

    Proto = WINFUNCTYPE(
                c_short,    # Return 
                c_short,    # Device Number
                c_ushort,   # nMsgID
                c_ushort)   # wTimeFactor

    #Setup initial parameters
    Params = (1, "p1", 0), (1, "p2", 0), (1, "p3", 0)

    #Setup function using proto
    f_aceBCSendAsyncMsgHP = Proto(("aceBCSendAsyncMsgHP", aceDll), Params)

    #make DLL Call
    return f_aceBCSendAsyncMsgHP(c_short(DevNum), c_ushort(nMsgID), c_ushort(wTimeFactor))

# ---------------------------------------------------------------------
# --------------------- OpCode Functions ------------------------------
# ---------------------------------------------------------------------

def aceBCOpCodeCreate(DevNum, nOpCodeID, wOpCodeType, wCondition, dwParameter1, dwParameter2, dwReserved):
    """Create OpCode to include in Frame."""
    Proto = WINFUNCTYPE(
            c_short,    #Return
            c_short,    #DevNum
            c_short,    #nOpCodeID
            c_ushort,   #wOpCodeType
            c_ushort,   #wCondition
            c_uint32,   #dwParameter1
            c_uint32,   #dwParameter2
            c_uint32)   #dwReserved

    #Setup initial parameters
    Params = (1, "p1", 0), (1, "p2", 1), (1, "p3", BcOpCode.ACE_OPCODE_XEQ.value), (1, "p4", BcConditionTest.ACE_CNDTST_ALWAYS.value), (1, "p5", 0), (1, "p6", 0), (1, "p7", 0)

    #Setup function using proto
    f_aceBCOpCodeCreate = Proto(("aceBCOpCodeCreate", aceDll), Params)

    #make DLL Call
    return f_aceBCOpCodeCreate(c_short(DevNum), c_short(nOpCodeID), c_ushort(wOpCodeType), c_ushort(wCondition), c_uint32(dwParameter1), c_uint32(dwParameter2), c_uint32(dwReserved))

# ---------------------------------------------------------------------
# ------------------- Mjr/Mnr Frame Functions -------------------------
# ---------------------------------------------------------------------

def aceBCFrameCreate(DevNum, nFrameID, wFrameType, aOpCodeIDs, wOpCodeCount, wMnrFrmTime, wFlags):
    """Create a frame to hold the OpCodes."""
    Proto = WINFUNCTYPE(
            c_short,    #Return
            c_short,    #DevNum
            c_short,    #nFrameID
            c_ushort,   #wFrameType
            c_short*10, #aOpCodeIDs
            c_ushort,   #wOpCodeCount
            c_uint32,   #wMnrFrmTime
            c_ushort)   #wFlags

    #Setup initial parameters
    Params = (1, "p1", 0), (1, "p2", 0), (1, "p3", 0), (1, "p4", 0), (1, "p5", 0), (1, "p6", 0), (1, "p7", 0)

    #Setup function using proto
    f_aceBCFrameCreate = Proto(("aceBCFrameCreate", aceDll), Params)

    #make DLL Call
    return f_aceBCFrameCreate(c_short(DevNum), c_short(nFrameID), c_ushort(wFrameType), aOpCodeIDs, c_ushort(wOpCodeCount), c_uint32(wMnrFrmTime), c_ushort(wFlags))

# ---------------------------------------------------------------------
# -------------------- HW Buffer Functions ----------------------------
# ---------------------------------------------------------------------

def aceBCInstallHBuf(DevNum, dwHBufSize):
    """Install Hardware Buffer to hold Rx/Tx Data."""

    Proto = WINFUNCTYPE(
            c_short,    # Return 
            c_short,    # Device Number
            c_uint)     # HW Buffer Size

    #Setup initial parameters
    Params = (1, "p1", 0), (1, "p2", 0)

    #Setup function using proto
    f_aceBCInstallHBuf = Proto(("aceBCInstallHBuf", aceDll), Params)

    #make DLL Call
    return f_aceBCInstallHBuf(c_short(DevNum), c_uint(dwHBufSize))

def aceBCGetHBufMsgDecoded(DevNum, pMsg, pdwMsgCount, pdwMsgLostHBuf, wMsgLoc):
    """Decode HW Buffer Msg into """

    Proto = WINFUNCTYPE(
            c_short,    # Return
            c_short,    # DevNum 
            POINTER(MSGSTRUCT),  # pMsg
            POINTER(c_uint32),   # pdwMsgCount
            POINTER(c_uint32),   # pdwMsgLostHBuf
            c_ushort)   # wMsgLoc

    #Setup initial parameters
    #Params = (1, "p1", 0), (1, "p2", 0), (1, "p3", 0), (1, "p4", 0), (1, "p5", BcMsgLoc.ACE_BC_MSGLOC_NEXT_PURGE.value)

    #Setup function using proto
    f_aceBCGetHBufMsgDecoded = Proto(("aceBCGetHBufMsgDecoded", aceDll), None)

    #make DLL Call
    return f_aceBCGetHBufMsgDecoded(c_short(DevNum), pMsg, pdwMsgCount, pdwMsgLostHBuf, c_ushort(wMsgLoc))

