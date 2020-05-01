"""
The various testing _tg_utilities
"""
import os


class TestUtils:
    """ The testing utilities class """
    
    @staticmethod
    def tfn(file_name):
        return TestUtils.test_file_name(file_name)

    @staticmethod
    def test_file_name(file_name):
        dirname = os.path.dirname(__file__)
        abspath = os.path.join(dirname, '../testdata/' + file_name)
        return os.path.relpath(abspath)
