import display
memory_warn = False
cpu_warn = False
RED_STATUS = 2
YELLOW_STATUS = 1
GREEN_STATUS = 0

def prepare_warn(cpu_warn_flag, mem_warn_flag):
    """Assigns global values corresponding to user input
    Args:
        cpu_warn_flag: whether or not --cpu_warn was in input
        mem_warn_flag: whether or not --mem_warn was in input

    Return value:"""
    global cpu_warn
    cpu_warn = cpu_warn_flag
    global memory_warn
    memory_warn = mem_warn_flag

def check_warning_percentage(percentage, is_cpu):
    """Checks if a percentage should or should not be colored. For that it checks if the corresponding flag is on,
    uses check_percentage_status() to see what color should it be painted with, checks if red then also add warning
    message, and last but not least add fitting colors.
    Args:
        percentage: the value being checked if and what color should it have
        is_cpu: is the percentage a cpu value or a mem value. True = cpu, False = mem

    Return value: str(percentage)
        """
    if is_cpu and cpu_warn:
        percentage_status = __check_percentage_status(percentage)
        if percentage_status == RED_STATUS:
            display.add_warning(f"A CPU threshold has exceeded to {percentage}.")
        return __color_percentage(percentage, percentage_status)
    elif (not is_cpu) and memory_warn:
        percentage_status = __check_percentage_status(percentage)
        if percentage_status == RED_STATUS:
            display.add_warning(f"A memory threshold has exceeded to {percentage}.")
        return __color_percentage(percentage, percentage_status)
    return percentage

def __color_percentage(percentage, percentage_status):
        if percentage_status == RED_STATUS:
            return "[bold red]"+percentage+"[/bold red]"
        if percentage_status == YELLOW_STATUS:
            return "[yellow]" + percentage + "[/yellow]"
        else:
            return "[green]" + percentage + "[/green]"

def __check_percentage_status(percentage):
    if len(percentage) >5: #if it's a three digits num or bigger
        return RED_STATUS
    elif len(percentage)==4: #if it's a one digit num
        return GREEN_STATUS
    if int(percentage[0])>7: #if it's two digits num with tens above 7
        return YELLOW_STATUS
    return GREEN_STATUS #if it's two digits num with tens not above 7
