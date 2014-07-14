Dump_None=0
Dump_ID=1
Dump_Summary=2
Dump_Full=3
Dump_Verbose=4


Need_More=0
Got_ACK=1
Got_NACK=2
Got_Undecoded=3 # This is not really an undecoded packet but bytes that are not part of a packet
Got_Packet=4
Got_Sub_Packet=5
Missing_Sub_Packet=6
Decode_Error=7

RTCM2_Min_Message_ID = 0 # Min Decoded Message
RTCM2_Max_Message_ID = 63 # Max Decoded Message

RTCM2_Message_Names=[]

RTCM2_Message_Names = (
    'RTCM Type 2: Message Type 64 (ID 0)',
    'Differential GPS Corrections ',
    'Delta Differential GPS Corrections (Retired) Unvalidated!!',
    'GPS Reference Station Parameters',
    'Reference Station Datum',
    'GPS Constellation Health',
    'GPS Null Frame',
    'DGPS Radiobeacon Almanac  (to be retired) Unvalidated!!',
    'Pseudolite Almanac (Tentative)',
    'GPS Partial Correction Set',
    'P-Code Differential Corrections (Reserved, Retired)',
    'C/A-Code L1, L2 Delta Corrections (Reserved, Retired)',
    'Pseudolite Station Parameters (Reserved, Retired)',
    'Ground Transmitter Parameters (Tentative, Retired)',
    'GPS Time of Week',
    'Ionospheric Delay Message',
    'GPS Special Message',
    'GPS Ephemerides  (Tentative)',
    'RTK Uncorrected Carrier Phases (Retired)',
    'RTK Uncorrected Pseudoranges (Retired)',
    'RTK Carrier Phase Corrections (Retired)',
    'RTK/Hi-Accuracy Pseudorange Corrections (Retired)',
    'Extended Reference Station Parameters  (to be Retired)',
    'Antenna Type Definition Record',
    'Antenna Reference Point (ARP)',
    'RTCM Type 2: Message Type 25',
    'RTCM Type 2: Message Type 26',
    'Extended Radiobeacon Almanac',
    'RTCM Type 2: Message Type 28',
    'RTCM Type 2: Message Type 29',
    'RTCM Type 2: Message Type 30',
    'Differential GLONASS Corrections (Tentative, Retired)',
    'Differential GLONASS Reference Station Parameters (Tentative, to be retired)',
    'GLONASS Constellation Health (Tentative, to be retired)',
    'GLONASS Partial Differential Correction Set (N > 1) or Null (Tentative, Retired)',
    'GLONASS Radiobeacon Almanac (Tentative, to be retired)',
    'GLONASS Special Message',
    'GNSS System Time Offset',
    'RTCM Type 2: Message Type 38',
    'RTCM Type 2: Message Type 39',
    'RTCM Type 2: Message Type 40',
    'GNSS Differential Corrections',
    'Generic GNSS Partial Basic Corrections',
    'Generic GNSS Nav Data Validity & Signal Health',
    'Generic GNSS Message (Reserved)',
    'Galileo Integrity Data (Reserved)',
    'RTCM Type 2: Message Type 46',
    'RTCM Type 2: Message Type 47',
    'RTCM Type 2: Message Type 48',
    'RTCM Type 2: Message Type 49',
    'RTCM Type 2: Message Type 50',
    'RTCM Type 2: Message Type 51',
    'RTCM Type 2: Message Type 52',
    'RTCM Type 2: Message Type 53',
    'RTCM Type 2: Message Type 54',
    'RTCM Type 2: Message Type 55',
    'RTCM Type 2: Message Type 56',
    'RTCM Type 2: Message Type 57',
    'Emergency Alert Message',
    'Proprietary Message',
    'RTCM Type 2: Multipurpose Usage 60',
    'RTCM Type 2: Multipurpose Usage 61',
    'RTCM Type 2: Multipurpose Usage 62',
    'RTCM Type 2: Multipurpose Usage 63');


RTCM2_Health_Names = (
    'UDRE Scale Factor = 1',
    'UDRE Scale Factor = 0.75',
    'UDRE Scale Factor = 0.5',
    'UDRE Scale Factor = 0.3',
    'UDRE Scale Factor = 0.2',
    'UDRE Scale Factor = 0.1',
    'Not Monitored',
    "Not Working")


RTCM2_UDRE_Names = (
    '<=1m',
    '>1m & <=4m',
    '>4m & <=8m',
    '>8m')

RTCM2_System_Names = (
    'GPS',
    'GLONASS'
    )

class RTCM2_Message:

    def __init__(self):
        self.Packet_ID=None

    def decode(self, length, data):
        pass;

    def dump(self,dump_level):
        pass;
