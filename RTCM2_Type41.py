# RTCM2_Type41

from RTCM2_Decls import *
import RTCM2
from bitField import bf
import pprint

class Type41 (RTCM2_Message):
    def __init__(self):
        self.Packet_ID=41
        self.GNSS_System=None
        self.GNSS_Signal=None
        self.SV_Ephemeris=None
        self.Use=None
        self.Iono_Included=None
        self.SVs=None

    def decode(self,length,data):
        if (length < 1):
            return Decode_Error
        else :

            self.SV_Details=[]
            self.GNSS_System=RTCM2.extract_rtcm_bits(data[3],1,4)
            self.GNSS_Signal=RTCM2.extract_rtcm_bits(data[3],5,8)
            self.SV_Ephemeris=RTCM2.extract_rtcm_bits(data[3],9,10)
            self.Use=RTCM2.extract_rtcm_bits(data[3],11,12)
            self.Iono_Included=RTCM2.extract_rtcm_bits(data[3],13,13)

            self.SVs=0
            wb = RTCM2.word_bit(3,14)
            finished=False

            while not finished:
                self.SVs+=1
                SV_ID=wb.extract_rtcm_data_and_move(data,6);
                UDRE=wb.extract_rtcm_data_and_move(data,4);
                if self.GNSS_System == 3 :
                    # print "GNSS_System: Galileo"
                    IOD=wb.extract_rtcm_data_and_move(data,10);
                else:
                    IOD=wb.extract_rtcm_data_and_move(data,8);
                PRC=RTCM2.twos_comp(wb.extract_rtcm_data_and_move(data,14),14)/50.0
                if self.Iono_Included :
                    IONO=wb.twos_comp(wb.extract_rtcm_data_and_move(data,12),12)/50.0
                else:
                    IONO=None
                finished=wb.word()==(length+2)

                self.SV_Details.append({'SV': SV_ID,'UDRE': UDRE, 'IOD':IOD,'PRC':PRC, 'IONO':IONO})

            return Got_Packet



    def dump(self,dump):
