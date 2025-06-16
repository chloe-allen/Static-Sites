import unittest
from main import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_only_whitespace(self):
        md = "\n   \n\n  \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_block(self):
        md = "This is just one block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is just one block"])

    def test_double_block(self):
        md = "First block\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_mutiline_block(self):
        md = "Paragraph line one\nParagraph line two\n\nAnother block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph line one\nParagraph line two", "Another block"])



if __name__ == "__main__":
    unittest.main()