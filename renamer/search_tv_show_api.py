import logging
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from tmdbv3api import TV, Movie, Season, TMDb

from renamer.api_key import MY_API_KEY

tmdb = TMDb()
tmdb.api_key = MY_API_KEY
_subdivider='*'*20

def get_ep_list(id, season):
    """Return a dictionary of episodes list from MovieDb, return None if not found"""
    if not id:
        return None
    ep_dict = dict()
    season_api = Season()
    try:
        season_api.details(id, season)
        tv = TV()
        name = tv.details(id)['name']
        for ep in season_api.details(id, season)['episodes']:
            nb_ep = int(ep['episode_number'])
            if ep['name']:
                title = ep['name']
            else:
                title = 'Episode ' + str(nb_ep)
            # logging.debug(ep['name'])
            # logging.debug(f'title {title}')
            res = name + " - " + "S"+str(season)+"E"+str(nb_ep)+" - " + title
            res = "{tv_name} - S{s_nb:02}E{ep_nb:02} - {tv_title}".format(
                tv_name=name, s_nb=int(season), ep_nb=int(nb_ep), tv_title=title[:30])
            # logging.debug(_subdivider)
            # logging.debug(res)
            # logging.debug(_subdivider)
            illegalChar = re.compile(
                "( \< | \> | \: | \" | \/ | \\ | \| | \? | \*)")
            title = illegalChar.sub(" ", title)
            ep_dict.setdefault(nb_ep, title)
        logging.debug(f"Found : {len(ep_dict.keys())} episodes")
        logging.debug(ep_dict)
    except IndexError as error:
        print("Tv Show Not Found - error : ", error)
        return None
    return ep_dict


def get_best_matched_id(tv_show_name):
    """Return a dictionary of episodes list from MovieDb, return None if not found"""
    tv = TV()
    # name = tv.details(id)['name']
    if tv.search(tv_show_name):
        return tv.search(tv_show_name)[0]['id']
    else:
        return None


def get_best_matched_name(tv_show_name):
    """Return a dictionary of episodes list from MovieDb, return None if not found"""
    tv = TV()
    try:
        name = tv.search(tv_show_name)[0]['name']
    except Exception as e:
        logging.critical(f"No show found for {tv_show_name}, error : {e}")
        exit()

    if tv.search(tv_show_name):
        return name
    else:
        return None

# def mvdbquery_str(tv_show_name):
#     """Return the query string for MovieDB WebSite"""
#     query_str = base
#     query_str += """/search/tv?query="""
#     words = tv_show_name.split()
#     words_lower = [word.lower() for word in words]
#     if debug:
#         for word in words_lower:
#             print("Word ", word)
#     for w_ind in range(len(words_lower)-1):
#             word = words_lower[w_ind]
#             query_str+=word
#             query_str+="+"
#     query_str+=words_lower[-1]
#     if debug:
#         print("Query str : ", query_str)
#     return query_str


if __name__ == "__main__":
    debug = 0
    if debug:
        set_w = ["86 Eighty Six",
                 "Walking Dead",
                 "Kaguya Sama",
                 "Lucifer",
                 "Flash",
                 "Non-existing show",
                 "Aie Caramba",
                 "Shadow-test"
                 ]
        # set_w = ["Walking Dead"]
        for tv_show in set_w:
            print(get_ep_list(get_best_matched_id(tv_show), 1))
        print(get_ep_list(get_best_matched_id(tv_show), 1))
    else:
        tv_show = str(input("Type the TV Show Name : "))
        s = int(input("Type Season : "))
        print("TV Show : ", tv_show, ", season : ", s)
        print(get_best_matched_name(tv_show))
        get_ep_list(get_best_matched_id(tv_show), s)
