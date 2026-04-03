import argparse
import datetime
import os
import collector
import display
import logger
import warn
import report
DEFAULT_INTERVAL = 2
BIGGEST_INVALID_INTERVAL = 0
FILE_TYPE_INDEX = 1

def handle_monitor(args, parser):
    checked_interval = check_interval(args.interval, parser)
    check_logging_path(args.log, "json", parser)
    logger.prepare_logger(args.log)
    warn.prepare_warn(args.cpu_warn, args.mem_warn)
    display.display_monitor(checked_interval)

def handle_report(args, parser):
    checked_date = check_date(args.date, parser)
    report_var = report.generate_report_data(args.src, checked_date)
    display.display_report(report_var)

def check_logging_path(logging_path, logging_format, parser):
    if logging_path:
        if not os.path.exists(logging_path):
            parser.exit(1,"Logging file path does not exist")
        file_type = os.path.splitext(logging_path)[FILE_TYPE_INDEX][1:]
        if file_type != logging_format:
            parser.exit(1, "Logging file path does not match specified format")

def check_date(date, parser):
    """Checks if date is with the format of YYYY-MM-DD, makes default date today.
    Args:
        date: the date being checked!
        parser: passed to exit if there is an error

    Return value:
        """
    if not date:
        date = datetime.datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.date.fromisoformat(date)
        except ValueError:
            parser.exit(1, "Date isn't in format. Should be written in YYYY-MM-DD format")
    return date

def check_interval(interval, parser):
    if interval<=BIGGEST_INVALID_INTERVAL:
        parser.exit(1, "Interval isn't in range. Should be greater than 0")
    return interval

def get_sys_readings(prev_bytes_sent, prev_bytes_recv, interval):
    """Gets from collector all data on cpu, disk, mem, network, and also logs it (if log flag is on)
    Args:
        prev_bytes_sent: the previous amount of bytes sent on network, essential for calculating network speed!
        prev_bytes_recv: the previous amount of bytes received on network, essential for calculating network speed!
        interval: time passed between 2 readings, again, essential for calculating network speed.

    Return value:
        dict{time: str(time), cpu: dict{str:list[str],str:str}, memory: dict{str:int,str:int,str:str}, disk: list[dict{str:str,str:int,str:int,str:str}],
        network: dict{str:str,str:str,str:int,str:int}}: a dict of string keys and corresponding values.
        -time is the time the reading was called (now)
        -cpu is the data from collector for cpu
        -memory is the data from collector for memory
        -disk is the data from collector for disk
        -network is the data from collector for network
        """
    system_readings = {"time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"cpu": collector.get_cpu_data(), "memory": collector.get_memory_data(),
                       "disk": collector.get_disk_data(), "network": collector.get_network_data(interval, prev_bytes_sent, prev_bytes_recv)}
    logger.log(system_readings)
    return system_readings


def main():
    """Parses args using argparse api. has 2 subcommands (monitor and report), each one having their own flags, and report has a non-optional argument.
    When being parsed argparse detects which subcommands with which flags, detects input errors if any, and corresponding to the subcommand turns on diff func.
    Also detects at all time if user types ctrl+c.
    Args:

    Return value:
    """
    parser = argparse.ArgumentParser(prog="sysmon")
    subparsers = parser.add_subparsers(title="subcommands")
    monitor_parser = subparsers.add_parser("monitor",
                                           help="gets realtime readings from CPU, memory, disks, and network. displays in CLI and logs them into specified log file")
    monitor_parser.set_defaults(func=handle_monitor)
    monitor_parser.add_argument("-i","--interval",type=float,default=DEFAULT_INTERVAL,help="set polling interval; default 2 secs")
    monitor_parser.add_argument("-l","--log",type=str,help="specify a log file path")
    monitor_parser.add_argument("--cpu_warn", action="store_true", help="when a cpu metric exceeds the threshold, trigger a desktop notification")
    monitor_parser.add_argument("--mem_warn", action="store_true", help="when a memory metric exceeds the threshold, trigger a desktop notification")
    report_parser = subparsers.add_parser("report",help="reads a log file and prints min/avg/max for each metric on a specific date")
    report_parser.set_defaults(func=handle_report)
    report_parser.add_argument("-d","--date", type=str, help="specify the date the report is supposed to be about in YYYY-MM-DD format; default today")
    report_parser.add_argument("src", type=str, help="specify the file from which the report will be based on")
    try:
        args = parser.parse_args()
        args.func(args, parser)
    except KeyboardInterrupt:
        parser.exit(0, "thanks for using sysmon!")




if __name__ == "__main__":
    main()