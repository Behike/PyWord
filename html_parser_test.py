import unittest
from html_parser import chapter_finder, capitalize_sentences

class TestHtmlParser(unittest.TestCase):
    def test_chapter_finder(self):
        # Test valid chapter
        self.assertTrue(chapter_finder("Chapter 1: Introduction"))
        self.assertTrue(chapter_finder("Chapter 2.1: Getting Started"))
        self.assertTrue(chapter_finder("Chapter One: Introduction"))
        self.assertTrue(chapter_finder("Chapter Two: Getting Started"))
        self.assertTrue(chapter_finder("1. Introduction"))
        self.assertTrue(chapter_finder("2.1 Getting Started"))
        self.assertTrue(chapter_finder("1."))
        self.assertTrue(chapter_finder("2."))

        # Test invalid chapter
        self.assertFalse(chapter_finder("This is not a chapter"))
        self.assertFalse(chapter_finder("Chapter"))
        self.assertFalse(chapter_finder("Chapter Introduction"))
        self.assertFalse(chapter_finder("Chapter 1 Introduction"))
        self.assertFalse(chapter_finder("Chapter 1. Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1 Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1. Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1 Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1. Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1 Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1. Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1.1 Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1.1. Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1.1.1 Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1.1.1. Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1.1.1.1 Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1.1.1.1. Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1.1.1.1.1 Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1.1.1.1.1. Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1.1.1.1.1.1 Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1.1.1.1.1.1. Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1.1.1.1.1.1.1 Introduction"))
        self.assertFalse(chapter_finder("Chapter 1.1.1.1.1.1.1.1.1.1. Introduction"))

    def test_capitalize_sentences(self):
        # Test capitalize_sentences function
        self.assertEqual(capitalize_sentences("this is a sentence."), "This Is a Sentence.")
        self.assertEqual(capitalize_sentences("this is a sentence. this is another sentence."), "This Is a Sentence. This is another sentence.")
        self.assertEqual(capitalize_sentences("this is a sentence. This is another sentence."), "This is a sentence. This is another sentence.")
        self.assertEqual(capitalize_sentences("this is a sentence. This is another sentence. THIS IS A THIRD SENTENCE."), "This is a sentence. This is another sentence. THIS IS A THIRD SENTENCE.")
        self.assertEqual(capitalize_sentences("this is a sentence. This is another sentence. THIS IS A THIRD SENTENCE. this is a fourth sentence."), "This is a sentence. This is another sentence. THIS IS A THIRD SENTENCE. This is a fourth sentence.")
        self.assertEqual(capitalize_sentences("this is a sentence. This is another sentence. THIS IS A THIRD SENTENCE. this is a fourth sentence. THIS IS A FIFTH SENTENCE."), "This is a sentence. This is another sentence. THIS IS A THIRD SENTENCE. This is a fourth sentence. THIS IS A FIFTH SENTENCE.")
        self.assertEqual(capitalize_sentences("this is a sentence. This is another sentence. THIS IS A THIRD SENTENCE. this is a fourth sentence. THIS IS A FIFTH SENTENCE. this is a sixth sentence."), "This is a sentence. This is another sentence. THIS IS A THIRD SENTENCE. This is a fourth sentence. THIS IS A FIFTH SENTENCE. This is a sixth sentence.")


if __name__ == "__main__":
    unittest.main()
