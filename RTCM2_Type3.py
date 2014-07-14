# RTCM2_Type3

from RTCM2_Decls import *
import RTCM2
from bitField import bf

class Type3 (RTCM2_Message):
    def __init__(self):
        self.Packet_ID=3
        self.ECF_X=None
        self.ECF_Y=None
        self.ECF_Z=None

    def decode(self,length,data):
        if (length != 4):
            return Decode_Error
        else :

            ECF=RTCM2.extract_rtcm_bits(data[3],1,24)
            ECF<<=8
            ECF|=RTCM2.extract_rtcm_bits(data[4],1,8)

            self.ECF_X=RTCM2.twos_comp(ECF,32)/100.0

            ECF=RTCM2.extract_rtcm_bits(data[4],9,24)
            ECF<<=16
            ECF|=RTCM2.extract_rtcm_bits(data[5],1,16)

            self.ECF_Y=int(ECF)/100.0
            self.ECF_Y=RTCM2.twos_comp(ECF,32)/100.0

            ECF=RTCM2.extract_rtcm_bits(data[5],17,24)
            ECF<<=24
            ECF|=RTCM2.extract_rtcm_bits(data[6],1,24)
            self.ECF_Z=RTCM2.twos_comp(ECF,32)/100.0

            return Got_Packet



    def dump(self,dump):
        print "X: {:12.4f}m Y: {:12.4f}m Z: {:12.4f}m".format(self.ECF_X,self.ECF_Y,self.ECF_Z)
