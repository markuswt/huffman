#!/usr/bin/env python3

"Encode and decode text using Huffman's algorithm"

import sys
import typing
from collections import Counter

def build_codes(text: str) -> typing.Dict[str, str]:
    "Determine the encoding"

    # the first element of each list is the summed count of all subsequent chars
    # [summed_count, ...chars]
    # this is not an actual tree, but a flattened one
    tree = [[p, c] for c, p in Counter(text).items()]
    # map chars to thier encoded counterparts
    codes = {pr[1]: "" for pr in tree}
    if len(tree) == 1:
        codes[text[0]] += "1"
    while len(tree) > 1:
        tree.sort(key=lambda l: l[0])
        l1 = tree.pop(0)
        l2 = tree.pop(0)
        tree.append([l1[0] + l2[0]] + l1[1:] + l2[1:])
        for c in l1[1:]:
            codes[c] = "0" + codes[c]
        for c in l2[1:]:
            codes[c] = "1" + codes[c]
    return codes

def encode(text: str) -> str:
    "Encode one piece of plain text using Huffman's algorithm"

    codes = build_codes(text)
    s = "[Codes]"
    # add codes sorted by code length
    for char, code in sorted(codes.items(), key=lambda c: len(c[1])):
        # use repr(char) so that escape sequences are not evaluated
        s += f"\n{code}={repr(char)}"
    s += "\n[Content]\n" + "".join([codes[c] for c in text])
    return s

def encode_stdin() -> None:
    "Encode input from stdin"

    text = sys.stdin.read()
    sys.stdout.write(encode(text))
    sys.stdout.write("\n")

def map_codes(text: str, codes: typing.Dict[str, str]) -> str:
    "Encode one piece of encoded text"

    # Huffman coding is prefix-free
    # so replacing char_stack with the first match works fine
    char_stack = ""
    decoded = ""
    for char in text:
        char_stack += char
        if char_stack in codes:
            decoded += escape(codes[char_stack])
            char_stack = ""
    if char_stack != "":
        raise ValueError("Encoding does not match encoded text")
    return decoded

def escape(s: str) -> str:
    "Evaluate escape characters"

    return s.encode("latin1") \
        .decode("unicode-escape") \
        .encode("latin1") \
        .decode("utf-8") \

def decode_stdin() -> None:
    "Decode input from stdin"

    codes = {}
    state = 0
    for line in sys.stdin:
        if state == 0 and "[Codes]" in line:
            state = 1
        elif state == 1:
            if "[Content]" in line:
                state = 2
            else:
                code = line.rstrip().split("=")
                codes[code[0]] = code[1][1:-1] # don't include "'"
        elif state == 2:
            sys.stdout.write(map_codes(line.rstrip(), codes))

if __name__ == "__main__":
    if len(sys.argv) <= 1 or sys.argv[1] not in ("encode", "decode"):
        print("usage: python3 huffman.py [encode|decode] [<text>]")
    elif sys.argv[1] == "encode":
        if len(sys.argv) > 2:
            print(encode(" ".join(sys.argv[2:])))
        else:
            encode_stdin()
    elif sys.argv[1] == "decode":
        decode_stdin()
