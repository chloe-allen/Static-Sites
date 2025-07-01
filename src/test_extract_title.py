import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
       md = "# Hello"
       self.assertEqual(extract_title(md), "Hello") 

    def test_extract_no_title(self):
         with self.assertRaises(ValueError):
              extract_title("No title here")

if __name__ == "__main__":
    unittest.main()




 