import os
import pathlib

root = "D:\\file-lists-mods"
test = False
dry = False

if test:
    mod_first = 1
    mod_last = 1
    dir_count = 2
    file_count = 2
    max_depth = 5
else:
    mod_first = 1
    mod_last = 10
    dir_count = 5
    file_count = 5
    max_depth = 5


def log(s):
    if test:
        print(s)

def create_directory(mod_name, dir):
    path = os.path.join(root, mod_name, dir)
    log("create " + path)

    if not dry:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def create_file(mod_name, parent, name):
    path = os.path.join(root, mod_name, parent, name)
    log(path)

    if not dry:
        with open(path, "w") as f:
            f.write(name)

def make_dir_name(dir, depth):
    return chr(ord('a') + dir) * (depth + 1)

def make_file_name(mod_name, dir, file):
    return mod_name + "." + dir.replace("\\", ".") + "." + str(file + 1) + ".txt"

def do_dir(mod_name, parent):
    create_directory(mod_name, parent)
    for file in range(file_count):
        name = make_file_name(mod_name, parent, file)
        create_file(mod_name, parent, name)

def do_depth(mod_name, parent, dir_name, depth):
    if depth >= max_depth:
        return

    path = os.path.join(parent, dir_name)
    do_dir(mod_name, path)

    for dir in range(dir_count):
        dir_name = make_dir_name(dir, depth + 1)
        do_depth(mod_name, path, dir_name, depth + 1)

    if depth > 0:
        dir_name = mod_name + "." + parent.replace("\\", ".")
        do_dir(mod_name, os.path.join(parent, dir_name))

def do_mod(mod):
    mod_name = "mod-" + str(mod)
    print(mod_name + "... ", end="", flush=True)

    for dir in range(dir_count):
        dir_name = make_dir_name(dir, 0)
        print(dir_name + " ", end="", flush=True)
        do_depth(mod_name, "", dir_name, 0)

    print("", flush=True)

for mod in range(mod_first, mod_last + 1):
    do_mod(mod)
