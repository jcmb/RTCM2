# RTCM2_Type2

from RTCM2_Decls import *
import RTCM2
from bitField import bf
import pprint

Typ1_UDRE_Names = (
    '<=1m',
    '>1m & <=4m',
    '>4m & <=8m',
    '>8m')


class Type2 (RTCM2_Message):
    def __init__(self):
        self.Packet_ID=2
        self.SVs=None

    def decode(self,length,data):
        if (length < 1):
            return Decode_Error
        else :
            self.SV_Details=[]
            self.SVs=0
            wb = RTCM2.word_bit(3,1)
            finished=False

            while not finished:
                self.SVs+=1
                Scale_Factor=wb.extract_rtcm_data_and_move(data,1);
                UDRE=wb.extract_rtcm_data_and_move(data,2);
                SV_ID=wb.extract_rtcm_data_and_move(data,5);
                if SV_ID == 0 :
                    SV_ID=32

                DPRC=RTCM2.twos_comp(wb.extract_rtcm_data_and_move(data,24),24)

                if Scale_Factor == 0:
                    DPRC*=0.02
                else:
                    DPRC*=0.32

                IOD=wb.extract_rtcm_data_and_move(data,8)
                finished=wb.word()==(length+2)

                self.SV_Details.append({'SV': SV_ID,'UDRE': UDRE, 'IOD':IOD,'DPRC':DPRC, 'Scale_Factor': Scale_Factor})

            return Got_Packet



    def dump(self,dump):
#        print "Time: {}".format(self.GNSS_Time)

        print "Number SV's: {} ".format(self.SVs)
        print " SV UDRE IOD    DPRC   Scale Factor"
        for SV in range(self.SVs):
            print "{:3} {} {:3} {:6.2f} {}".format(self.SV_Details[SV]['SV'], RTCM2_UDRE_Names(self.SV_Details[SV]['UDRE']),self.SV_Details[SV]['IOD'],self.SV_Details[SV]['DPRC'],self.SV_Details[SV]['Scale_Factor'])

        #pprint.pprint (self.SV_Details)

