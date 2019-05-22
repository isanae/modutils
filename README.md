## Usage ##

1. Clone somewhere
2. Add parent path to PYTHONPATH
3. `cd` to MO's output directory, the one that contains `build/` and `install/`
4. Do `python -m modutils` for help and the list of commands
5. Get help for a command with `python -m modutils <command> --help`

By default, modutils will **take over** an instance named "mo-test", which has to be created manually beforehand. **Expect the contents of that instance to be deleted at any time.** Most commands will empty either the mods/ or downloads/ directory. The `--dry` option can be used to simulate all filesystem operations and the `dump` command will show all the paths used.
