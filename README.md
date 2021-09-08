# Simple TV Show Renamer

Python script that help rename your TV Show files with a standard format.

## Description

Simple renamer that analyze the file name and try to find the TV Show that latches the best in TheMovieDb and seek for the episode name in order to rename the file. There is two functions to do it, one relies on selenium and parses TheMovieDb Website and the other uses the api and the library tmdbv3api.

## Getting Started

### Dependencies

* Python 3.x
* selenium or tmdbv3api
* BeautifulSoup4

### Executing program

* Currently it seek for all files in a directory that is provided in the script but new versions will have a command-line parser

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [Kodi-Regexes](https://kodi.wiki/view/Advancedsettings.xml#tvshowmatching)