#        print "Time: {}".format(self.GNSS_Time)

        if self.Use == 0 :
            print "Max Correction Usage: 15 (Seconds)"
        elif self.Use == 1 :
            print "Max Correction Usage: 30 (Seconds)"
        elif self.Use == 2 :
            print "Max Correction Usage: 60 (Seconds)"
        else:
            print "Max Correction Usage: 120 (Seconds)"

        if self.GNSS_System == 1 :
            print "GNSS System: GPS"

            if self.GNSS_Signal == 1 :
               print "GNSS Signal: L1 C/A"
            elif self.GNSS_Signal == 2 :
               print "GNSS Signal: L1 P"
            elif self.GNSS_Signal == 3:
               print "GNSS Signal: L1 C"
            elif self.GNSS_Signal == 4 :
               print "GNSS Signal: L2 C"
            elif self.GNSS_Signal == 5 :
               print "GNSS Signal: L2 P"
            elif self.GNSS_Signal == 6 :
               print "GNSS Signal: L5"
            else:
               print "GNSS Signal: Reserved (" + str(self.GNSS_Signal) +')'

            if self.SV_Ephemeris == 0:
                print "GNSS Ephemeris: NAV"
            elif self.SV_Ephemeris == 1:
                print "GNSS Ephemeris: L2 CNAV"
            elif self.SV_Ephemeris == 2:
                print "GNSS Ephemeris: L5 CNAV"
            else :
                print "GNSS Ephemeris: Reserved (" + str(self.GNSS_Signal) +')'


        elif self.GNSS_System == 2 :
            print "GNSS_System: GLONASS"

            if self.GNSS_Signal == 1 :
               print "GNSS Signal: G1 C/A"
            elif self.GNSS_Signal == 2 :
               print "GNSS Signal: G1 P"
            elif self.GNSS_Signal == 3:
               print "GNSS Signal: G2 C/A"
            elif self.GNSS_Signal == 4 :
               print "GNSS Signal: G2 P"
            else:
               print "GNSS Signal: Reserved (" + str(self.GNSS_Signal) +')'

            if self.SV_Ephemeris == 0:
                print "GNSS Ephemeris: L1?"
            else :
                print "GNSS Ephemeris: Reserved (" + str(self.GNSS_Signal) +')'


        elif self.GNSS_System == 3 :
            print "GNSS_System: Galileo"

            if self.GNSS_Signal == 1 :
               print "GNSS Signal: E5a"
            elif self.GNSS_Signal == 2 :
               print "GNSS Signal: E5b"
            elif self.GNSS_Signal == 3:
               print "GNSS Signal: E5ab"
            elif self.GNSS_Signal == 4 :
               print "GNSS Signal: E6-A"
            elif self.GNSS_Signal == 5 :
               print "GNSS Signal: E6-BC"
            elif self.GNSS_Signal == 6 :
               print "GNSS Signal: E1-A"
            elif self.GNSS_Signal == 7 :
               print "GNSS Signal: E1-BC"
            else:
               print "GNSS Signal: Reserved (" + str(self.GNSS_Signal) +')'

            if self.SV_Ephemeris == 0:
                print "GNSS Ephemeris: C/NAV"
            elif self.SV_Ephemeris == 1:
                print "GNSS Ephemeris: F/NAV"
            elif self.SV_Ephemeris == 2:
                print "GNSS Ephemeris: I/NAV"
            else :
                print "GNSS Ephemeris: Reserved (" + str(self.GNSS_Signal) +')'


        elif self.GNSS_System == 4 :
            print "GNSS_System: SBAS"

            if self.GNSS_Signal == 1 :
               print "GNSS Signal: GPS L1"
            elif self.GNSS_Signal == 2 :
               print "GNSS Signal: GPS L5"
            else:
               print "GNSS Signal: Reserved (" + str(self.GNSS_Signal) +')'

            if self.SV_Ephemeris == 0:
                print "GNSS Ephemeris: Type 9"
            else :
                print "GNSS Ephemeris: Reserved (" + str(self.GNSS_Signal) +')'


        elif self.GNSS_System == 5 :
            print "GNSS_System: QZSS"

            if self.GNSS_Signal == 1 :
               print "GNSS Signal: L1 C-A"
            elif self.GNSS_Signal == 2 :
               print "GNSS Signal: L1C"
            elif self.GNSS_Signal == 3:
               print "GNSS Signal: L2C"
            elif self.GNSS_Signal == 4 :
               print "GNSS Signal: L5"
            elif self.GNSS_Signal == 5 :
               print "GNSS Signal: L1-SAIF"
            elif self.GNSS_Signal == 6 :
               print "GNSS Signal: LEX"
            else:
               print "GNSS Signal: Reserved (" + str(self.GNSS_Signal) +')'

            if self.SV_Ephemeris == 0:
                print "GNSS Ephemeris: NAV"
            elif self.SV_Ephemeris == 1:
                print "GNSS Ephemeris: CNAV"
            elif self.SV_Ephemeris == 2:
                print "GNSS Ephemeris: CNAV2"
            else :
                print "GNSS Ephemeris: Reserved (" + str(self.GNSS_Signal) +')'


        else:
            print "GNSS_System: Reserved (" + str(self.GNSS_Signal) +')'

        print "Iono Present: {}".format(self.Iono_Included)

        print "Number SV's: {} ".format(self.SVs)
        print " SV UDRE IOD    PRC IONO"
        for SV in range(self.SVs):
            print "{:3} {:4} {:3} {:6.2f} {}".format(self.SV_Details[SV]['SV'],self.SV_Details[SV]['UDRE'],self.SV_Details[SV]['IOD'],self.SV_Details[SV]['PRC'],self.SV_Details[SV]['IONO'])

        #pprint.pprint (self.SV_Details)

