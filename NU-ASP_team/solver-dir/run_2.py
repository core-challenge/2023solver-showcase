import sys, os, shutil, subprocess, tempfile
import argparse
import re
import signal

HEADPATH = os.path.dirname(__file__)
TMP_DIR_PATH = tempfile.mkdtemp(prefix="run")
BIN_DIR_PATH = os.path.join(HEADPATH, "bin")
ENC_DIR_PATH = os.path.join(HEADPATH, "encoding")
SOLVER_DIR_PATH = os.path.join(HEADPATH, "solver")
RECONGO_CONFIG_BASIC = ["--heu=domain", "--stats"]
OUTPUT_SEP = "-" * 30

from bin import decoder_compet2023_2 as decoder

def setup():
    signal.signal(signal.SIGTERM, sig_handler)
    os.makedirs(TMP_DIR_PATH, exist_ok=True)

def set_parser():
    parser = argparse.ArgumentParser(description=
                                     "This script is for running recongo in CoRe Challenge 2023")
    parser.add_argument("input_col_file",
                        help="input .col file by CoRe Challenge 2023")
    parser.add_argument("input_dat_file",
                        help="input .dat file by CoRe Challenge 2023")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="output verbose result as comments")
    parser.add_argument("--unremoved",
                        help="not removed temporary working directory for debug")
    parser.add_argument("-t", "--thread", type=int, choices=range(1, 65),
                        help="the number of threads in running recongo")
    parser.add_argument("--na", action="store_true",
                        help="runnin recongo in sequential portforios for existent")
    track_group = parser.add_mutually_exclusive_group(required=True)
    track_group.add_argument("--existent", action="store_true",
                             help="flag for existent track")
    track_group.add_argument("--shortest", action="store_true",
                             help="flag for shortest track")
    track_group.add_argument("--longest", action="store_true",
                             help="flag for longest track")
    return parser


def sig_handler(signum, frame) -> None:
    sys.exit(1)
#    sys.exit()

def run_existent(args):
    ENC_ISRP = "compet2023_existent.lp"
    ENC_ISP = "isp.lp"
    ENC_NA_PREPRO = "prepro.lp"
    ENC_NA_SOLVE = "solve_AL.lp"
    NA_TIMELIMIT = 5 * 60
    ISP_TIMELIMIT = 1 * 60
    recongo_config = RECONGO_CONFIG_BASIC + ["--istrategy=exp"]
    if args.thread is not None:
        recongo_config.append("-t" + str(args.thread))

    input_col = args.input_col_file
    input_dat = args.input_dat_file
    col_file_name = os.path.splitext(os.path.basename(input_col))[0]
    dat_file_name = os.path.splitext(os.path.basename(input_dat))[0]
    lp_col = col_file_name + ".lp"
    lp_dat = dat_file_name + ".lp"
    instance = [os.path.join(TMP_DIR_PATH, lp_col), os.path.join(TMP_DIR_PATH, lp_dat)]
    log_na_file = dat_file_name + "__na.log"
    log_isp_file = dat_file_name + "__isp.log"
    log_isrp_file = dat_file_name + ".log"

    # convert to ASP fact
    convert_instance(input_col, input_dat)

    # run numeric abstraction
    if args.na:
        with open(os.path.join(TMP_DIR_PATH, log_na_file), "w") as fp:
            cmd = ["clingo"] + instance\
                + [os.path.join(ENC_DIR_PATH, "numeric_abstraction", ENC_NA_PREPRO)]\
                + [os.path.join(ENC_DIR_PATH, "numeric_abstraction", ENC_NA_SOLVE)]\
                + ["--time-limit=" + str(NA_TIMELIMIT), "--stats"]
            if args.thread is not None:
                cmd.append("-t" + str(args.thread))
            else:
                cmd.append("--config=frumpy")
            print_verbose(args.verbose, "CMD", " ".join(cmd))
            subprocess.run(cmd, stdout = fp)
        with open(os.path.join(TMP_DIR_PATH, log_na_file), "r") as fp:
            lines = fp.readlines()
            for line in lines:
                if (re.match("UNSATISFIABLE", line)):
                    return

    # run isp
    with open(os.path.join(TMP_DIR_PATH, log_isp_file), "w") as fp:
        cmd = ["clingo"] + instance\
            + [os.path.join(ENC_DIR_PATH, "isp", ENC_ISP)]\
            + ["-n0", "--time-limit=" + str(ISP_TIMELIMIT), "--quiet=1,0", "--stats"]
        if args.thread is not None:
            cmd.append("-t" + str(args.thread))
        print_verbose(args.verbose, "CMD", " ".join(cmd))
        subprocess.run(cmd, stdout = fp)

    with open(os.path.join(TMP_DIR_PATH, log_isp_file), "r") as fp:
        lines = fp.readlines()
        for line in lines:
            check = re.match("Models\s+: (\d+)\n", line)
            if check is not None:
                model_num = check[1]
                recongo_config.append("--imax=" + model_num)

    # run recongo
    with open(os.path.join(TMP_DIR_PATH, log_isrp_file), "w") as fp:
        cmd = ["python", os.path.join(SOLVER_DIR_PATH, "recongo_compet2023.py")]\
            + instance + [os.path.join(ENC_DIR_PATH, "isrp_inc", ENC_ISRP)]\
            + recongo_config
        print_verbose(args.verbose, "CMD", " ".join(cmd))
        subprocess.run(cmd, stdout = fp)

