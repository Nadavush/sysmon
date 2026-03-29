

def color_percentage(percentage):
    if len(percentage)>5 or percentage=="100%":
        return "[bold red]"+percentage+"[/bold red]"
    elif len(percentage)==4 or int(percentage[0])<=7:
        return "[lime]"+percentage+"[/lime]"
    else:
        return "[yellow]"+percentage+"[/yellow]"
