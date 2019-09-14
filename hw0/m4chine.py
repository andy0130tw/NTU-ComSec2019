# uncompyle6 version 3.4.0
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.5.3 (default, Sep 27 2018, 17:25:39)
# [GCC 6.3.0 20170516]
# Embedded file name: m4chine.py
# Size of source mod 2**32: 4498 bytes
from ctypes import *
from binascii import *

class Machine:

    def __init__(self, init):
        self.context = list(map(ord, init))
        print('init' + ' ' * 20, self.context)
        self.op = {0:self.add,  1:self.cmp,  2:self.context,  3:self.empty,  6:self.pop,  7:self.push,  8:self.sub,  9:self.terminal}

    def empty(self, _):
        return len(self.context) == 0

    def e_start(self, code):
        for xxx, i in enumerate(zip(*(iter(code),) * 2)):
            print('{:3d}:'.format(xxx), self.op[ord(i[0])].__name__, ord(i[1]) if ord(i[0]) in [1, 7] else '')
            if i != None:
                self.op[ord(i[0])](ord(i[1]))
            print('cxt ' + ' ' * 20, self.context)

    def push(self, num):
        self.context.append(num)

    def pop(self, _):
        assert len(self.context) >= 1, 'You should sharpen your coding skill'
        result, self.context = self.context[(-1)], self.context[:-1]
        return result

    def terminal(self, _):
        assert len(self.context) >= 1, 'You should sharpen your coding skill'
        if self.context[(-1)] == 0:
            print('You fail, try again')
            exit(0)

    def add(self, _):
        assert len(self.context) >= 2, 'You should sharpen your coding skill'
        result, self.context = self.context[(-1)] + self.context[(-2)], self.context[:-2]
        self.context.append(c_int8(result).value)

    def sub(self, _):
        assert len(self.context) >= 2, 'You should sharpen your coding skill'
        result, self.context = self.context[(-1)] - self.context[(-2)], self.context[:-2]
        self.context.append(c_int8(result).value)

    def cmp(self, num):
        assert len(self.context) >= 1, 'You should sharpen your coding skill'
        self.context[-1] = 1 if self.context[(-1)] == num else 0


print('''

888b      88  88  888b      88  88    d8\'  ad88888ba      88b           d88         db         ,ad8888ba,   88        88  88  888b      88  88888888888
8888b     88  88  8888b     88  88   d8\'  d8"     "8b     888b         d888        d88b       d8"\'    `"8b  88        88  88  8888b     88  88
88 `8b    88  88  88 `8b    88  88  ""    Y8,             88`8b       d8\'88       d8\'`8b     d8\'            88        88  88  88 `8b    88  88
88  `8b   88  88  88  `8b   88  88        `Y8aaaaa,       88 `8b     d8\' 88      d8\'  `8b    88             88aaaaaaaa88  88  88  `8b   88  88aaaaa
88   `8b  88  88  88   `8b  88  88          `"""""8b,     88  `8b   d8\'  88     d8YaaaaY8b   88             88""""""""88  88  88   `8b  88  88"""""
88    `8b 88  88  88    `8b 88  88                `8b     88   `8b d8\'   88    d8""""""""8b  Y8,            88        88  88  88    `8b 88  88
88     `8888  88  88     `8888  88        Y8a     a8P     88    `888\'    88   d8\'        `8b  Y8a.    .a8P  88        88  88  88     `8888  88
88      `888  88  88      `888  88         "Y88888P"      88     `8\'     88  d8\'          `8b  `"Y8888Y"\'   88        88  88  88      `888  88888888888

This is nini\'s machine to test if you are qualified to join this class


''')

arr = [
70, 76, 65, 71, 123, 87, 48, 119, 95, 66, 105, 105, 105, 105, 105, 105, 105, 105, 71, 95, 83, 105, 90, 101, 51, 101, 51, 33, 125
]