def run_longest(args):
    ENC_ISRP = "compet2023_longest.lp"
    recongo_config = RECONGO_CONFIG_BASIC + ["--isearch=longest"]
    if args.thread is not None:
        recongo_config.append("-t" + str(args.thread))
    
    input_col = args.input_col_file
    input_dat = args.input_dat_file
    col_file_name = os.path.splitext(os.path.basename(input_col))[0]
    dat_file_name = os.path.splitext(os.path.basename(input_dat))[0]
    lp_col = col_file_name + ".lp"
    lp_dat = dat_file_name + ".lp"
    instance = [os.path.join(TMP_DIR_PATH, lp_col), os.path.join(TMP_DIR_PATH, lp_dat)]
    log_file = dat_file_name + ".log"
    
    # convert to ASP fact
    convert_instance(input_col, input_dat)

    # run solver
    with open(os.path.join(TMP_DIR_PATH, log_file), "w") as fp:
        cmd = ["python", os.path.join(SOLVER_DIR_PATH, "recongo_compet2023.py")]\
            + instance + [os.path.join(ENC_DIR_PATH, "isrp_inc", ENC_ISRP)]\
            + recongo_config
        print_verbose(args.verbose, "CMD", " ".join(cmd))
        subprocess.run(cmd, stdout = fp)

def run_shortest(args):
    ENC_ISRP = "compet2023_existent.lp"
    recongo_config = RECONGO_CONFIG_BASIC
    if args.thread is not None:
        recongo_config.append("-t" + str(args.thread))
    
    input_col = args.input_col_file
    input_dat = args.input_dat_file
    col_file_name = os.path.splitext(os.path.basename(input_col))[0]
    dat_file_name = os.path.splitext(os.path.basename(input_dat))[0]
    lp_col = col_file_name + ".lp"
    lp_dat = dat_file_name + ".lp"
    instance = [os.path.join(TMP_DIR_PATH, lp_col), os.path.join(TMP_DIR_PATH, lp_dat)]
    log_file = dat_file_name + ".log"
    
    # convert to ASP fact
    convert_instance(input_col, input_dat)

    # run solver
    with open(os.path.join(TMP_DIR_PATH, log_file), "w") as fp:
        cmd = ["python", os.path.join(SOLVER_DIR_PATH, "recongo_compet2023.py")]\
            + instance + [os.path.join(ENC_DIR_PATH, "isrp_inc", ENC_ISRP)]\
            + recongo_config
        print_verbose(args.verbose, "CMD", " ".join(cmd))
        subprocess.run(cmd, stdout = fp)

