# RTCM2_Type18

from RTCM2_Decls import *
import RTCM2
from bitField import bf
import pprint

class Type19 (RTCM2_Message):
    def __init__(self):
        self.Packet_ID=19
        self.Freq=None
        self.GNSS_Time=None
        self.SV_Details=None
        self.SVs=None
        self.Smoothed=None

    def decode(self,length,data):
        if (length < 1):
            return Decode_Error
        else :

            self.SV_Details=[]
            self.Freq=RTCM2.extract_rtcm_bits(data[3],1,2)
            self.Smoothed=RTCM2.extract_rtcm_bits(data[3],3,4)
            self.GNSS_Time=RTCM2.extract_rtcm_bits(data[3],5,24)
            self.SVs=(length-1)/2 # 3=0, 5=1, 7=2

            for SV in range (self.SVs):
                word=SV*2+4 # 4,6,8..
                Last_Message=RTCM2.extract_rtcm_bits(data[word],1,1)==1
                Pcode=RTCM2.extract_rtcm_bits(data[word],2,2)==1
                Glonass=RTCM2.extract_rtcm_bits(data[word],3,3)==1
                SV_ID=int(RTCM2.extract_rtcm_bits(data[word],4,8))
                if SV_ID == 0 :
                    SV_ID=32
                Quailty=int(RTCM2.extract_rtcm_bits(data[word],9,12))
                Multipath=int(RTCM2.extract_rtcm_bits(data[word],13,16))
                Range=RTCM2.extract_rtcm_bits(data[word],17,24)
                Range<<=24
                Range|=RTCM2.extract_rtcm_bits(data[word+1],1,24)
                Range=RTCM2.twos_comp(Range,32)/50.0 # 0.02cm

                self.SV_Details.append({'SV': SV_ID,'Pcode': Pcode, 'Last_Message':Last_Message,'GLONASS':Glonass, 'Multipath':Multipath, 'Quailty': Quailty,'Range':Range})

            return Got_Packet



    def dump(self,dump):
        print "Time: {}".format(self.GNSS_Time)
        if self.Freq == 0 :
            print "Freq: L1"
        elif self.Freq == 1 :
            print "Freq: L2"
        else:
            print "Freq: Reserved"

        if self.Smoothed == 0 :
            print "Smoothing: 0 to 1 (Minutes)"
        elif self.Smoothed == 1 :
            print "Smoothing: 1- to 5 (Minutes)"
        elif self.Smoothed == 2 :
            print "Smoothing: 5- to 15 (Minutes)"
        else:
            print "Smoothing: Undefined"

        print "Number SV's: {} ".format(self.SVs)
        print " SV MUTLI PCODE QUAL LAST  Range (m)"
        for SV in range(self.SVs):
            print "{:3}    {:2} {}    {:1} {} {}".format(self.SV_Details[SV]['SV'],self.SV_Details[SV]['Multipath'],self.SV_Details[SV]['Pcode'],self.SV_Details[SV]['Quailty'],self.SV_Details[SV]['Last_Message'],self.SV_Details[SV]['Range'])
        #pprint.pprint (self.SV_Details)

