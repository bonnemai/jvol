from jfile import JFile
import unittest
import logging
logger=logging.getLogger(__name__)

class JFileTest(unittest.TestCase):
    def test_jfile1(self):
        jf=JFile(region='DEV', indices=['NKY'])
        self.assertIsNotNone(jf)
        logger.info(jf.results['NKY'])
        print(jf.results['NKY'])

        vol_value=jf.get_vol_value(strike=12000, expiry='7Dec18')
        logger.info(vol_value)
        self.assertIsNotNone(vol_value)
        self.assertEqual(10, vol_value, 'Should be equal to 10')
