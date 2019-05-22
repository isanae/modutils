import os
import configparser
from .operations import DryOperations, RealOperations

class Context:
    SRC_PATH = os.path.join("build", "modorganizer_super", "modorganizer", "src")

    def __init__(self, opts):
        self.ops_ = None
        self.options = opts
        self.mods_ = None
        self.dl_ = None

        if self.options.install_dir is None:
            self.options.install_dir = os.path.join(self.options.output_dir, "install")

        if self.options.dry:
            print("this is a dry run")
            self.ops_ = DryOperations()
        else:
            self.ops_ = RealOperations()

        if not self.options.no_ini:
            self.read_ini()

    def read_ini(self):
        # hack: don't throw for 'dump', let it run and warn the user instead
        if self.options.command == "dump":
            try:
                self.read_ini_impl()
            except:
                pass
        else:
            self.read_ini_impl()

    def read_ini_impl(self):
        cp = configparser.ConfigParser()
        cp.read_file(open(self.settings_ini()))

        if "download_directory" in cp["Settings"]:
            self.dl_ = os.path.normpath(cp["Settings"]["download_directory"])

        if "mod_directory" in cp["Settings"]:
            self.mods_ = os.path.normpath(cp["Settings"]["mod_directory"])

    def settings_ini(self):
        return os.path.join(self.instance_directory(), "ModOrganizer.ini")

    def instance_directory(self):
        return os.path.join(self.options.base_dir, self.options.instance)

    def mods_directory(self):
        if self.mods_ is not None:
            return self.mods_

        return os.path.join(self.instance_directory(), "mods")

    def downloads_directory(self):
        if self.dl_ is not None:
            return self.dl_

        return os.path.join(self.instance_directory(), "downloads")

    def install_directory(self):
        if self.options.install_dir is not None:
            return self.options.install_dir

        return os.path.join(self.options.output_dir, "install")

    def src_directory(self):
        if self.options.src_dir is not None:
            return self.options.src_dir

        return os.path.join(self.options.output_dir, Context.SRC_PATH)

    def clear_directory(self, path):
        path = os.path.normpath(path)
        print("clearing directory " + path)
        self.ops_.clear_directory(path)

    def create_directory(self, path):
        path = os.path.normpath(path)
        print("creating directory " + path)
        self.ops_.create_directory(path)

    def write_file(self, path, content):
        path = os.path.normpath(path)
        print("writing to " + path)
        self.ops_.write_file(path, content)

    def archive(self, input, output):
        input = os.path.normpath(input)
        output = os.path.normpath(output)
        print("archiving " + input + " into " + output)
        self.ops_.archive(input, output)

    def archive_string(self, path, content):
        print("archiving temp data into archive, archived filename is " + path)
        return self.ops_.archive_string(path, content)

    def dump(self):
        print("options:")
        for k, v in vars(self.options).items():
            print(" . " + k + "=" + str(v))

        print("paths:")
        print("  . instance:  " + self.dump_instance())
        print("  . ini:       " + self.dump_ini())
        print("  . mods:      " + self.dump_mods())
        print("  . downloads: " + self.dump_downloads())
        print("  . install:   " + self.dump_install())
        print("  . src:       " + self.dump_src())

    def dump_instance(self):
        return self.dump_path(False, self.instance_directory())

    def dump_ini(self):
        return self.dump_path(False, self.settings_ini())

    def dump_mods(self):
        return self.dump_path(self.mods_ is not None, self.mods_directory())

    def dump_downloads(self):
        return self.dump_path(self.dl_ is not None, self.downloads_directory())

    def dump_install(self):
        p = self.install_directory()
        ok = os.path.exists(os.path.join(p, "bin", "ModOrganizer.exe"))
        return self.dump_path_string(ok, False, p)

    def dump_src(self):
        p = self.src_directory()
        ok = os.path.exists(os.path.join(p, "main.cpp"))
        return self.dump_path_string(ok, False, p)

    def dump_path(self, ini, p):
        return self.dump_path_string(os.path.exists(p), ini, p)

    def dump_path_string(self, ok, ini, p):
        s = ""

        if ok:
            s = "[OK] "
        else:
            s = "[BAD]"

        s += " "

        if ini:
            s += "[INI] "
        else:
            s += "      "

        return p + " " + s


class Dump:
    def name(self):
        return "dump"

    def create_parser(self, sp):
        p = sp.add_parser(
            self.name(),
            help="dumps all settings used by this script",
            description="dumps all settings used by this script")

        return p

    def run(self, cx):
        cx.dump()
        return 0
