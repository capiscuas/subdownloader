# SubDownloader

SubDownloader is a Free Open-Source tool written in Python for automatic download/upload of subtitles for video files. It uses some smart hashing algorithms to work fast.

## Dependencies

Required:
- [Python]: version 2 or 3
- Python packages:
  * [argparse]: parsing command line options (standard since Python 3.2)
  * [python-progressbar]: command line interface
- [Qt]: graphical interface.
  * Qt: Libraries.
  * [pyQt]: Python bindings (version 4)

Optional Python packages:
- [kaa-metadata]: currently only available for Python 2
- [pymediainfo]: used as fallback for python-kaa-metadata. This package needs [MediaInfo](https://mediaarea.net).
- [argcomplete]: Bash tab completion for argparse

## Running the program

### Graphical Interface

```sh
$ ./run.py
```

### Command Line

```sh
$ ./run.py -c
```

### Help

```sh
$ ./run.py -h
```

## License

SubDownloader is licensed under [GPL v3].

   [Python]: <https://www.python.org/>
   [argparse]: <https://python.readthedocs.org/en/latest/library/argparse.html>
   [python-progressbar]: <https://github.com/niltonvolpato/python-progressbar>
   [Qt]: <https://www.qt.io/>
   [pyQt]: <https://riverbankcomputing.com/software/pyqt/intro>
   [kaa-metadata]: <https://github.com/freevo/kaa-metadata>
   [pymediainfo]: <https://pymediainfo.readthedocs.org/en/latest/>
   [argcomplete]: <https://argcomplete.readthedocs.org/>
   [GPL v3]: <https://www.gnu.org/licenses/gpl-3.0.html>
   