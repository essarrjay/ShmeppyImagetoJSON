import sys


def progress_bar(it, prefix="", suffix="", width=60, file=sys.stdout):
    """An iterable-like obj for command line progress_bar

    Usage:
    for i in progress_bar(range(15), "Processing: ",  "Part ", 40):
        <some long running calculation>

    Processing: [####################################] Part 16/16
    """

    count = len(it)

    def show(j):
        x = int(width*(j)/count)
        bar = "#"*x
        remaining = "."*(width-x)
        num = j
        file.write(f"{prefix}[{bar}{remaining}]{suffix}{num}/{count}\r")
        file.flush()

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()
