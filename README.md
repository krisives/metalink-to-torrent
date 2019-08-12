# metalink-to-torrent

Convert metalink files to torrent web seeds.


## Installation

I'm not super experienced with generating `pip` packages or `setup.py` so
here are the commands I had to run to get the packages. Pull requests to
make a setup.py would be appreciated.

    pip3 install bencode3
    pip3 install lxml
    pip3 install beautifulsoup4

## Usage

    python3 input.meta4 output.torrent

## Options

* `--urlname` grabs the filename from the first mirror URL in the metalink file
  instead of using the name provided in the metalink XML. This can be useful if
  the metalink always provides a name like `something-current.iso` but mirrors
  provide a more useful name like `something-20190801.iso`

## Notes

* Only works on torrents that contain a single file
