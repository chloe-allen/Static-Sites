import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multi_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), ![image2](https://i.imgur.com/zjjcJKZZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZZ.png")], matches)

    def test_extract_markdown_no_images(self):
        matches = extract_markdown_images("This is text only")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_multi_links(self):
        matches = extract_markdown_links("This is text with a [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    
    def test_extract_markdown_no_links(self):
        matches = extract_markdown_links("This is text with no link")
        self.assertListEqual([], matches)