from module.clean import clean_name
from module.search_tv_show_api import get_ep_list
from module.search_tv_show_api import get_best_matched_id, get_best_matched_name
from module.get_season import get_season
import re
import os

filenames = ["Ping Pong The Animation - 01 VOSTFR.mp4",
              "Monster 54.avi",
              "[Fansub] Fairy Ranmaru - 07 (480p).mkv",
              "Ping Pong The Animation - 06 VOSTFR.mp4",
              "Kaze+ga+Tsuyoku+Fuiteiru+(Run+with+the+Wind)+-+18+VOSTFR.mp4"
              ]

debug=0
output_format="""{tv_name} - S{s_nb:02}E{ep_nb:02} - {tv_title}"""
output_format2="""{tv_name} - {s_nb:02}x{ep_nb:02} - {tv_title}"""

def group_series(filename_list):
    group_dict={}
    for filename in filename_list:
        cleaned_filename = clean_name(filename)
        best_match = get_best_matched_name(cleaned_filename)
        season_nb, ep_nb = get_season(filename)
        group_dict.setdefault(best_match,{})
        group_dict[best_match].setdefault(filename, (season_nb,ep_nb))
        formated_name = output_format.format(tv_name=best_match, s_nb=int(season_nb), ep_nb=int(ep_nb), tv_title="Episode {ep_nb:02}".format(ep_nb=ep_nb))
        group_dict[best_match].setdefault("new_name", formated_name)
    return group_dict


def main1(dirname):
    # print(group_series(filenames))
    group_dict, sort_dict, ep_dicts, final_dict = find_rename(os.listdir(dirname))
    # final_dicts = {Best_matched_name: {filename:{Season=int,Episode=int, new_name = str()}}}
    print(final_dict)
    for best_match in final_dict.keys() :
        print("***********************************************************************************************************************************************")
        print("Show : ", best_match)
        for filename in final_dict[best_match].keys():
            # print(filename[:100], "-->", final_dict[best_match][filename]['new_name'][:100])
            print(filename.ljust(65), "-->", final_dict[best_match][filename]['new_name'].ljust(75))


def main():
    # print(group_series(filenames))
    group_dict, sort_dict, ep_dicts, final_dict = find_rename(filenames)
    # final_dicts = {Best_matched_name: {filename:{Season=int,Episode=int, new_name = str()}}}
    print(final_dict)
    for best_match in final_dict.keys() :
        print("***********************************************************************************************************************************************")
        print("Show : ", best_match)
        for filename in final_dict[best_match].keys():
            # print(filename[:100], "-->", final_dict[best_match][filename]['new_name'][:100])
            print(filename.ljust(65), "-->", final_dict[best_match][filename]['new_name'].ljust(75))

    # fin = open("./test/other/clean_test_db.txt", 'r', encoding="utf-8")
    # print(group_series(fin.readlines()[1:100]))
    # print(find_rename(fin.readlines()[1:100]))
    # fin.close()
    # filename = "Ping Pong The Animation - 01 VOSTFR.mp4"
    # cleaned_name = clean_name(filename)
    # ep_list = get_ep_list(cleaned_name, 1)
    # print(cleaned_name, ep_list)

def find_rename(filename_list):
    group_dict={}
    sort_dict={}
    final_dict={}
    ep_dicts={}
    # Regroup tv shows by cleaned name
    for filename in filename_list:
        cleaner = re.compile("\\n", re.IGNORECASE)
        filename = cleaner.sub("", filename)
        cleaned_filename = clean_name(filename)
    # Maybe clean the cleaned names (all lower case, or something)
        cleaned_filename = cleaned_filename.lower()
        group_dict.setdefault(cleaned_filename,[])
        group_dict[cleaned_filename].append(filename)
    if debug:
        print(group_dict)
        print("\n\n\n",group_dict.keys(),"\n\n\n")
    # --------------
    # Find out tv show name for cleaned names
    for key in group_dict.keys():
        if debug:
            print("Finding best match for ", key)
        best_match = get_best_matched_name(key)
        
        if best_match:
            sort_dict.setdefault(key, best_match)
        else:
    # Ask in terminal if the names match and if not ask new name
            while (best_match==None):
                print("No TV Show Name Found, please Type")
                print("Old name : ", key)
                new_name = str(input())
                best_match = get_best_matched_name(new_name)
                sort_dict.setdefault(key, best_match)
    if debug:
        print(sort_dict)
    # Find out episode names for set of cleaned names
    for key in group_dict.keys():
        seasons = {}
        best_match = sort_dict[key]
        # final_dicts = {Best_matched_name: {filename:{Season=int,Episode=int, new_name = str()}}}
        final_dict.setdefault(best_match,{})
        for filename in group_dict[key]:
            season_nb, ep_nb = get_season(filename)
            # print("final_dict[best_match][filename], {} {}, ep {}, s {}".format(best_match, filename, season_nb, ep_nb))
            final_dict[best_match].setdefault(filename, {})
    # Associate Season and episode with filenames
            final_dict[best_match][filename].setdefault("Season" , season_nb)
            final_dict[best_match][filename].setdefault("Episode", ep_nb)
            seasons.setdefault(season_nb,"")
    # Associate Best Match with filenames
        for season in seasons.keys():
            best_match = sort_dict[key]
            best_name=get_best_matched_name(best_match)
            best_id=get_best_matched_id(best_match)
            ep_dicts.setdefault(best_name,{})
            ep_dicts[best_match].setdefault(season,get_ep_list(best_id,season))
        if debug:
            print("Show : {0} and seasons: {1}".format(best_match, seasons.keys()))
    # Associate Episode title with filenames
        if debug:
            print("\n\n\n",final_dict,"\n\n\n")
            print("\n\n\n",ep_dicts,"\n\n\n")
        for filename in group_dict[key]:
            best_match = sort_dict[key]
            season_nb = final_dict[best_match][filename]['Season']
            ep_nb     = final_dict[best_match][filename]['Episode']
            try:
                title     = ep_dicts[best_match][season_nb][ep_nb]
            except KeyError as error:
                print("No episode ", ep_nb," found, error: ", error)
                title = 'Episode ' + str(ep_nb)
            if debug:
                print(best_match, season_nb, ep_nb, title)
            formated_name = output_format.format(tv_name=best_match, s_nb=int(season_nb), ep_nb=int(ep_nb), tv_title=title)
            final_dict[best_match][filename].setdefault("new_name", formated_name)
    # -----------------
    # TODO Or maybe show other matches
    return group_dict, sort_dict, ep_dicts, final_dict
    pass

if __name__=="""__main__""":
    main()
    # main1(MyDirectory)
    pass