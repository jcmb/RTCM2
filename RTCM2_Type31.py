# RTCM2_Type1

from RTCM2_Decls import *
import RTCM2
from bitField import bf
import pprint


class Type31 (RTCM2_Message):
    def __init__(self):
        self.Packet_ID=1
        self.SVs=None

    def decode(self,length,data):
        if (length < 1):
            return Decode_Error
        else :
            self.SV_Details=[]
            self.SVs=0
            wb = RTCM2.word_bit(3,1)
            finished=False
#            pprint.pprint(data)
#            print "Length: " + str(length+2)

            while not finished:
                self.SVs+=1
#                print "SV: " + str(self.SVs)
                Scale_Factor=wb.extract_rtcm_data_and_move(data,1);
                UDRE=wb.extract_rtcm_data_and_move(data,2);
                SV_ID=wb.extract_rtcm_data_and_move(data,5);
                if SV_ID == 0 :
                    SV_ID=32
                PRC=wb.extract_rtcm_data_and_move(data,16)
                PRC=RTCM2.twos_comp(PRC,16)
                RRC=RTCM2.twos_comp(wb.extract_rtcm_data_and_move(data,8),8)

                if Scale_Factor == 0:
                    PRC*=0.02
                    RRC*=0.02
                else:
                    PRC*=0.32
                    RRC*=0.32

                Change=wb.extract_rtcm_data_and_move(data,1)
                TOD=wb.extract_rtcm_data_and_move(data,7)
                finished=wb.word()>=(length+2)
#                print "Word: " +str(wb.word()) + " Bit: " + str(wb.bit())

                self.SV_Details.append({'SV': SV_ID,'UDRE': UDRE, 'Change' : Change,'TOD':TOD,'PRC':PRC, 'RRC':RRC, 'Scale_Factor': Scale_Factor})

            return Got_Packet



    def dump(self,dump):
#        print "Time: {}".format(self.GNSS_Time)

        print "Number SV's: {} ".format(self.SVs)
        print " SV UDRE TOD Change    PRC    RRC Scale Factor"
        for SV in range(self.SVs):
            print "{:3} {} {:3} {:6.0f} {:6.2f} {:6.2f} {:1.0f}".format(self.SV_Details[SV]['SV'],RTCM2_UDRE_Names[self.SV_Details[SV]['UDRE']],self.SV_Details[SV]['TOD'],self.SV_Details[SV]['Change'],self.SV_Details[SV]['PRC'],self.SV_Details[SV]['RRC'],self.SV_Details[SV]['Scale_Factor'])

        #pprint.pprint (self.SV_Details)

