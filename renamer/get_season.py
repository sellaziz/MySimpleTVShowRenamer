import logging
import re

info_regex = {
    "season_ep": "[Ss]([0-9]+)[][ ._-]*[Ee]([0-9]+)",  # S03E04
    "season": "S[eai]+son\W(\d{1,2})",  # Season 1
    "ep": "[\-\s]?\W(\d{1,3})[\W\.]",  # - 13
    "episode": "(episode[s]?\W|\WEp\W|\W)(\d{1,3})"  # Episode 1, Ep 1
}


def get_season(filename):
    (ep_nb, season_nb) = (0, 0)
    season_ep_reg = re.compile(info_regex["season_ep"], re.IGNORECASE)
    season_reg = re.compile(info_regex["season"], re.IGNORECASE)
    ep_reg = re.compile(info_regex["ep"], re.IGNORECASE)
    episode_reg = re.compile(info_regex["episode"], re.IGNORECASE)
    m = season_ep_reg.search(filename)
    if m:  # S03E04, we get the ep and season directly
        season_nb = int(m.group(1))
        ep_nb = int(m.group(2))
    else:  # we try to figure out if there is an episode/season number
        m = ep_reg.search(filename)
        if m:
            ep_nb = int(m.group(1))
            ms = season_reg.search(filename)
            if ms:
                season_nb = int(m.group(1))
            else:
                season_nb = 1
            logging.debug(int(m.group(1)))
        else:
            m = episode_reg.search(filename)
            if m:
                logging.debug(m.group(2))
                episode_reg = int(m.group(2))
                ms = season_reg.search(filename)
                if ms:
                    season_nb = int(m.group(1))
                else:
                    season_nb = 1
            else:
                print("no match")
                season_nb = 0
                ep_nb = 0
    return (season_nb, ep_nb)


if __name__ == """__main__""":
    txt = "Walking Dead - S01E01.mp4"
    print(txt)
    print(get_season(txt))
    pass
