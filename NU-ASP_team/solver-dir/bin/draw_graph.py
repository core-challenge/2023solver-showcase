#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
@author Shuji Kosuge
"""

import sys
import getopt
import re
import os


def  usage():
    print(f"This program makes dot file from col and dat files.")
    print(f"usage: python3 {sys.argv[0]} col_file dat_file")
    print(f"\n")
    print(f"After using this program, do under command.")
    print(f"> brew install graphviz")
    print(f"> dot -Tpng hogehoge.dot -o hogehoge.png")


"""
main
"""
def main():
    col_file = sys.argv[1]
    dat_file = sys.argv[2]
    file_name = os.path.splitext(os.path.basename(dat_file))[0]
    color = '[fillcolor="#ccddff", style="filled"]'

    edges = []
    with open(col_file) as cf:
        for line in cf:
            e = re.match(r"^e\s(\d+)\s(\d+)", line)
            if e is None:
                continue
            edges.append(f"{e.group(1)} -- {e.group(2)};\n")

    s = []
    t = []
    with open(dat_file) as df:
        for line in df:
            sl = re.match(r"^s\s", line)
            tl = re.match(r"^t\s", line)
            if sl is not None:
                for w in line.split():
                    i = re.match(r"(\d+)", w)
                    if i is not None:
                        s.append(i.group(1))
            if tl is not None:
                for w in line.split():
                    i = re.match(r"(\d+)", w)
                    if i is not None:
                        t.append(i.group(1))

    with open(f"{file_name}_s.dot", mode='w') as f:
        f.write("graph name{\n")
        f.write(",".join(s)+color+";\n")
        for e in edges:
            f.write(e)
        f.write("}")
        print(f"{file_name}_s.dot")

    with open(f"{file_name}_t.dot", mode='w') as f:
        f.write("graph name{\n")
        f.write(",".join(t)+color+";\n")
        for e in edges:
            f.write(e)
        f.write("}")
        print(f"{file_name}_t.dot")


if __name__ == "__main__":
    main()
