from selenium import webdriver
from bs4 import BeautifulSoup
import re

debug=0
base = """https://www.themoviedb.org"""
driver =  webdriver.Firefox()
output_format="""{tv_name} - S{s_nb:02}E{ep_nb:02} - {tv_title}"""
output_format2="""{tv_name} - {s_nb:02}x{ep_nb:02} - {tv_title}"""

def get_ep_list(tv_show_name, season):
    """Return a dictionary of episodes list from MovieDb, return None if not found"""
    ep_dict=dict()
    # Create string for query
    query = mvdbquery_str(tv_show_name)
    # Get HTML Source Code from query
    driver.get(query)
    # Select the First Result
    QuerySoup = BeautifulSoup(driver.find_element_by_css_selector("body").get_attribute("innerHTML"), 'html.parser')
    if debug:
        for div in QuerySoup.findAll('div', attrs={'class':'card v4 tight'}):
            name=div.find('h2')
            link=div.find('a', attrs={'class':'result'})
            print(name.text)
            print(link['href'])
    try:
        div = QuerySoup.findAll('div', attrs={'class':'card v4 tight'})[0]
        name=div.find('h2')
        link=div.find('a', attrs={'class':'result'})
        if debug:
            print(name.text)
            print(link['href'])
        full_link=base+str(link['href'])+"""/season/"""+str(season)
        # Get HTML Source Code from Result in Right Season
        driver.get(full_link)
        # Get Episode names
        QuerySoup = BeautifulSoup(driver.find_element_by_css_selector("body").get_attribute("innerHTML"), 'html.parser')
        div = QuerySoup.findAll('div', attrs={'class':'card'})
        for ep in div:
            nb_ep = int(ep.find('a')['episode'])
            m = re.search('Episode \d{1,4} - (.*)$', ep.find('a')['title'])
            if m.group(1):
                title = m.group(1)
            else:
                title = 'Episode ' + str(nb_ep)
            if debug:
                print(ep.find('a')['title'])
                print('title ', title)
            res = name.text + " - " + "S"+str(season)+"E"+str(nb_ep)+" - "+ title
            res = output_format2.format(tv_name=name.text, s_nb=int(season), ep_nb=int(nb_ep), tv_title=title[:30])
            if debug:
                print('*'*20, '\n',res, '\n', '*'*20,'\n')
            illegalChar = re.compile("( \< | \> | \: | \" | \/ | \\ | \| | \? | \*)")
            title = illegalChar.sub(" ", title)
            ep_dict.setdefault(nb_ep, title)
        if debug:
            print(ep_dict)
    except IndexError as error:
        print("Tv Show Not Found - error : ", error)
        return None
    return ep_dict

def get_best_matched_name(tv_show_name):
    """Return a dictionary of episodes list from MovieDb, return None if not found"""
    ep_dict=dict()
    # Create string for query
    query = mvdbquery_str(tv_show_name)
    # Get HTML Source Code from query
    driver.get(query)
    # Select the First Result
    QuerySoup = BeautifulSoup(driver.find_element_by_css_selector("body").get_attribute("innerHTML"), 'html.parser')
    if debug:
        for div in QuerySoup.findAll('div', attrs={'class':'card v4 tight'}):
            name=div.find('h2')
            link=div.find('a', attrs={'class':'result'})
            print(name.text)
            print(link['href'])
    try:
        div = QuerySoup.findAll('div', attrs={'class':'card v4 tight'})[0]
        if debug:
            print('div : ', div.find('h2').text)
        name=div.find('h2')
        link=div.find('a', attrs={'class':'result'})
    except IndexError as error:
        print("Tv Show Not Found - error : ", error)
        return None
    return name.text


def mvdbquery_str(tv_show_name):
    """Return the query string for MovieDB WebSite"""
    query_str = base
    query_str += """/search/tv?query="""
    words = tv_show_name.split()
    words_lower = [word.lower() for word in words]
    if debug:
        for word in words_lower:
            print("Word ", word)
    for w_ind in range(len(words_lower)-1):
            word = words_lower[w_ind]
            query_str+=word
            query_str+="+"
    query_str+=words_lower[-1]
    if debug:
        print("Query str : ", query_str)
    return query_str
    

if __name__=="__main__":
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
            print(get_ep_list(tv_show, 1))
        print(get_ep_list(tv_show, 1))
    else:
        tv_show = str(input("Type the TV Show Name : "))
        s       = int(input("Type Season : "))
        print("TV Show : ", tv_show, ", season : ", s)
        get_ep_list(tv_show, s)
        print(get_best_matched_name(tv_show))
    