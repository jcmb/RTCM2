#!/usr/bin/env python

from array import array
from RTCM2_Decls import *
import sys
import pprint
from datetime import datetime
from bitField import bf


import RTCM2_Type1
import RTCM2_Type2
import RTCM2_Type3
import RTCM2_Type7
import RTCM2_Type18
import RTCM2_Type19
import RTCM2_Type22
import RTCM2_Type23
import RTCM2_Type24
import RTCM2_Type27
import RTCM2_Type31
import RTCM2_Type41


# Version 2 Preamble
#POS_VER2_PREAMBLE = bf(0x66,32) <<  22;
#NEG_VER2_PREAMBLE = bf(0x99,32) <<  22;
POS_VER2_PREAMBLE = 0x66;
NEG_VER2_PREAMBLE = 0x99;
RTCM2_Max_Bits = 25;
RTCM2_Max_Words = 31;
RTCM2_N_FLAG_WORDS  = 32;
#  RTCM2_NO_STATION_ID = -1;
RTCM2_MAX_SVS_PER_MSG = 24;
RTCM2_Min_Message_ID = 1;
RTCM2_Max_Station_ID = 1023;


#Tformat_status
NO_INFO=0
MESSAGE_COMPLETE_GOOD_ID=1
MESSAGE_COMPLETE_BAD_ID=2
GOOD_HDR1=3
GOOD_HDR2=4
ERROR_DETECTED=5

#TFraming_Mode =
HDR_WORD1_SRCH=0
HDR_WORD2_CONFIRM=1
DATA_COLLECT=2


parity_table = (
   0x29, 0x16, 0x2a, 0x34,  #* D29*, D30*,   d1,   d2 *)
   0x3b, 0x1c, 0x2f, 0x37,  #*   d3,   d4,   d5,   d6 *)
   0x1a, 0x0d, 0x07, 0x23,  #*   d7,   d8,   d9,  d10 *)
   0x31, 0x38, 0x3d, 0x3e,  #*  d11,  d12,  d13,  d14 *)
   0x1f, 0x0e, 0x26, 0x32,  #*  d15,  d16,  d17,  d18 *)
   0x19, 0x2c, 0x16, 0x0b,  #*  d19,  d20,  d21,  d22 *)
   0x25, 0x13);          #*  d23,  d24  *)

RTCM2_PARITY_D29   = 0x29;    # parity_table[0] */


def extract_rtcm_bits(word,first_rtcm_bit,last_rtcm_bit):
    first_bit=30-last_rtcm_bit
    last_bit=first_bit+(last_rtcm_bit-first_rtcm_bit)+1
#    print "Extract: " + str(first_bit) + ":" + str(last_bit)
#    print type (bf), type(word[first_bit:last_bit])
    return(word[first_bit:last_bit])

def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if( (val&(1L<<(bits-1))) != 0 ):
        val = val - (1<<bits)
    return val

def OutputDebugString(s):
   print s
   sys.stdout.flush()

# Since the packets are alway small, and we have ram we make an list that each item is a single bit. It is also a slow way to do it


class word_bit(object):
    def __init__(self,word=3,bit=1):
        self._word=word
        self._bit=bit

    def word(self):
        return self._word

    def bit(self):
        return self._bit

    def addbits(self,bits):
        self._bit+=bits
        if self._bit>24:
            self._word+=1
            self._bit-=24

    def extract_rtcm_data_and_move(self,data,length):

        end_bit=self._bit+length-1
#        print "Extract"
#        print self._word
#        print self._bit
#        print end_bit
#        print data[self._word]


        if end_bit <= 24 :
            result=extract_rtcm_bits(data[self._word],self._bit,end_bit)
            self._bit+=length
            if self._bit==25:
                self._bit=1
                self._word+=1
        else:
            result=extract_rtcm_bits(data[self._word],self._bit,24)
#            print "Extract: " + str(self._word) + " " + str(self._bit) + " : 24"

            end_bit-=24
            result<<=end_bit # We are getting end_bit bits from the next word, so we need to shift the previous data by the amount we are going to get from this word
            self._word+=1
            result|=extract_rtcm_bits(data[self._word],1,end_bit)

            self._bit=end_bit+1
