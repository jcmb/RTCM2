import unittest
from RTCM2 import word_bit
from bitField import bf
import pprint


class TestBitField(unittest.TestCase):

    def setUp(self):
        self.data_zero=[]
        self.data_1=[]

        for i in range(10):
            self.data_zero.append(bf(0,32))
            self.data_1.append(bf(0,32))

        self.data_1[5]=bf(0x123456<<6,30)
        self.data_1[6]=bf(0x345678<<6,30)


#        for i in range(10):
#            print self.data_power[i]


    def test_default(self):
        # make sure the shuffled sequence does not lose any elements
        k = word_bit()
        self.assertIsInstance(k,word_bit)
        self.assertEqual(int(k.word()), 3)
        self.assertEqual(int(k.bit()), 1)

    def test_word_4(self):
        # make sure the shuffled sequence does not lose any elements
        k = word_bit(4)
        self.assertIsInstance(k,word_bit)
        self.assertEqual(int(k.word()), 4)
        self.assertEqual(int(k.bit()), 1)

    def test_word_5_bit_8(self):
        # make sure the shuffled sequence does not lose any elements
        k = word_bit(5,8)
        self.assertIsInstance(k,word_bit)
        self.assertEqual(int(k.word()), 5)
        self.assertEqual(int(k.bit()), 8)

    def test_word_add_within_word(self):
        # make sure the shuffled sequence does not lose any elements
        k = word_bit(5,1)
        self.assertIsInstance(k,word_bit)
        self.assertEqual(int(k.word()), 5)
        self.assertEqual(int(k.bit()), 1)

        k.addbits(3)
        self.assertEqual(int(k.word()), 5)
        self.assertEqual(int(k.bit()), 4)

        k.addbits(13)
        self.assertEqual(int(k.word()), 5)
        self.assertEqual(int(k.bit()), 17)

        k.addbits(7)
        self.assertEqual(int(k.word()), 5)
        self.assertEqual(int(k.bit()), 24)

        k.addbits(1)
        self.assertEqual(int(k.word()), 6)
        self.assertEqual(int(k.bit()), 1)

        k.addbits(24)
        self.assertEqual(int(k.word()), 7)
        self.assertEqual(int(k.bit()), 1)

        k.addbits(12)
        self.assertEqual(int(k.word()), 7)
        self.assertEqual(int(k.bit()), 13)

    def test_extract_simple(self):
        k = word_bit(5)
        self.assertIsInstance(k,word_bit)
        self.assertEqual(int(k.extract_rtcm_data_and_move(self.data_zero,4)),0)
        self.assertEqual(int(k.word()), 5)
        self.assertEqual(int(k.bit()), 5)

        k = word_bit(5)
        self.assertIsInstance(k,word_bit)

        self.assertEqual(int(k.extract_rtcm_data_and_move(self.data_1,4)),1)
        self.assertEqual(int(k.word()), 5)
        self.assertEqual(int(k.bit()), 5)

        self.assertEqual(int(k.extract_rtcm_data_and_move(self.data_1,4)),2)
        self.assertEqual(int(k.word()), 5)
        self.assertEqual(int(k.bit()), 9)


        self.assertEqual(int(k.extract_rtcm_data_and_move(self.data_1,8)),0x34)
        self.assertEqual(int(k.word()), 5)
        self.assertEqual(int(k.bit()), 17)

        self.assertEqual(int(k.extract_rtcm_data_and_move(self.data_1,8)),0x56)
        self.assertEqual(int(k.word()), 6)
        self.assertEqual(int(k.bit()), 1)

        self.assertEqual(int(k.extract_rtcm_data_and_move(self.data_1,8)),0x34)
        self.assertEqual(int(k.word()), 6)
        self.assertEqual(int(k.bit()), 9)


    def test_extract_split(self):
        k = word_bit(5,22)
        self.assertIsInstance(k,word_bit)
        self.assertEqual(int(k.extract_rtcm_data_and_move(self.data_zero,6)),0)
        self.assertEqual(int(k.word()), 6)
        self.assertEqual(int(k.bit()), 4)

        k = word_bit(5)
        self.assertIsInstance(k,word_bit)

        self.assertEqual(int(k.extract_rtcm_data_and_move(self.data_1,20)),0x12345)
        self.assertEqual(int(k.word()), 5)
        self.assertEqual(int(k.bit()), 21)

        self.assertEqual(int(k.extract_rtcm_data_and_move(self.data_1,8)),0x63)
        self.assertEqual(int(k.word()), 6)
        self.assertEqual(int(k.bit()), 5)

        self.assertEqual(int(k.extract_rtcm_data_and_move(self.data_1,8)),0x45)
        self.assertEqual(int(k.word()), 6)
        self.assertEqual(int(k.bit()), 13)





if __name__ == "__main__":
    unittest.main()