def decode(args) -> None:
    input_col = args.input_col_file
    input_dat = args.input_dat_file
    log_na_file = os.path.splitext(os.path.basename(input_dat))[0] + "__na.log"
    log_isp_file = os.path.splitext(os.path.basename(input_dat))[0] + "__isp.log"
    log_isrp_file = os.path.splitext(os.path.basename(input_dat))[0] + ".log"
    log_na_path = os.path.join(TMP_DIR_PATH, log_na_file)
    log_isp_path = os.path.join(TMP_DIR_PATH, log_isp_file)
    log_isrp_path = os.path.join(TMP_DIR_PATH, log_isrp_file)
    
    fp_na, fp_isrp = None, None
    read_log_na = None
    
    if args.na and args.existent:
        fp_na = open(log_na_path, "r")
    if os.path.exists(log_isrp_path):
        fp_isrp = open(log_isrp_path, "r")

    if fp_na is not None:
        read_log_na = fp_na.read()
        if re.search(r"UNSATISFIABLE", read_log_na):
            with open(input_dat, "r") as fp_dat:
                print(fp_dat.read(), end="")
            print_answer("NO")
            print_comment("UNREACHABLE")


    if fp_isrp is not None:
        decoder.decode(input_dat, log_isrp_path, args.existent)

    if args.verbose:
        if fp_na is not None:
            print_comment(OUTPUT_SEP)
            print_comment("clingo output for numeric abstraction")
            lines = read_log_na.split("\n")
            for line in lines:
                if line:
                    print_comment(line)

        if os.path.exists(log_isp_path):
            print_comment(OUTPUT_SEP)
            print_comment("clingo output for model counting")
            with open(log_isp_path, "r") as fp_isp:
                lines = fp_isp.read().split("\n")
                for line in lines:
                    if line:
                        print_comment(line)
    
        if fp_isrp is not None:
            print_comment(OUTPUT_SEP)
            print_comment("recongo output")
            lines = fp_isrp.read().split("\n")
            for line in lines:
                if line:
                    print_comment(line)

    if fp_na is not None:
        fp_na.close()
    if fp_isrp is not None:
        fp_isrp.close()


def convert_instance(col, dat) -> None:
    col_file_name = os.path.splitext(os.path.basename(col))[0]
    dat_file_name = os.path.splitext(os.path.basename(dat))[0]
    lp_col = col_file_name + ".lp"
    lp_dat = dat_file_name + ".lp"
    with open(os.path.join(TMP_DIR_PATH, lp_col), "w") as fp:
        cmd = ["ruby", os.path.join(BIN_DIR_PATH, "col_2_lp.rb"), col]
        subprocess.run(cmd, stdout = fp)
    with open(os.path.join(TMP_DIR_PATH, lp_dat), "w") as fp:
        cmd = ["ruby", os.path.join(BIN_DIR_PATH, "dat_2_lp.rb"), dat]
        subprocess.run(cmd, stdout = fp)

def print_message(*args) -> None:
    elems = [str(x) for x in args]
    print(" ".join(elems), flush=True)

def print_answer(*args) -> None:
    print_message('a', *args)

def print_comment(*args) -> None:
    print_message('c', *args)

def print_verbose(flag, *args) -> None:
    if flag:
        print_comment(*args)

def cleanup(args) -> None:
    if args.unremoved is not None:
        path = os.path.join(os.getcwd(), args.unremoved, str(os.getpid()))
        shutil.copytree(TMP_DIR_PATH, path)
        print_comment("unremoved option is ON")
        print_comment("path: ", path)
    shutil.rmtree(TMP_DIR_PATH)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)

def main():
    setup()
    args = set_parser().parse_args()
    print_comment(args.input_col_file)
    print_comment(args.input_dat_file)
    try:
        if args.existent:
            run_existent(args)
        elif args.longest:
            run_longest(args)
        else:
            run_shortest(args)

    except:
        pass

    finally:
        decode(args)
        cleanup(args)
#        exit()

if __name__ == "__main__":
    main()