#        print "Result: " + str(result)
        return result




class RTCM2:
    def __init__ (self,default_output_level):
        self.undecoded=bytearray("")
        self.buffer=bytearray("")
        self.default_output_level=default_output_level
        self.packet_ID=None
        self.packet_Length=None
        self.Dump_Levels=array("I")
        self.Handler=[]

        self.commands={}
        self.last_32_bits=bf(length=32)
        self.bit_count=0
        self.framing_mode = HDR_WORD1_SRCH
        self.frame_locked=False
        self.data=[]
        for i in range(RTCM2_Max_Words):
            self.data.append(0)

        self.word_count=0

        for i in range (RTCM2_Min_Message_ID,RTCM2_Max_Message_ID):
            self.Dump_Levels.append(default_output_level)
            self.Handler.append(None)

        self.Handler[1]=RTCM2_Type1.Type1()
        self.Handler[2]=RTCM2_Type2.Type2()
        self.Handler[3]=RTCM2_Type3.Type3()
        self.Handler[7]=RTCM2_Type7.Type7()
        self.Handler[9]=RTCM2_Type1.Type1() # Type 9 is just type 1 but without all the SV information
        self.Handler[18]=RTCM2_Type18.Type18()
        self.Handler[19]=RTCM2_Type19.Type19()
        self.Handler[22]=RTCM2_Type22.Type22()
        self.Handler[23]=RTCM2_Type23.Type23()
        self.Handler[24]=RTCM2_Type24.Type24()
        self.Handler[27]=RTCM2_Type27.Type27()
        self.Handler[31]=RTCM2_Type31.Type31()
        self.Handler[41]=RTCM2_Type41.Type41()



    def add_data (self,data):
    # Add more received data into the system. Adding data does not mean that we will try and decode it.
        self.buffer+=data
#        print len(self.buffer)
#       print hexlify(self.buffer)


    def compute_gps_parity (self,dataword):

        # * XOR D30* with D1..D24 to yield d1..d24 *)
        if( dataword & 0x40000000) :
          dataword = dataword ^ 0x3fffffc0;
#          OutputDebugString("Parity high bit")

        # * For bits D29* thru d24 calculate the 6 parity bits *)
        parity_sum = 0;

        for Bit_Count in range (0,26) : # 2 bits previous parity + 24 bits data
#           print "Bit Count: " + str(Bit_Count)

#           print ( int(dataword & 0x80000000) )
#           print ( int(dataword & 0x80000000) ) <> 0
#           print ( dataword[31] ) <> 0
#           print dataword

           if ( dataword[31] ) <> 0 :
              parity_sum = parity_sum ^ parity_table[Bit_Count];
           dataword <<= 1;

        return (parity_sum)

    def check_gps_parity (self,dataword):
#        OutputDebugString("Checking Parity")
#        print dataword  & 0x3f

        computed= self.compute_gps_parity( dataword )
        parity = int(dataword & 0x3f )
#        OutputDebugString("Parity: " + str(computed) + " " + str(int(parity)))
        return computed == parity




    def extract_data (self,dataword):
    #///**********************************************************************)
    #///* XORs away the effect of D30* to produce d1..d24. For completeness
    #// * D29*, D30* and D25 thru D30 are set to 0
        if( dataword & 0x40000000 ):
            dataword = ~dataword;
        return dataword & 0x3fffffc0 # //* All non data bits set to 0 *)


    def process_rtcm_byte (self, rtcm_byte):
        good_parity=False;
        format_status=NO_INFO

#        OutputDebugString("Process RTCM Byte Start:  " + "{:02X}".format(rtcm_byte))
#        OutputDebugString('Process RTCM Byte: ' + str(self.framing_mode)+ ' ' + str(self.frame_locked))

        if ((rtcm_byte & 0xC0) <> 0x40) :
            OutputDebugString('Not 6 of 8');
            return NO_INFO;  # Invalid 6 of 8 byte, so give up
        rtcm_byte &= 0x3F

