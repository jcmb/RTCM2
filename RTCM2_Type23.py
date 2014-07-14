# RTCM2_Type23

from RTCM2_Decls import *
import RTCM2
from bitField import bf

class Type23 (RTCM2_Message):
    def __init__(self):

        self.Packet_ID=23
        self.ARP_Ant_Height_Following=None
        self.Serial_Included=None
        self.Antenna_Length=None
        self.Antenna_Name=None
        self.Setup_ID=None
        self.Serial_Length=None
        self.Serial=None

    def decode(self,length,data):
        if (length < 3):
            return Decode_Error
        else :
            self.ARP_Ant_Height_Following=RTCM2.extract_rtcm_bits(data[3],2,2)
            self.Serial_Included=RTCM2.extract_rtcm_bits(data[3],3,3)
            self.Antenna_Length=RTCM2.extract_rtcm_bits(data[3],4,8)
            current_word=3
            chars_in_word=2
            chars_left=self.Antenna_Length;

            self.Antenna_Name=""
            while chars_left > 0:
                self.Antenna_Name+=chr(RTCM2.extract_rtcm_bits(data[current_word],25-(chars_in_word*8),25-(chars_in_word*8)+7))
                chars_in_word-=1
                if chars_in_word == 0:
                    chars_in_word=3
                    current_word+=1
                chars_left-=1

            self.Setup_ID=RTCM2.extract_rtcm_bits(data[current_word],25-(chars_in_word*8),25-(chars_in_word*8)+7)
            chars_in_word-=1
            if chars_in_word == 0:
                chars_in_word=3
                current_word+=1

            self.Serial_Length=RTCM2.extract_rtcm_bits(data[current_word],25-(chars_in_word*8)+3,25-(chars_in_word*8)+4)
            chars_in_word-=1
            if chars_in_word == 0:
                chars_in_word=3
                current_word+=1

            self.Serial=""
            chars_left=self.Serial_Length

            while chars_left > 0:
                self.Serial+=chr(RTCM2.extract_rtcm_bits(data[current_word],25-(chars_in_word*8),25-(chars_in_word*8)+7))
                chars_in_word-=1
                if chars_in_word == 0:
                    chars_in_word=3
                    current_word+=1
                chars_left-=1
            return Got_Packet



    def dump(self,dump):

        if self.ARP_Ant_Height_Following:
            print " ARP Antenna Height: Following"
        else :
            print " ARP Antenna Height: Not Following"


        print " Name : " + self.Antenna_Name
        print " Setup ID : " + str(self.Setup_ID)

        if self.Serial_Included:
            print " Serial : " + self.Serial
        else :
            print " Serial : Not included"

