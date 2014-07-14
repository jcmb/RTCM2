# RTCM2_Type24

from RTCM2_Decls import *
import RTCM2
from bitField import bf

class Type24 (RTCM2_Message):
    def __init__(self):
        self.Packet_ID=24
        self.ECF_X=None
        self.ECF_Y=None
        self.ECF_Z=None
        self.GLONASS=None
        self.Ant_Height_Included=None
        self.Ant_Height=0

    def decode(self,length,data):
        if (length < 5) or (length > 6):
            return Decode_Error
        else :

            ECF=RTCM2.extract_rtcm_bits(data[3],1,24)
            ECF<<=14
            ECF|=RTCM2.extract_rtcm_bits(data[4],1,14)

            self.ECF_X=RTCM2.twos_comp(ECF,38)/10000.0

            ECF=RTCM2.extract_rtcm_bits(data[4],17,24)
            ECF<<=24
            ECF|=RTCM2.extract_rtcm_bits(data[5],1,24)
            ECF<<=6
            ECF|=RTCM2.extract_rtcm_bits(data[6],1,6)

            self.ECF_Y=RTCM2.twos_comp(ECF,38)/10000.0

            ECF=RTCM2.extract_rtcm_bits(data[6],9,24)
            ECF<<=22
            ECF|=RTCM2.extract_rtcm_bits(data[7],1,22)
            self.ECF_Z=RTCM2.twos_comp(ECF,38)/10000.0

            self.GLONASS=RTCM2.extract_rtcm_bits(data[7],23,23)==1
            self.Ant_Height_Included=RTCM2.extract_rtcm_bits(data[7],24,24)==1

            if self.Ant_Height_Included:
                self.Ant_Height=int(RTCM2.extract_rtcm_bits(data[8],1,18))/10000.0
            else :
                self.Ant_Height=None
            return Got_Packet



    def dump(self,dump):
        print "X: {:12.4f}m Y: {:12.4f}m Z: {:12.4f}m".format(self.ECF_X,self.ECF_Y,self.ECF_Z)
        if self.Ant_Height_Included:
            print "Antenna Height: {:.4}m".format(self.Ant_Height)
        else :
            print "Antenna Height: Not Included"

        if self.GLONASS:
            print "GLONASS Base position"
        else:
            print "GPS Base position"

