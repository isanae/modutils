## Usage ##

1. Clone somewhere
2. Add parent path to PYTHONPATH
3. `cd` to MO's output directory, the one that contains `build/` and `install/`
4. Do `python -m modutils` for help and the list of commands
5. Get help for a command with `python -m modutils <command> --help`

By default, modutils will **take over** an instance named "mo-test", which has to be created manually beforehand. **Expect the contents of that instance to be deleted at any time.** Most commands will empty either the mods/ or downloads/ directory. The `--dry` option can be used to simulate all filesystem operations and the `dump` command will show all the paths used.

I'm dumping the help of all commands below.

## License ##
CC0 1.0 Universal. This project is in the public domain.

### mods ###
```
usage: modutils mods [-h] [--duplicate-hidden] count files

creates mods with files in each

positional arguments:
  count               number of mods to create
  files               number of files to create per mod

optional arguments:
  -h, --help          show this help message and exit
  --duplicate-hidden  creates a duplicate of each file by appending .mohidden
                      to filenames
```
                      
### dls ###
```
usage: modutils dls [-h] [--no-meta] [--no-nexus] [--ext EXT] count

creates dummy downloads

positional arguments:
  count       number of downloads to create

optional arguments:
  -h, --help  show this help message and exit
  --no-meta   disables creation of .meta files
  --no-nexus  disables generation of random nexus ids
  --ext EXT   specifies extension (defaults to '7z')
```

### overwrite ###
```
usage: modutils overwrite [-h]

creates files in the overwrite directory
```

### conflict ###
```
usage: modutils conflict [-h] file_count

Creates three mods: the first with files named 1 to N, the second with files
named 1 to N*3 and a third with files named N*2 to N*3. All files from the
first mods will be overwritten by the second mod, all files from the third mod
will overwrite files from the second mod, and the second mod will have N files
not overwritten by anything

positional arguments:
  file_count  number of conflicting files
```

### tree ###
```
usage: modutils tree [-h]

creates one mod with a varied file tree
```

### devbuild ###
```
usage: modutils devbuild [-h] [--no-bin] [--no-src] [--pdbs]
                         [--output-dir OUTPUT_DIR] [--version VERSION]
                         [--force]
                         build [name]

creates two archives in the current directory: one from install/bin/* and
another with the sources of projects in modorganizer_super

positional arguments:
  build                 build number
  name                  string to add to the 7z filenames

optional arguments:
  -h, --help            show this help message and exit
  --no-bin              skips the creation of the binaries archive
  --no-src              skips the creation of the sources archive
  --pdbs                creates another archive from install/pdbs/*
  --output-dir OUTPUT_DIR
                        sets the output directory instead of the current
                        directory
  --version VERSION     sets the version instead of getting it from
                        modorganizer.exe or version.rc
  --force               ignore file size warnings which could indicate bad
                        paths or unexpected files being pulled into the
                        archives
```