print(bytes(arr).decode())
# FLAG{W0w_BiiiiiiiiG_SiZe3e3!}

s = ''.join(map(chr, bytes(arr)))
emu = Machine(s)
emu.e_start('\x08\x00\x07\x08\x00\x00\x01d\t\x00\x00\x00\x014\t\x00\x073\x07\x01\x073\x08\x00\x00\x00\x01e\t\x00\x00\x00\x08\x00\x07c\x00\x00\x01\x00\t\x00\x00\x00\x074\x08\x00\x01\x00\t\x00\x06\x00\x01e\t\x00\x06\x00\x07Z\x08\x00\x01\x00\t\x00\x07h\x00\x00\x08\x00\x01\x00\t\x00\x06\x00\x07S\x08\x00\x01\x00\t\x00\x06\x00\x07_\x08\x00\x01\x00\t\x00\x06\x00\x07G\x08\x00\x01\x00\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01j\t\x00\x00\x00\x01C\t\x00\x06\x00\x07\x00\x07\x01\x00\x00\x07\x02\x00\x00\x07\x03\x00\x00\x07\x04\x00\x00\x07\x05\x00\x00\x07\x06\x00\x00\x07\x07\x00\x00\x07\x08\x00\x00\x07\t\x00\x00\x07\n\x00\x00\x07\x0b\x00\x00\x07\x0c\x00\x00\x07\r\x00\x00\x07\x04\x00\x00\x08\x00\x01\x00\t\x00\x06\x00\x01w\t\x00\x06\x00\x010\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x13\x00\x00\x01\x00\t\x00')

'''
  0 sub
  1 push, 8
  2 add
  3 cmp, 100
  4 terminal
  5 add
  6 cmp, 52
  7 terminal
  8 push, 51
  9 push, 1
 10 push, 51
 11 sub
 12 add
 13 cmp, 101
 14 terminal
 15 add
 16 sub
 17 push, 99
 18 add
 19 cmp, 0
 20 terminal
 21 add
 22 push, 52
 23 sub
 24 cmp, 0
 25 terminal
 26 pop
 27 cmp, 101
 28 terminal
 29 pop
 30 push, 90
 31 sub
 32 cmp, 0
 33 terminal

 34 push, 104
 35 add
 36 sub
 37 cmp, 0
 38 terminal
 39 pop
 40 push, 83
 41 sub
 42 cmp, 0
 43 terminal

 44 pop
 45 push, 95
 46 sub
 47 cmp, 0
 48 terminal

 49 pop
 50 push, 71
 51 sub
 52 cmp, 0
 53 terminal
 54 add
 55 cmp, 106
 56 terminal
 57 add
 58 cmp, 106
 59 terminal
 60 add
 61 cmp, 106
 62 terminal
 63 add
 64 cmp, 106
 65 terminal
 66 add
 67 cmp, 106
 68 terminal
 69 add
 70 cmp, 106
 71 terminal
 72 add
 73 cmp, 106
 74 terminal
 75 add
 76 cmp, 106
 77 terminal
 78 add
 79 cmp, 67
 80 terminal
 81 pop
 82 push, 0
 83 push, 1
 84 add
 85 push, 2
 86 add
 87 push, 3
 88 add
 89 push, 4
 90 add
 91 push, 5
 92 add
 93 push, 6
 94 add
 95 push, 7
 96 add
 97 push, 8
 98 add
 99 push, 9
100 add
101 push, 10
102 add
103 push, 11
104 add
105 push, 12
106 add
107 push, 13
108 add
109 push, 4
110 add
111 sub
112 cmp, 0
113 terminal
114 pop
115 cmp, 119
116 terminal
117 pop
118 cmp, 48
119 terminal
120 add
121 add
122 add
123 add
124 add
125 add
126 push, 19
127 add
128 cmp, 0
129 terminal
'''

print('Yeah, you got the flag')
# okay decompiling m4chine.pyc
