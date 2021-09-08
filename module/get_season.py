import re

debug =0

examples="""
[AnimeRG] Boku No Hero Academia - 96 (1080P 10bit) (Season 5 - 08).mkv
[Judas] Digimon Adventure (2020) - S01E49 [1080p][HEVC x265 10bit][Multi-Subs] (Weekly)
1 [EMBER] Mairimashita! Iruma-kun S02E06 [1080p] [HEVC WEBRip] (Welcome to Demon School! Iruma-kun 2nd Season)
[SSA] One Piece - 975 [480p].mkv
[SSA] Digimon Adventure (2020) - 49 [480p].mkv
[SSA] One Piece - 975 [720p].mkv
2 [Serenae] Tropical-Rouge! Precure - 13 (1080p).mkv
1 [Serenae] Tropical-Rouge! Precure - 13 (720p).mkv
[SSA] Digimon Adventure (2020) - 49 [720p].mkv
4 [Judas] One Piece - 975 [1080p][HEVC x265 10bit][Multi-Subs] (Weekly)
Digimon.Adventure.2020.S01E49.1080p.WEBRip.x264-Rapta
[ASW] One Piece - 975 [1080p HEVC x265 10Bit][AAC]
[SSA] One Piece - 975 [1080p].mkv
[ASW] Digimon Adventure (2020) - 49 [1080p HEVC x265 10Bit][AAC]
[SSA] Digimon Adventure (2020) - 49 [1080p].mkv
[SSA] Tropical-Rouge! Precure - 13 [480p].mkv
[-KS-] D4DJ First Mix [1080p] [Tri Audio] [VRV] [V2]
[-KS-] D4DJ First Mix [720p] [Tri Audio] [VRV] [V2]
[SSA] Tropical-Rouge! Precure - 13 [720p].mkv
Boku no Hero Academia (Saison 4) - 20 VOSTFR.mp4
Boku no Hero Academia (Season 4) - 20 VOSTFR.mp4
Boku no Hero Academia (Saison-4) - 20 VOSTFR.mp4
Boku no Hero Academia (Season.4) - 20 VOSTFR.mp4
Boku no Hero Academia (Saison-4) - 20 VOSTFR.mp4
Boku no Hero Academia (Season 4) - 20 VOSTFR.mp4
"""

info_regex ={
    "season_ep"     : "[Ss]([0-9]+)[][ ._-]*[Ee]([0-9]+)",
    "season"        : "S[eai]+son\W(\d{1,2})",
    "ep"            : "[\-\s]?\W(\d{1,3})[\W\.]",
    "episode"       : "(episode[s]?\W|\WEp\W|\W)(\d{1,3})"
}

def get_season(filename):
    (ep_nb, season_nb)=(0,0)
    season_ep_reg = re.compile(info_regex["season_ep"], re.IGNORECASE)
    season_reg    = re.compile(info_regex["season"], re.IGNORECASE)
    ep_reg        = re.compile(info_regex["ep"], re.IGNORECASE)
    episode_reg   = re.compile(info_regex["episode"], re.IGNORECASE)
    m = season_ep_reg.search(filename)
    if m:
        season_nb = int(m.group(1))
        ep_nb     = int(m.group(2))
    else:
        m = ep_reg.search(filename)
        if m:
            ep_nb = int(m.group(1))
            ms = season_reg.search(filename)
            if ms:
                season_nb = int(m.group(1))
            else:
                season_nb = 1
            if debug:
                print( int(m.group(1)) )
        else:
            m = episode_reg.search(filename)
            if m:
                if debug:
                    # print(m.group(0)[5:])
                    print(m.group(2))
                episode_reg = int(m.group(2))
                ms = season_reg.search(filename)
                if ms:
                    season_nb = int(m.group(1))
                else:
                    season_nb = 1
            else:
                print("no match")
                season_nb = 0
                ep_nb     = 0
    # if m :
    #     print(m.group())
    return (season_nb, ep_nb)

if __name__=="""__main__""":
    # fin = open("./test/other/clean_test_db.txt", 'r', encoding="utf-8")
    # fout = open("./test/other/res_get_season_test_db.txt", 'w')
    # for file in fin.readlines():
    #     print(file)
    #     print(get_season(file))
    #     fout.write(file)
    #     fout.write("S{0}E{1}".format(get_season(file)[0],get_season(file)[1]))
    #     fout.write('\n')
    # fin.close()
    # fout.close()
    for txt in examples.split('\n'):
        print(txt)
        print(get_season(txt))
    pass