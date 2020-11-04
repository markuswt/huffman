# huffman-py

A toy huffman encoder.

```bash
$ ./huffman.py encode foo
[Codes]
0='f'
1='o'
[Content]
011
$ echo foo | ./huffman.py encode
[Codes]
0='o'
10='f'
11='\n'
[Content]
100011
$ echo foo | ./huffman.py encode | ./huffman.py decode
foo
```
