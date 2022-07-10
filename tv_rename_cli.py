from renamer.find_new_name import find_rename
import argparse
import logging
import os

_divider = "*"*150

def main(filenames,
         dry_run,
         ):
    group_dict, sort_dict, ep_dicts, final_dict = find_rename(filenames)
    # final_dicts = {Best_matched_name: {filename:{Season=int,Episode=int, new_name = str()}}}
    logging.debug(final_dict)
    for best_match in final_dict.keys():
        logging.info(_divider)
        logging.info(f"Show : {best_match}")
        for filename in final_dict[best_match].keys():
            for key, item in group_dict.items():
                    for elements in item:
                        old_filename, extension = elements
                        if filename==old_filename:
                            ext=extension
            new_name = final_dict[best_match][filename]['new_name']+"."+ext
            logging.info(
                f"{filename: <65} --> {new_name: <75}")
        if not dry_run:
            for filename in final_dict[best_match].keys():
                ext=None
                for key, item in group_dict.items():
                    for elements in item:
                        old_filename, extension = elements
                        if filename==old_filename:
                            ext=extension
                os.rename(filename, final_dict[best_match][filename]['new_name']+"."+ext)
    pass


if __name__ == """__main__""":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filenames", nargs='+', help='<Required> Filenames', required=True)
    parser.add_argument("--dry-run", action="store_true", help='dry run')
    parser.add_argument("-v", action="store_true", help='Verbosity')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    if args.v:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('Debug Mode')
    for key, item in vars(args).items():
        logging.debug(f"--{key: <10} : {item}")
    main(args.filenames, args.dry_run)
    pass