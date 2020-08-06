import sys

def progressbar(it, prefix="", width=60, file=sys.stdout):
    """Usage:
    for i in progressbar(range(15), "Computing: ", 40):
        <some long running calculation>
    """

    count = len(it)
    def show(j):
        x = int(width*(j)/count)
        bar = "#"*x
        remaining = "."*(width-x)
        num = j
        file.write(f"{prefix}[{bar}{remaining}]{num}/{count}\r")
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()
