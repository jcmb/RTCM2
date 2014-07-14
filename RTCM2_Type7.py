# RTCM2_Type7

from RTCM2_Decls import *
import RTCM2
from bitField import bf
import pprint

Type7_Health_Names=(
    "Radiobeacon Operation Normal",
    "No Integrity Monitor Operating",
    "No information available",
    "Don't Use this Radiobeacon")

Type7_Modulation_Names=(
    'MSK',
    'FSK'
    )

Type7_Sync_Names=(
    'Asynchronous',
    'Synchronous'
    )

Type7_Coding_Names=(
    'No Added Coding',
    'FEC'
    )

Type7_Rate_Names=(
    '25  bits/sec',
    '50  bits/sec',
    '100 bits/sec',
    '110 bits/sec',
    '150 bits/sec',
    '200 bits/sec',
    '250 bits/sec',
    '300 bits/sec')


class Type7 (RTCM2_Message):
    def __init__(self):
        self.Packet_ID=7
        self.Beacons=None

    def decode(self,length,data):
        if (length < 1):
            return Decode_Error
        else :
            self.SV_Details=[]
            self.SVs=0

            wb = RTCM2.word_bit(3,1)
            finished=False

            while not finished:
                self.Beacons+=1
                Latitude=RTCM2.twos_comp(wb.extract_rtcm_data_and_move(data,16),16);
                Longitude=RTCM2.twos_comp(wb.extract_rtcm_data_and_move(data,16),16);
                Range=wb.extract_rtcm_data_and_move(data,10);
                Freq=wb.extract_rtcm_data_and_move(data,12)*100 + 190;
                Health=wb.extract_rtcm_data_and_move(data,2);
                Station_ID=wb.extract_rtcm_data_and_move(data,10);
                Bit_Rate=wb.extract_rtcm_data_and_move(data,3);
                Modulation=wb.extract_rtcm_data_and_move(data,1);
                Sync_type=wb.extract_rtcm_data_and_move(data,1);
                Coding=wb.extract_rtcm_data_and_move(data,1);

                finished=wb.word()==(length+2)

                self.SV_Details.append({'Beacon': Station_ID,'Lat': Latitude, 'Long':Longitude,'Range':Range, 'Freq':Freq,'Health':Health,'BitRate':Bit_Rate,'Modulation':Modulation,'Sync_type':Sync_type,'Coding':Coding})

            return Got_Packet



    def dump(self,dump):
#        print "Time: {}".format(self.GNSS_Time)

        print "Number Beacon's: {} ".format(self.SVs)
        print " Beacon Lat Long Range (km) Freq (kHz)   Bit Rate Modulation Syncronization Coding"
        for SV in range(self.SVs):
            print "{:3} {} {:3} {:6.2f} {} {}".format(self.SV_Details[SV]['Beacon'],self.SV_Details[SV]['Lat'],self.SV_Details[SV]['Long'],self.SV_Details[SV]['Range'],self.SV_Details[SV]['Freq'],Type7_Health_Names(self.SV_Details[SV]['Health']),Type7_Rate_Names(self.SV_Details[SV]['BitRate']),Type7_Modulation_Names(self.SV_Details[SV]['Modulation']),Type7_Sync_Names(self.SV_Details[SV]['Sync_type']),Type7_Coding_Names(self.SV_Details[SV]['Coding']))

        #pprint.pprint (self.SV_Details)

