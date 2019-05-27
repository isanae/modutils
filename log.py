from enum import Flag, auto

class LogLevels(Flag):
    NONE = 0
    ERROR = auto()
    WARN = auto()
    INFO = auto()
    OPERATIONS = auto()


log_level = LogLevels.INFO | LogLevels.WARN | LogLevels.ERROR

def set_log_level(lv):
    global log_level
    log_level = lv

def add_log_level(lv):
    global log_level
    log_level |= lv

def info(s, *args):
    if log_level & LogLevels.INFO:
        print(s.format(*args))

def warn(s, *args):
    if log_level & LogLevels.WARN:
        print(s.format(*args))

def error(s, *args):
    if log_level & LogLevels.ERROR:
        print(s.format(*args))

def log_op(s, *args, **kwargs):
    if log_level & LogLevels.OPERATIONS:
        print(s.format(*args))

def make_table(rows):
    longest = 0
    for k, v in rows:
        longest = max(longest, len(k))

    s = ""
    for k, v in rows:
        if s != "":
            s += "\n"

        f = "{:<" + str(longest) + "} = {}"
        s += (" . " + f).format(k, str(v))

    return s
