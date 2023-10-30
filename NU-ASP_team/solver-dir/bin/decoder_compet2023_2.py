#!/usr/bin/env python3


import re
import argparse


def get_recongo_result(line, old_result):
    if re.match("^s\sUNREACHABLE", line):
        return "UNREACHABLE"
    elif re.match("^s\sREACHABLE", line):
        return "REACHABLE"
    elif re.match("^s\sREACHABILITY\sUNKNOWN", line):
        return "REACHABILITY UNKNOWN"
    return old_result


def get_clingo_result(line, old_result):
    if re.match("^c\sResult:\sUNSAT", line) and old_result != "REACHABLE":
        return "UNKNOWN"
    elif re.match("^c\sResult:\sSAT", line):
        return "REACHABLE"
    return old_result


def get_answer(answer):
    ans = []
    for a in answer:
        m = re.match("in\((\d+),(\d+)\)", a)
        if m is not None:
            ans.append((int(m.group(1)), int(m.group(2))))
    ans.sort()
    return sorted(ans, key=lambda x: x[1])


def get_in(ans, num):
    in_state = []
    for a in ans:
        if a[1] == num:
            in_state.append(a[0])
    return in_state


def output_answer(answer, is_existent=False):
    step = 0

    if is_existent:
        s = step
        while True:
            in_state = get_in(answer, step)
            if not in_state:
                break
            elif get_in(answer, step) == get_in(answer, step-1):
                step += 1
                continue
            else:
                print_flush(f"a {' '.join([str(i) for i in in_state])}")
                step += 1
                s += 1
        step = s
    else:
        while True:
            in_state = get_in(answer, step)
            if not in_state:
                break
            else:
                print_flush(f"a {' '.join([str(i) for i in in_state])}")
                step += 1
    print_flush(f"c Step: {step-1}")


def decode(dat_file, log_file, is_existent=False):

    with open(dat_file) as df:
        for i in df.read().splitlines():
            print_flush(i)

    recongo_result = "REACHABILITY UNKNOWN"
    clingo_result = "UNKNOWN"
    recongo_answer = ""
    clingo_answer = ""
    with open(log_file) as lf:
        for line in lf:
            recongo_result = get_recongo_result(line, recongo_result)
            clingo_result = get_clingo_result(line, clingo_result)
            if re.match("^a\sAnswer:", line):
                recongo_answer = line
            if re.match("^Answer:\s1", line):
                clingo_answer = lf.readline()

    if recongo_result == "REACHABLE" or clingo_result == "REACHABLE":
        print_flush("a YES")
    elif recongo_result == "UNREACHABLE":
        print_flush("a NO")
        print_flush("c UNREACHABLE")
        return
    else:
        print_flush("c UNKNOWN")
        print_flush("c REACHABILITY UNKNOWN")
        return

    if recongo_answer != "":
        answer = get_answer(recongo_answer.split())
        output_answer(answer, is_existent)
    elif clingo_answer != "":
        answer = get_answer(clingo_answer.split())
        output_answer(answer, is_existent)

def print_flush(msg):
    print(msg, flush=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--existent', action='store_true', help='for at-most-one encoding')
    parser.add_argument('arg_col', help='Graph data  *.col')
    parser.add_argument('arg_dat', help='Start and Goal data  *.dat')
    parser.add_argument('arg_log', help='Solver LOG file  *.log ')

    args = parser.parse_args()

    decode(args.arg_dat, args.arg_log, args.existent)




if __name__ == "__main__":
    main()
