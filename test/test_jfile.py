from jfile import JFile
import unittest
import logging
logger=logging.getLogger(__name__)

class JFileTest(unittest.TestCase):
    def test_jfile1(self):
        jf=JFile(region='DEV')
        self.assertIsNotNone(jf)
        logger.info(jf.results['NKY'])
        print(jf.results['NKY'])