#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@author Shuji Kosuge
version: 1.0
"""

import sys
import getopt
from graphviz import Graph
import re
import datetime
import os
import glob
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def usage(msg=""):
    if msg != "":
        print(msg)
    config = Config()
    print(f"Usage: python3 {sys.argv[0]} <options> col_file sol_file")
    print(f"    -h --help               : show this help")
    print(f"    -o --output file_name   : output file name.      default='{config.output_file}'")
    print(f"    -d --directory name     : output directory name. default='YYYY-mm-dd_HH-MM-SS'")
    print(f"    -e --engine value       : graphviz engine.       default='{config.engine}'")
    print(f"                              example: dot, neato, twopi, circo, fdp, osage, patchwork, sfdp")
    print(f"    -c --color value        : node color.            default='{config.fill_color}'")
    print(f"    -f --format extension   : picture format.        default='{config.format}'")
    print(f"    -i --interval value     : gif interval.          default={config.interval}")
    print(f"    -r --repeat_delay value : gif repeat_delay.      default={config.repeat_delay}")

    exit()


class Config:
    def __init__(self
                 , output_file="output"
                 , engine="dot"
                 , format="png"
                 , shape="circle"
                 , fontname="MS Gothic"
                 , fill_color="red"
                 , interval=200
                 , repeat_delay=1000
                 ):
        self.folder_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.output_file = output_file
        self.engine = engine
        self.format = format
        self.shape = shape
        self.fontname = fontname
        self.fill_color = fill_color
        self.interval = interval
        self.repeat_delay = repeat_delay


def read_solution(log_file):
    sol = []
    with open(log_file) as f:
        for line in f:
            a = re.match(r"^a\s([\d\s]+)", line)
            if a is not None:
                sol.append(a.group(1).split())
    return sol


def create_graph(col_file, config):
    gv = Graph(engine=config.engine, format=config.format)
    gv.attr('node', shape=config.shape, fontname=config.fontname)

    with open(col_file) as f:
        for line in f:
            e = re.match(r"^e\s(\d+)\s+(\d+)", line)
            if e is not None:
                gv.edge(e.group(1), e.group(2))

    return gv


def draw_step(gv, sol, num, step, config):
    for s in sol:
        gv.node(s, fillcolor=config.fill_color, style="filled")
    num_str = format(num, f"0{len(str(step))}")  # 数値を0埋め
    gv.render(f"{num_str}_{config.output_file}", directory=config.folder_name)
    update_print(f"Output ./{config.folder_name}/{num_str}_{config.output_file}.png", num, step)


def update_print(msg, num, step):
    progress = float(format(num/step, '.5f'))
    done = "■"*int(progress*10)
    progress_str = '{:□<10}'.format(done)
    print(f"  {progress_str}  {int(progress*100)}%")
    if num != step:
        print(f"{msg}\n\033[2A", end="")
    else:
        print(f"{msg}")


def create_gif(config):
    fig = plt.figure()
    plt.axis("off")
    pic_list = sorted(glob.glob(config.folder_name + "/[0-9]*." + config.format))
    ims = []
    for i in range(len(pic_list)):
        tmp = Image.open(pic_list[i])
        ims.append([plt.imshow(tmp)])
    ani = animation.ArtistAnimation(fig, ims, interval=config.interval, repeat_delay=config.repeat_delay)
    ani.save(f"./{config.folder_name}/{config.output_file}.gif", writer="pillow")
    print(f"Output ./{config.folder_name}/{config.output_file}.gif")


"""
main
"""


def main():
    config = Config()
    try:
        opts, args = getopt.getopt(sys.argv[1:]
                                   , "ho:d:f:i:r:e:c:"
                                   , ["help"
                                       , "output="
                                       , "directory="
                                       , "format="
                                       , "interval="
                                       , "repeat_delay="
                                       , "engine="
                                       , "color="
                                      ]
                                   )

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
            elif opt in ("-o", "--output"):
                print(f"output_file = {arg}")
                config.output_file = arg
            elif opt in ("-d", "--directory"):
                print(f"directory = {arg}")
                config.folder_name = arg
            elif opt in ("-f", "--format"):
                print(f"format = {arg}")
                config.format = arg
            elif opt in ("-i", "--interval"):
                print(f"interval = {arg}")
                config.interval = int(arg)
            elif opt in ("-r", "--repeat_delay"):
                print(f"repeat_delay = {arg}")
                config.repeat_delay = int(arg)
            elif opt in ("-e", "--engine"):
                print(f"engine = {arg}")
                config.engine = arg
            elif opt in ("-c", "--color"):
                print(f"color = {arg}")
                config.fill_color = arg

        if len(args) != 2:
            usage("please input col-file and solution-file.")

    except getopt.GetoptError as err:
        print(str(err))
        usage()

    # make directory
    try:
        os.makedirs(config.folder_name)
    except FileExistsError:
        pass

    # read solution
    sol = read_solution(args[1])

    # create pictures
    print("\nmaking pictures...")
    for i in range(len(sol)):
        original_gv = create_graph(args[0], config)
        draw_step(original_gv, sol[i], i+1, len(sol), config)

    # create gif
    print("\nmaking gif...")
    create_gif(config)


if __name__ == "__main__":
    main()
