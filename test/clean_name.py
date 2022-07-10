import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from renamer.clean import clean_name



class TestClean(unittest.TestCase):

    def test_remove_plus(self):
        example_str = "Foo+bar+Egg+Spam+(Bacon+pan+bread+Honey)+-+18+VOSTFR.mp4"
        self.assertEqual(clean_name(example_str),
                         "Foo bar Egg Spam", "Bad cleaning for +")

    def test_redundant_spaces(self):
        example_str = "Foo         bar   Egg Spam   Bacon.mp4"
        self.assertEqual(clean_name(
            example_str), "Foo bar Egg Spam Bacon", "Bad cleaning for redundant spaces")

    def test_extensions(self):
        extensions = ['avi', 'ext', 'mkv', 'mp4', 'foo']
        base_example = "Foo"
        for extension in extensions:
            self.assertEqual(clean_name(base_example+"."+extension),
                             base_example, "Bad cleaning for extension")

    def test_bracket_n_parenthesis(self):
        middle_words = ['Bacon', 'Spam', 'Egg', 'Str@ng_Words']
        base_example = "Foo"
        for middle_word in middle_words:
            self.assertEqual(clean_name(base_example+"("+middle_word+")" +
                             ".mp4"), base_example, "Bad cleaning for extension")
            self.assertEqual(clean_name(
                base_example+"{"+middle_word+"}"+".mp4"), base_example, "Bad cleaning for extension")

    def test_various_words(self):
        webs = ['www.subs.net', 'www.hey.net',
                'www.f0oB@rs.com', 'www.eggs_and&_spams.net']
        encodings = ['x264', 'x265', 'h264', 'h265', 'H264', 'H265']
        encodings2 = [f"{x}-bits" for x in (8, 10)]+[f"{x}-bit" for x in (8, 10)]+[
            f"{x} bit" for x in (8, 10)]
        encodings3 = ['hevc', 'nvenc', 'BLURAY', 'BDrip']
        audioencodings = ['ac3', 'aac']
        subs = ['VOST', 'VOSTFR', 'VF', 'ENG', 'FRENCH']
        qualities = ['480p', '720p', '1080p']
        sets = [webs, encodings, encodings2,
                encodings3, audioencodings, subs, qualities]
        base_example = "Foo"
        for my_set in sets:
            for word in my_set:
                self.assertEqual(clean_name(base_example+" "+word+".mp4"),
                                 base_example, f"Bad cleaning for various {word}")
                self.assertEqual(clean_name(word+" "+base_example+".mp4"),
                                 base_example, f"Bad cleaning for various {word}")


if __name__ == '__main__':
    unittest.main()