#        OutputDebugString("Process RTCM Start:  " + "{:06b}".format(rtcm_byte))

        for Count in range(6,0,-1): # The low 6 Bits in the byte we care about, we have to make this into a bit stream


            #OutputDebugString("Process RTCM Byte:  " + "{:02X}".format(rtcm_byte) + " " + str(Count))
            self.last_32_bits<<=1; #always shift left 1

            if rtcm_byte & 1 :
                self.last_32_bits[0]=1; #Had a 1 in the byte add to the last_32_bits
            self.bit_count+=1

            #OutputDebugString(str(self.last_32_bits)+ " " + str(self.bit_count));

            rtcm_byte >>=1

            if self.bit_count >= 30:
                self.bit_count=0; # Not convinced that we should reset this here, since it seems wrong in the case that we have a bit stream and are trying to sync
                                  # In practice though we are only working with byte aligned streams, since we bail if the byte doesn't start with 0x40
                self.word_boundary=True;
                good_parity=self.check_gps_parity(self.last_32_bits)
#                OutputDebugString("word_boundary: " + str(good_parity))
                #Need to check if we should bail here or if we have to keep going for the headers
#                if not good_parity:
#                    continue
            else:
                self.word_boundary=False;
                if( self.frame_locked ) :
                    #   In an effort to save throughput, we make use of the
                    #    fact that the switch statement below need only be
                    #    executed on a non-word boundary when frame_locked is FALSE.
                   continue;

            if self.framing_mode == HDR_WORD1_SRCH:

                # If last msg ok, then wait for next word boundary
                if( (not self.frame_locked ) or self.word_boundary ):
                    #OutputDebugString("HDR_WORD1_SRCH");
                    # Look for a valid preamble bit sequence. If one is found, overwrite B30 with the assumed value *)
#                    preamble = self.last_32_bits & 0x3fc00000;
                    preamble = extract_rtcm_bits(self.last_32_bits,1,8)

#                    print preamble, POS_VER2_PREAMBLE, NEG_VER2_PREAMBLE
#                    print preamble==POS_VER2_PREAMBLE, preamble==NEG_VER2_PREAMBLE
#                    print int(preamble)==int(POS_VER2_PREAMBLE), int(preamble)==int(NEG_VER2_PREAMBLE)

                    if( preamble == POS_VER2_PREAMBLE ) :
                        self.last_32_bits[30]=0 # &= (not 0x40000000); # Clear D30* *)
#                        OutputDebugString('Pos Ver Preamble');
                        self.found_RTCMV2_header=True
                    elif( preamble == NEG_VER2_PREAMBLE ) :
                        self.last_32_bits[30]=1 # |= 0x40000000;  # Set D30* *)
#                        OutputDebugString('Neg Ver Preamble');
                        self.found_RTCMV2_header=True
                    else :
                        self.found_RTCMV2_header=False

                if self.found_RTCMV2_header:
#                    OutputDebugString('Found Header');
#                    received_checksum=self.last_32_bits[0:6] # & $3F
                    received_checksum=extract_rtcm_bits(self.last_32_bits,25,30)

                    calced_checksum=self.compute_gps_parity(self.last_32_bits)
                    xor_checksum=received_checksum ^ calced_checksum
#                    OutputDebugString("Checksum: " + "{:02X}".format(xor_checksum))

                    if (xor_checksum == 0x29) :
                        self.last_32_bits ^=  0x80000000; #Don't understand this one at all.
#                        OutputDebugString('Checksum 29 hack used');
                        xor_checksum=0

                    if (xor_checksum == 0 ):
                        self.bit_count=0;
                        self.framing_mode=HDR_WORD2_CONFIRM;
                        self.format_status=GOOD_HDR1
                        self.hdr_word=self.extract_data(self.last_32_bits)
                        self.stn_id = extract_rtcm_bits(self.hdr_word, 15, 24);
#                        print " Stn Id   : " + str(self.stn_id);
                        self.packet_ID = extract_rtcm_bits(self.hdr_word,9,14);
#                        print " Type     : " + str(self.packet_ID)

                    else :
                        self.format_status = ERROR_DETECTED;
                        self.frame_locked = False

            elif self.framing_mode == HDR_WORD2_CONFIRM:
                if ( self.word_boundary ) :
                   if( good_parity ) :
                       self.hdr_word=bf(self.extract_data(self.last_32_bits),30)
