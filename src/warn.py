import display
memory_warn = False
cpu_warn = False
RED_STATUS = 2
YELLOW_STATUS = 1
GREEN_STATUS = 0

def prepare_warn(cpu_warn_flag, mem_warn_flag):
    global cpu_warn
    cpu_warn = cpu_warn_flag
    global memory_warn
    memory_warn = mem_warn_flag

def check_warning_percentage(percentage, is_cpu=False, is_mem=False):
    if is_cpu and cpu_warn:
        percentage_status = check_percentage_status(percentage)
        if percentage_status == RED_STATUS:
            display.add_warning(f"A CPU threshold has exceeded to {percentage}.")
        return color_percentage(percentage, percentage_status)
    elif is_mem and memory_warn:
        percentage_status = check_percentage_status(percentage)
        if percentage_status == RED_STATUS:
            display.add_warning(f"a memory threshold has exceeded to {percentage}.")
        return color_percentage(percentage, percentage_status)
    return percentage

def color_percentage(percentage, percentage_status):
        if percentage_status == RED_STATUS:
            return "[bold red]"+percentage+"[/bold red]"
        if percentage_status == YELLOW_STATUS:
            return "[yellow]" + percentage + "[/yellow]"
        if percentage_status == GREEN_STATUS:
            return "[green]" + percentage + "[/green]"
        return percentage #never supposed to get here

def check_percentage_status(percentage):
    if len(percentage) >5: #if it's a three digits num or bigger
        return RED_STATUS
    elif len(percentage)==4: #if it's a one digit num
        return GREEN_STATUS
    if int(percentage[0])>7: #if it's two digits num with tens above 7
        return RED_STATUS
    return RED_STATUS #if it's two digits num with tens not above 7
