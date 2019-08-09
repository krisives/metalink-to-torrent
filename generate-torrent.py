
import bencode3
from hashlib import md5, sha1
import os
from time import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description='Convert a meta4 link to a torrent')
parser.add_argument('meta4', help="meta4 file input")
parser.add_argument('torrent', help="torrent file output")
parser.add_argument('--urlname', action='store_true', help="Use a name in the mirror list instead")
args = parser.parse_args()

meta4 = BeautifulSoup(open(args.meta4), 'xml')
name = meta4.file['name']
fileSize = int(meta4.file.size.string)
fileHash = meta4.file.select('hash[type=sha-1]')[0].text
pieceSize = int(meta4.file.pieces['length'])
pieceCount = 0
pieceHashes = bytearray()
mirrorList = []

for node in meta4.file.pieces.children:
    pieceHash = node.string.strip()

    if not pieceHash:
        continue

    pieceHashes += bytearray.fromhex(pieceHash)
    pieceCount += 1

for node in meta4.file.select('url'):
    mirrorList.append(node.string.strip())

if args.urlname:
    url = urlparse(mirrorList[0])
    name = os.path.basename(url.path)

print("File:       ", name)
print("File Size:  ", fileSize)
print("File Hash:  ", fileHash)
print("Piece Size: ", pieceSize, "(", pieceSize * pieceCount, ")")
print("Piece Count:", pieceCount)
print("Mirrors:    ", len(mirrorList))

torrent = {
    'announce': 'udp://tracker.openbittorrent.com:80',
    'creation date': int(time()),
    'info': {
        'length': fileSize,
        'piece length': pieceSize,
        'name': name,
        'pieces': bytes(pieceHashes)
    },
    'url-list': mirrorList
}

encoded = bencode3.encode_dict(torrent, 'ascii')

with open(args.torrent, 'wb') as fp:
    fp.write(encoded)
