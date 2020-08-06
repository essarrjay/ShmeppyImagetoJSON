import sys

def progressbar(it, prefix="", width=60, file=sys.stdout):
    """Usage:
    import time

    for i in progressbar(range(15), "Computing: ", 40):
    time.sleep(0.1) # any calculation you need
    """

    count = len(it)-1
    def show(j):
        x = int(width*(j)/count)
        bar = "#"*x
        remaining = "."*(width-x)
        num = j-1
        file.write(f"{prefix}[{bar}{remaining}]{num}/{count}\r")
        file.flush()
    show(1)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()
