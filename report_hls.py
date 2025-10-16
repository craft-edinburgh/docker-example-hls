#! /usr/bin/env python3
# ---------------------------------------
# This script runs cheri hls
# ---------------------------------------
import sys, os, time, logging, colorlog, functools, shutil, subprocess, glob
from argparse import ArgumentParser

# ---------------------------------------
# Report HLS
# ---------------------------------------


class ReportHLS:

    def __init__(self, args):
        self.args = args
        self.top = args.top
        self.project = args.project

    def run(self):
        if self.args.synth:
            self.report_synth()
        elif self.args.impl:
            self.report_impl()
        else:
            assert False, "Not valid option provided."

    def report_impl(self):
        cycles = self._get_cycles()
        impl_log = os.path.join(
            self.project, "hls", "impl", "report", "verilog", f"{self.top}_export.rpt"
        )

        luts = -1
        ffs = -1
        dsps = -1
        brams = -1
        fmax = -1

        flag = 0
        with open(impl_log) as lines:
            for line in lines:
                if "Post-Synthesis Resource usage" in line:
                    flag = 1
                if "synthesis end" in line:
                    flag = 0
                if flag > 0:
                    flag += 1
                if flag == 4:
                    luts = int(line[line.find(":") + 1 :])
                if flag == 5:
                    ffs = int(line[line.find(":") + 1 :])
                if flag == 6:
                    dsps = int(line[line.find(":") + 1 :])
                if flag == 7:
                    brams = int(line[line.find(":") + 1 :])
                if flag == 15:
                    fmax = 1000.0 / float(line[line.find(":") + 1 :])

        print("LUTs, FFs, DSPs, BRAMs, Cycles, Fmax,\n")
        print(f"{luts}, {ffs}, {dsps}, {brams}, {cycles}, {fmax},\n")

    def report_synth(self):
        cycles = self._get_cycles()
        synth_log = os.path.join(
            self.project, "hls", "syn", "report", f"{self.top}_csynth.rpt"
        )

        luts = -1
        ffs = -1
        dsps = -1
        brams = -1
        fmax = -1

        with open(synth_log) as lines:
            for line in lines:
                if "ap_clk" in line and fmax == -1:
                    val = line.split("|")
                    val = val[3].replace("ns", "")
                    fmax = 1000.0 / float(val)
                if "Total" in line:
                    val = line.split("|")
                    brams = int(val[2])
                    dsps = int(val[3])
                    ffs = int(val[4])
                    luts = int(val[5])
                    break

        print("LUTs, FFs, DSPs, BRAMs, Cycles, Fmax,")
        print(f"{luts}, {ffs}, {dsps}, {brams}, {cycles}, {fmax},")

    def _get_cycles(self):
        sim_log = os.path.join(
            self.project, "hls", "sim", "report", f"{self.top}_cosim.rpt"
        )
        cycles = -1
        with open(sim_log) as lines:
            for line in lines:
                if "Verilog|" in line:
                    c = line.split("|")
                    cycles = int(c[4])
        return cycles


# ---------- main function --------------
def cheri_hls():
    USAGE = """Usage:
report_hls.py -t top -p ./example/project_name -s 
"""

    parser = ArgumentParser(usage=USAGE)
    parser.add_argument(
        "-s",
        "--synthesis",
        action="store_true",
        dest="synth",
        default=False,
        help="Synthesis results - suitable for debugging",
    )
    parser.add_argument(
        "-i",
        "--impl",
        action="store_true",
        dest="impl",
        default=False,
        help="Implementation results - suitable for final reports",
    )
    parser.add_argument(
        "-p",
        "--project",
        dest="project",
        default=None,
        help="Project dir, e.g. ./example/project_name",
    )
    parser.add_argument(
        "-t",
        "--top",
        dest="top",
        default=None,
        help="Top design name, e.g. top",
    )

    args = parser.parse_args()

    r = ReportHLS(args)
    sys.exit(r.run())


if __name__ == "__main__":
    cheri_hls()
