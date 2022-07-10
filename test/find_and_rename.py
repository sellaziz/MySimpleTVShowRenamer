import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from renamer.find_new_name import find_rename



class TestFindRename(unittest.TestCase):

    def test_remove_plus(self):
        example_str = "Monster 54.avi"
        group_dict, sort_dict, ep_dicts, final_dict = find_rename([example_str])
        # final_dicts = {Best_matched_name: {filename:{Season=int,Episode=int, new_name = str()}}}
        for best_match in final_dict.keys():
            for filename in final_dict[best_match].keys():
                self.assertEqual(final_dict[best_match][filename]['new_name'],
                                 "Monster - S01E54 - Escape", "Bad rename")


if __name__ == '__main__':
    unittest.main()
