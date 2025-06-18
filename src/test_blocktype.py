import unittest
from blocktype import BlockType, block_to_block_type

class TestBlockType(unittest.TestCase):
    def test_code_block(self):
        md = "```\nprint('Hello!')\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_quote_block(self):
        md = "> This is first quote\n> This is second quote"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_unordered_block(self):
        md = "- item1\n- item2"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_ordered_block(self):
        md = "1. item1\n2. item2"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)
    
    def test_heading_block(self):
        md = "#### This is heading"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)

    def test_negative_block(self):
        md = "This is just a paragraph"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    