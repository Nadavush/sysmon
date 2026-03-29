import argparse
import datetime
import collector
import display
import os

DEFAULT_INTERVAL = 2

def parse_monitor(args, parser):
    checked_interval = check_interval(args.interval, parser)
    display.display_monitor(checked_interval)


def parse_report(args, parser):
    checked_date = check_date(args.date, parser)
    #report_var = report.doyourthing()
    #display.displayreport()



def check_date(date, parser):
    if not date:
        date = datetime.datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.date.fromisoformat(date)
        except ValueError:
            parser.exit(1, "Date isn't in format. Should be written in YYYY-MM-DD format")
    return date

def check_interval(interval, parser):
    if interval<=0:
        parser.exit(1, "Interval isn't in range. Should be greater than 0")
    return interval

def get_sys_readings(prev_bytes_sent, prev_bytes_recv, interval):
    return collector.get_cpu_data(),collector.get_memory_data(), collector.get_disk_data(), collector.get_network_data(interval, prev_bytes_sent, prev_bytes_recv)


def main():
    parser = argparse.ArgumentParser(prog="sysmon")
    try:
        subparsers = parser.add_subparsers(title="subcommands")
        monitor_parser = subparsers.add_parser("monitor", help="gets realtime readings from CPU, memory, disks, and network. displays in CLI and logs them into specified log file")
        monitor_parser.set_defaults(func=parse_monitor)
        report_parser = subparsers.add_parser("report",help="reads a log file and prints min/avg/max for each metric on a specific date")
        report_parser.set_defaults(func=parse_report)
        monitor_parser.add_argument("-i","--interval",type=float,default=DEFAULT_INTERVAL,help="set polling interval; default 2 secs")
        monitor_parser.add_argument("-l","--log",type=str,help="specify a log file path")
        monitor_parser.add_argument("--cpu_warn", action="store_true", help="when a cpu metric exceeds the threshold, trigger a desktop notification")
        monitor_parser.add_argument("--mem_warn", action="store_true", help="when a memory metric exceeds the threshold, trigger a desktop notification")
        monitor_parser.add_argument("-f","--format",type=str,default="json",choices=["json","csv"],help="support json/csv for the log output; default is json")
        report_parser.add_argument("-d","--date", type=str,help="specify the date the report is supposed to be about in YYYY-MM-DD format; default today")
        args = parser.parse_args()
        args.func(args, parser)
    except KeyboardInterrupt:
        parser.exit(0, "thanks for using sysmon!")


if __name__ == "__main__":
    main()