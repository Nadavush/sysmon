import argparse
import os

DEFAULT_INTERVAL = 2
def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--interval",type=float,default=DEFAULT_INTERVAL,help="set polling interval; default 2 secs")
    parser.add_argument("-l","--log",type=str,help="specify a log file path; if not specified, creates a new folder with log file in the program's directory")
    parser.add_argument("--cpu_warn", action="store_true", help="when a cpu metric exceeds the threshold, trigger a desktop notification")
    parser.add_argument("--mem_warn", action="store_true", help="when a memory metric exceeds the threshold, trigger a desktop notification")
    parser.add_argument("-f","--format",type=str,default="json",choices=["json","csv"],help="support json/csv for the log output; default is json")
    parser.add_argument("-d","--date", type=str,help="reads a log file and prints min/avg/max for each metric on that day")
    args = parser.parse_args()

    polling_interval = args.interval
    if args.cpu_warn:
        print("cpu warned")
    if args.mem_warn:
        print("mem warned")



def main():
    parse_input()


if __name__ == "__main__":
    main()