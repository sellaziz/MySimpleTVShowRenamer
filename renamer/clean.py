import logging
import re

my_regexes = {
    "extension": "\.[^.]+$",
    "brackets": "\[[^]]*\]",
    "parenthesis": "\([^)]*\)",
    "web": "www\.[^.]*\.",
    "separators": "(\+|\.|\(|\)|\_)",
    "encoding": "[\w\.]{0,2}26\d",  # (x264, x265, h264, h265,...)
    "encoding2": "\d{1,2}.?bit[s]?",  # 8-bits, 10-bit, 10-bits
    "encoding3": "nvenc|hevc|bluray|(bd|hd|dvd|web)rip|xvid|hdlight",
    "lang": "\W(VOST\D{1,2}|VF\w{0,3})\W",
    "lang2": "\W(TRUE)?FRENCH|ENG\W",
    "subs": "\W(multi\w{0,3}|sub\w{0,3})\W",
    "qual": "(480|720|1080)\D",
    "audio_enc": "ac3|aac",
    "season_ep": "[Ss]([0-9]+)[][ ._-]*[Ee]([0-9]+)([^\\/]*)",
    "season_full": "[Ss]eason\s*\d+",
    "ep": "\W\-?\s?\d{1,3}\W",
    "ep_short": "Ep\s*\d+",
    "episode": "episode[s]?\W\d{1,3}\W|\WEp\W"
}


def clean_name(file):
    new_file = file
    for key in my_regexes.keys():
        cleaner = re.compile(my_regexes[key], re.IGNORECASE)
        new_file = cleaner.sub("+", new_file)
    new_tab = []
    for txt in new_file.split("+"):
        if txt != '+' and not txt.isspace() and txt:
            new_tab.append(txt)
    new_tab1 = []
    for txt in " ".join(new_tab).split(" "):
        if not txt.isspace() and txt:
            new_tab1.append(txt)
    logging.debug(f'Clean Name : {file} --> {" ".join(new_tab1)}')
    return (" ".join(new_tab1))


if __name__ == """__main__""":
    fin = open("./test/other/clean_test_db.txt", 'r', encoding="utf-8")
    fout = open("./test/other/res_clean_test_db.txt", 'w')
    # test_str = fin.read()
    # for file in test_str.split('\n'):
    # test_str = fin.read()
    for file in fin.readlines():
        print(file)
        print(clean_name(file))
        fout.write(file)
        fout.write(clean_name(file))
        fout.write('\n')
    fin.close()
    fout.close()
