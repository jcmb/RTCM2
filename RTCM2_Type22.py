# RTCM2_Type24

from RTCM2_Decls import *
import RTCM2
from bitField import bf

class Type22 (RTCM2_Message):
    def __init__(self):
        self.Packet_ID=24
        self.ECF_X=None
        self.ECF_Y=None
        self.ECF_Z=None
        self.GLONASS=None
        self.Ant_Height_Included=None
        self.Ant_Height=0

    def decode(self,length,data):
        if (length < 1) or (length > 3):
            return Decode_Error
        else :

            ECF=RTCM2.extract_rtcm_bits(data[3],1,8)
            self.dECF_X=RTCM2.twos_comp(ECF,8)/256.0

            ECF=RTCM2.extract_rtcm_bits(data[3],9,16)
            self.dECF_Y=RTCM2.twos_comp(ECF,8)/256.0

            ECF=RTCM2.extract_rtcm_bits(data[3],17,24)
            self.dECF_Z=RTCM2.twos_comp(ECF,8)/256.0

            if length >= 2 :
                self.Antenna_Info=True
                self.System=RTCM2.extract_rtcm_bits(data[4],3,3)
                self.Antenna_Type_Inc=RTCM2.extract_rtcm_bits(data[4],4,4)==1
                self.Antenna_ARP_Inc=RTCM2.extract_rtcm_bits(data[4],5,5)==1
                self.Antenna_Height_Inc=RTCM2.extract_rtcm_bits(data[4],6,6)==0
                if self.Antenna_Height_Inc :
                    self.Antenna_Height=RTCM2.extract_rtcm_bits(data[4],5,24)/256
                else:
                    self.Antenna_Height=None
            else :
                self.Antenna_Info=False
                self.System=None
                self.Antenna_Type_Inc=None
                self.Antenna_ARP_Inc=None
                self.Antenna_Height_Inc=None
                self.Antenna_Height=None

            if length >= 3 :
                self.L2_Offsets=True
                ECF=RTCM2.extract_rtcm_bits(data[5],1,8)
                self.L2_DECF_X=RTCM2.twos_comp(ECF,8)/16.0
                ECF=RTCM2.extract_rtcm_bits(data[5],9,16)
                self.L2_DECF_Y=RTCM2.twos_comp(ECF,8)/16.0
                ECF=RTCM2.extract_rtcm_bits(data[5],17,24)
                self.L2_DECF_Z=RTCM2.twos_comp(ECF,8)/16.0
            else:
                self.L2_Offsets=False
                self.L2_dECF_X=None
                self.L2_dECF_Y=None
                self.L2_dECF_Z=None

            return Got_Packet



    def dump(self,dump):
        print "dX: {:12.4f}m dY: {:12.4f}m dZ: {:12.4f}m".format(self.dECF_X,self.dECF_Y,self.dECF_Z)

        if self.Antenna_Info:
            print "System: {}  Type 23: {}  Type 24: {}  Height: {:.2f}cm".format (RTCM2_System_Names[self.System],self.Antenna_Type_Inc,self.Antenna_ARP_Inc,self.Antenna_Height)
        else :
            print " Antenna information not included"

        if self.L2_Offsets:
            print "dX: {:12.4f}m dY: {:12.4f}m dZ: {:12.4f}m".format(self.L2_dECF_X,self.l2_dECF_Y,self.l2_dECF_Z)
        else :
            print " L2 Antenna offset information not included"

