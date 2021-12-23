#!/usr/bin/env python3

"Encode and decode text using Huffman's algorithm"

import sys
import typing
from bisect import insort
from collections import Counter


def build_codes(text: str) -> typing.Dict[str, str]:
    "Determine the encoding"
    
    # the first element of each tuple is the total count of all subsequent chars
    chars = sorted([(count, [char]) for char, count in Counter(text).items()])
    
    # maps each character to its encoded counterpart
    codes = {char[0]: "" for _, char in chars}
    
    if len(chars) == 1:
        codes[text[0]] += "1"
    while len(chars) > 1:
        count_1, chars_1 = chars.pop(0)
        count_2, chars_2 = chars.pop(0)
        insort(chars, (count_1 + count_2, chars_1 + chars_2))
        for char in chars_1:
            codes[char] = "0" + codes[char]
        for char in chars_2:
            codes[char] = "1" + codes[char]
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


def decode(text: str, codes: typing.Dict[str, str]) -> str:
    "Decode one piece of encoded text"
    
    current_code = ""
    decoded = ""
    for char in text:
        current_code += char
        # Huffman coding is prefix-free, so replacing current_code with the first match works fine
        if current_code in codes:
            decoded += codes[current_code]
            current_code = ""
    if current_code != "":
        raise ValueError("Encoding does not match encoded text")
    
    # evaluate escape characters
    return decoded \
        .encode("latin1") \
        .decode("unicode-escape") \
        .encode("latin1") \
        .decode("utf-8")


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
                codes[code[0]] = code[1][1:-1]  # don't include "'"
        
        elif state == 2:
            sys.stdout.write(decode(line.rstrip(), codes))


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
