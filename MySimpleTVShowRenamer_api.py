from renamer.clean import clean_name
from renamer.search_tv_show_api import get_ep_list
from renamer.search_tv_show_api import get_best_matched_id, get_best_matched_name
from renamer.get_season import get_season
from renamer.find_new_name import find_rename
import re
import os

filenames = ["Ping Pong The Animation - 01 VOSTFR.mp4",
             "Monster 54.avi",
             "[Fansub] Fairy Ranmaru - 07 (480p).mkv",
             "Ping Pong The Animation - 06 VOSTFR.mp4",
             "Kaze+ga+Tsuyoku+Fuiteiru+(Run+with+the+Wind)+-+18+VOSTFR.mp4"
             ]

debug = 0
output_format = """{tv_name} - S{s_nb:02}E{ep_nb:02} - {tv_title}"""
output_format2 = """{tv_name} - {s_nb:02}x{ep_nb:02} - {tv_title}"""
_divider = "*"*150


def group_series(filename_list):
    group_dict = {}
    for filename in filename_list:
        cleaned_filename = clean_name(filename)
        best_match = get_best_matched_name(cleaned_filename)
        season_nb, ep_nb = get_season(filename)
        group_dict.setdefault(best_match, {})
        group_dict[best_match].setdefault(filename, (season_nb, ep_nb))
        formated_name = output_format.format(tv_name=best_match, s_nb=int(
            season_nb), ep_nb=int(ep_nb), tv_title="Episode {ep_nb:02}".format(ep_nb=ep_nb))
        group_dict[best_match].setdefault("new_name", formated_name)
    return group_dict


def main1(dirname):
    # print(group_series(filenames))
    group_dict, sort_dict, ep_dicts, final_dict = find_rename(
        os.listdir(dirname))
    # final_dicts = {Best_matched_name: {filename:{Season=int,Episode=int, new_name = str()}}}
    print(final_dict)
    for best_match in final_dict.keys():
        print(_divider)
        print("Show : ", best_match)
        for filename in final_dict[best_match].keys():
            print(
                f"{filename: <65} --> {final_dict[best_match][filename]['new_name']: <75}")


def main():
    # print(group_series(filenames))
    group_dict, sort_dict, ep_dicts, final_dict = find_rename(filenames)
    # final_dicts = {Best_matched_name: {filename:{Season=int,Episode=int, new_name = str()}}}
    print(final_dict)
    for best_match in final_dict.keys():
        print(_divider)
        print("Show : ", best_match)
        for filename in final_dict[best_match].keys():
            print(
                f"{filename: <65} --> {final_dict[best_match][filename]['new_name']: <75}")



if __name__ == """__main__""":
    main()
    # main1(MyDirectory)
    pass
