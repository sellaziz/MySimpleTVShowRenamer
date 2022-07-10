import logging
import re

from renamer.clean import clean_name
from renamer.get_season import get_season
from renamer.search_tv_show_api import (get_best_matched_id,
                                        get_best_matched_name, get_ep_list)

output_format = """{tv_name} - S{s_nb:02}E{ep_nb:02} - {tv_title}"""
output_format2 = """{tv_name} - {s_nb:02}x{ep_nb:02} - {tv_title}"""


def find_rename(filename_list):
    group_dict = {}
    sort_dict = {}
    final_dict = {}
    ep_dicts = {}
    # Regroup tv shows by cleaned name
    for filename in filename_list:
        cleaner = re.compile("\\n", re.IGNORECASE)
        filename = cleaner.sub("", filename)
        cleaned_filename = clean_name(filename)
        extension=re.search("\.(\w+)$", filename).group(1)
    # Maybe clean the cleaned names (all lower case, or something)
        cleaned_filename = cleaned_filename.lower()
        group_dict.setdefault(cleaned_filename, [])
        group_dict[cleaned_filename].append((filename, extension))
    logging.debug(group_dict)
    # logging.debug(f" {group_dict.keys()} ")
    # --------------
    # Find out tv show name for cleaned names
    for key in group_dict.keys():
        logging.debug(f"Finding best match for {key}")
        best_match = get_best_matched_name(key)

        if best_match:
            sort_dict.setdefault(key, best_match)
        else:
            # Ask in terminal if the names match and if not ask new name
            while (best_match == None):
                print("No TV Show Name Found, please Type")
                print("Old name : ", key)
                new_name = str(input())
                best_match = get_best_matched_name(new_name)
                sort_dict.setdefault(key, best_match)
    # logging.debug(sort_dict)
    # Find out episode names for set of cleaned names
    for key in group_dict.keys():
        seasons = {}
        best_match = sort_dict[key]
        # final_dicts = {Best_matched_name: {filename:{Season=int,Episode=int, new_name = str()}}}
        final_dict.setdefault(best_match, {})
        for filename, extension in group_dict[key]:
            season_nb, ep_nb = get_season(filename)
            # logging.debug("final_dict[best_match][filename], {} {}, ep {}, s {}".format(best_match, filename, season_nb, ep_nb))
            final_dict[best_match].setdefault(filename, {})
    # Associate Season and episode with filenames
            final_dict[best_match][filename].setdefault("Season", season_nb)
            final_dict[best_match][filename].setdefault("Episode", ep_nb)
            seasons.setdefault(season_nb, "")
    # Associate Best Match with filenames
        for season in seasons.keys():
            best_match = sort_dict[key]
            best_name = get_best_matched_name(best_match)
            best_id = get_best_matched_id(best_match)
            ep_dicts.setdefault(best_name, {})
            ep_dicts[best_match].setdefault(
                season, get_ep_list(best_id, season))
        logging.debug("Show : {0} and seasons: {1}".format(
            best_match, seasons.keys()))
    # Associate Episode title with filenames
        # logging.debug(f" {final_dict} ")
        # logging.debug(f" {ep_dicts} ")
        for filename, extension in group_dict[key]:
            best_match = sort_dict[key]
            season_nb = final_dict[best_match][filename]['Season']
            ep_nb = final_dict[best_match][filename]['Episode']
            try:
                title = ep_dicts[best_match][season_nb][ep_nb]
            except KeyError as error:
                print("No episode ", ep_nb, " found, error: ", error)
                title = 'Episode ' + str(ep_nb)
            logging.debug(f"best_match: {best_match}, season_nb: {season_nb}, ep_nb: {ep_nb}, title: {title}")
            formated_name = output_format.format(tv_name=best_match, s_nb=int(
                season_nb), ep_nb=int(ep_nb), tv_title=title)
            final_dict[best_match][filename].setdefault(
                "new_name", formated_name)
    # -----------------
    # TODO Or maybe show other matches
    return group_dict, sort_dict, ep_dicts, final_dict
