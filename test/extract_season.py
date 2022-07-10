import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from renamer.get_season import get_season



examples_set = """
[Fansub] Foo Spam Egg Bacon - 96 (1080P 10bit) (Season 5 - 08).mkv
[Fansub] Egg Adventure (2020) - S01E49 [1080p][HEVC x265 10bit][Multi-Subs] (Weekly)
1 [Fansub] Spam! Egg-kun S02E06 [1080p] [HEVC WEBRip] (Bacon spam egg Bacon! Egg-kun 2nd Season)
[Fansub] One Egg - 975 [480p].mkv
[Fansub] Egg Adventure (2020) - 49 [480p].mkv
[Fansub] One Egg - 975 [720p].mkv
2 [Fansub] Tropical-spam! Prebaked - 13 (1080p).mkv
1 [Fansub] Tropical-spam! Prebaked - 13 (720p).mkv
[Fansub] Egg Adventure (2020) - 49 [720p].mkv
4 [Fansub] One Egg - 975 [1080p][HEVC x265 10bit][Multi-Subs] (Weekly)
Egg.Adventure.2020.S01E49.1080p.WEBRip.x264-Rapta
One Egg - 975 [1080p HEVC x265 10Bit][AAC]
One Egg - 975 [1080p].mkv
Egg Adventure (2020) - 49 [1080p HEVC x265 10Bit][AAC]
Egg Adventure (2020) - 49 [1080p].mkv
Tropical-spam! Precure - 13 [480p].mkv
Str@ng3 First Egg [1080p] [Tri Audio] [VRV] [V2]
Str@ng3 First Egg [720p] [Tri Audio] [VRV] [V2]
Tropical-Rouge! Precure - 13 [720p].mkv
Foo Spam Egg Bacon (Saison 4) - 20 VOSTFR.mp4
Foo Spam Egg Bacon (Season 4) - 10 VOSTFR.mp4
Foo Spam Egg Bacon (Saison-4) - 21 VOSTFR.mp4
Foo Spam Egg Bacon (Season.4) - 42 VOSTFR.mp4
Foo Spam Egg Bacon (Saison-4) - 57 VOSTFR.mp4
Foo Spam Egg Bacon (Season 4) - 1 VOSTFR.mp4
"""

expected_result = [(0, 0),
                   (5, 8),
                   (1, 49),
                   (2, 6),
                   (1, 975),
                   (1, 49),
                   (1, 975),
                   (1, 13),
                   (1, 13),
                   (1, 49),
                   (1, 975),
                   (1, 49),
                   (1, 975),
                   (1, 975),
                   (1, 49),
                   (1, 49),
                   (1, 13),
                   (1, 1),
                   (1, 1),
                   (1, 13),
                   (1, 20),
                   (1, 10),
                   (1, 21),
                   (1, 42),
                   (1, 57),
                   (1, 1)
                   ]


class TestGetSeason(unittest.TestCase):

    def test_multiple_test(self):
        examples = examples_set.split('\n')[1:]
        assert(len(examples) == len(expected_result)
               ), f"Expected Result not same size with example set {len(examples)} {len(expected_result)}"
        for i in range(len(examples)):
            self.assertEqual(get_season(
                examples[i]), expected_result[i], f"Did not get expected result for {examples[i]}, got {expected_result[i]}")


if __name__ == '__main__':
    unittest.main()
