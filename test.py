
import os.path
import unittest
import random
import magic
from os import path


testfile = [
    ("magic.pyc", "python 2.4 byte-compiled", "application/octet-stream"),
    ("test.pdf", "PDF document, version 1.2", "application/pdf"),
    ("test.gz", 'gzip compressed data, was "test", from Unix, last modified: '
     'Sat Jun 28 18:32:52 2008', "application/x-gzip"),
    ("text.txt", "ASCII text", "text/plain"),
    # is there no better way to encode a unicode literal across python2/3.[01]/3.3?
    ("\xce\xbb".decode('utf-8'), "empty", "application/x-empty")
    ]

testFileEncoding = [('text-iso8859-1.txt', 'iso-8859-1')]

class TestMagic(unittest.TestCase):

    mime = False
    
    def setUp(self):
        self.m = magic.Magic(mime=self.mime)

    def testFileTypes(self):
        for filename, desc, mime in testfile:
            filename = path.join(path.dirname(__file__),
                                 "testdata",
                                 filename)
            if self.mime:
                target = mime
            else:
                target = desc
                
            snippet = open(filename, 'rb').read(1024)
            
            # do this rather than b"" literals since those aren't supported in 2.4
            target_bytes = target.encode('utf-8')
            self.assertEqual(target_bytes, self.m.from_buffer(snippet))
            self.assertEqual(target_bytes, self.m.from_file(filename), filename)

            self.assertEqual(target_bytes, magic.from_buffer(snippet, mime=self.mime))
            self.assertEqual(target_bytes, magic.from_file(filename, mime=self.mime), 
                             filename)
        

    def testErrors(self):
        self.assertRaises(IOError, self.m.from_file, "nonexistent")
        self.assertRaises(IOError, lambda: magic.from_file("nonexistent", mime=self.mime))

        self.assertRaises(magic.MagicException, magic.Magic, magic_file="noneexistent")
        os.environ['MAGIC'] = '/nonexistent'
        self.assertRaises(magic.MagicException, magic.Magic)
        del os.environ['MAGIC']

class TestMagicMime(TestMagic):
    mime = True

class TestMagicMimeEncoding(unittest.TestCase):
    def setUp(self):
        self.m = magic.Magic(mime_encoding=True)

    def testFileEncoding(self):
        for filename, encoding in testFileEncoding:
            filename = path.join(path.dirname(__file__),
                                 "testdata",
                                 filename)
            snippet = open(filename, 'rb').read(1024)
            
            self.assertEqual(encoding, self.m.from_buffer(snippet))
            self.assertEqual(encoding, self.m.from_file(filename), filename)

if __name__ == '__main__':
    unittest.main()
    
