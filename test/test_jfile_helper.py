import jfile_helper
import unittest
import logging
logger=logging.getLogger(__name__)

class JFileHelperTest(unittest.TestCase):
    def test_get_latest_file(self):
        result_file= jfile_helper.get_latest_file()
        logger.info('Result File: %s', result_file)
        self.assertIsNotNone(result_file)