#                       OutputDebugString('HDR Word2 CONFIRM Good Parity');
                       self.frame_locked = True;
                       # Extract fields for word 2 of the message header *)
                       self.zcount  = int(extract_rtcm_bits( self.hdr_word, 1, 13 ));
                       self.sqn_num = int(extract_rtcm_bits( self.hdr_word, 14, 16 ));
                       self.length  = int(extract_rtcm_bits( self.hdr_word, 17, 21 ));
                       self.health  = int(extract_rtcm_bits( self.hdr_word, 22, 24 ));

                       # Handle the 0 length message case eg :- Type 6 *)
                       if( self.length == 0 ) :
                          self.framing_mode = HDR_WORD1_SRCH;
                          format_status  = MESSAGE_COMPLETE_GOOD_ID;
                       else:
                          self.framing_mode = DATA_COLLECT;
#                          OutputDebugString('HDR Word2 going to Data Collect');
                          format_status = GOOD_HDR2;
                          self.word_count = 0;
                   else :
                      self.frame_locked = False;
                      self.framing_mode = HDR_WORD1_SRCH;
                      format_status  = ERROR_DETECTED;

            elif self.framing_mode == DATA_COLLECT:
                if ( self.word_boundary ) :
                   if( good_parity ) :
#                       OutputDebugString('Data Collect: ' + str(self.word_count) + " " + str(self.length));
                       self.data[self.word_count+3] = self.extract_data(self.last_32_bits)
                       self.word_count+=1

                       if( self.word_count >= self.length ):
                   # This word completes the message. Perform the message termination work. *)
                           self.framing_mode = HDR_WORD1_SRCH;
                           self.bit_count = 0;
                           format_status  = MESSAGE_COMPLETE_GOOD_ID;
#                           OutputDebugString("Message Complete")
                           return format_status

                   else:
                     # A bad data word has been received. Reset data collection. *)
                       self.framing_mode = HDR_WORD1_SRCH;
                       self.frame_locked = False;
                       format_status  = ERROR_DETECTED;
        return format_status

    def process_data (self, dump_decoded=False):

#        if len (self.buffer) <  RTCM2_Min_Size :
#            print "To short"
#            return Need_More

#        OutputDebugString('Process Data start');
        result=0

        while len(self.buffer) and (not result):
            result=self.process_rtcm_byte (self.buffer[0])
            del(self.buffer[0])


#        OutputDebugString('Process Data end');
        if result == NO_INFO:
            return Need_More
        elif result == GOOD_HDR1:
            return Need_More
        elif result == GOOD_HDR2:
            return Need_More
        elif result == MESSAGE_COMPLETE_GOOD_ID:
            if self.Handler[self.packet_ID]:
                return self.Handler[self.packet_ID].decode(self.length,self.data)
            else:
                return Got_Packet
        else:
            return Decode_Error



    def dump (self,dump_undecoded=False,dump_decoded=False,dump_timestamp=False,dump_header=False):


        if self.Dump_Levels[self.packet_ID] :
            print "***********************************************************"
            if dump_timestamp :
               print datetime.now()

            print RTCM2_Message_Names[self.packet_ID] + " ("+ str(self.packet_ID) +")"
            if dump_header:
                print(' Zcount   : '+ str(self.zcount));
                print(' Length   : '+ str(self.length));
                print(' Sequence : '+ str(self.sqn_num));
                print(' Health   : '+ RTCM2_Health_Names[self.health])


            if self.Handler[self.packet_ID]:
                self.Handler[self.packet_ID].dump(self.Dump_Levels[self.packet_ID])
            else :
                print "!Undecoded packet"
                if dump_undecoded:
                    for word in range (3,self.length+3):
                        print "{:2} ".format(word) + str(bf(extract_rtcm_bits(self.data[word],1,24),24))



#        self.Handlers[self.packet_ID].dump(self.Dump_Levels[self.packet_ID]);


    def name (self):
        return str(self.packet_ID)

