# RTCM2_Type18

from RTCM2_Decls import *
import RTCM2
from bitField import bf
import pprint

class Type18 (RTCM2_Message):
    def __init__(self):
        self.Packet_ID=18
        self.Freq=None
        self.GNSS_Time=None
        self.SV_Details=None
        self.SVs=None

    def decode(self,length,data):
        if (length < 1):
            return Decode_Error
        else :

            self.SV_Details=[]
            self.Freq=RTCM2.extract_rtcm_bits(data[3],1,2)
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
                Quailty=int(RTCM2.extract_rtcm_bits(data[word],9,11))
                Slips=int(RTCM2.extract_rtcm_bits(data[word],12,16))
                Phase=RTCM2.extract_rtcm_bits(data[word],17,24)
                Phase<<=24
                Phase|=RTCM2.extract_rtcm_bits(data[word+1],1,24)
                Phase=RTCM2.twos_comp(Phase,32)/256.0

                self.SV_Details.append({'SV': SV_ID,'Pcode': Pcode, 'Last_Message':Last_Message,'GLONASS':Glonass, 'Quailty': Quailty,'Slips':Slips,'Phase':Phase})

            return Got_Packet



    def dump(self,dump):
        print "Time: {}".format(self.GNSS_Time)
        if self.Freq == 0 :
            print "Freq: L1"
        elif self.Freq == 1 :
            print "Freq: L2"
        else:
            print "Freq: Reserved"
        print "Number SV's: {} ".format(self.SVs)
        print " SV  SLIP PCODE QUAL LAST  PHASE (cycles)"
        for SV in range(self.SVs):
            print "{:3}    {:2} {}    {:1} {} {}".format(self.SV_Details[SV]['SV'],self.SV_Details[SV]['Slips'],self.SV_Details[SV]['Pcode'],self.SV_Details[SV]['Quailty'],self.SV_Details[SV]['Last_Message'],self.SV_Details[SV]['Phase'])
        #pprint.pprint (self.SV_Details)

#        quit()
