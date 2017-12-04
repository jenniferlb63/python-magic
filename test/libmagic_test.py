# coding: utf-8

import unittest

import magic


class MagicTestCase(unittest.TestCase):

    filename = 'test/testdata/test.pdf'
    expected_mime_type = 'application/pdf'
    expected_encoding = 'us-ascii'
    expected_name = 'PDF document, version 1.2'

    def assert_result(self, result):
        self.assertEqual(result.mime_type, self.expected_mime_type)
        self.assertEqual(result.encoding, self.expected_encoding)
        self.assertEqual(result.name, self.expected_name)

    def test_detect_from_filename(self):
        result = magic.detect_from_filename(self.filename)
        self.assert_result(result)

    def test_detect_from_fobj(self):
        with open(self.filename) as fobj:
            result = magic.detect_from_fobj(fobj)
        self.assert_result(result)

    def test_detect_from_content(self):
        with open(self.filename) as fobj:
            result = magic.detect_from_content(fobj.read(4096))
        self.assert_result(result)

if __name__ == '__main__':
    unittest.main()
