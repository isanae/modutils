import os
import re
from ctypes import *
from pathlib import Path
from .log import *

# returns the requested version information from the given file
#
# `language` should be an 8-character string combining both the language and
# codepage (such as "040904b0"); if None, the first language in the translation
# table is used instead
#
def get_version_string(filename, what, language=None):
    # VerQueryValue() returns an array of that for VarFileInfo\Translation
    #
    class LANGANDCODEPAGE(Structure):
        _fields_ = [
            ("wLanguage", c_uint16),
            ("padding_", c_uint16),
            ("wCodePage", c_uint16)]

    wstr_file = wstring_at(filename)

    # getting the size in bytes of the file version info buffer
    size = windll.version.GetFileVersionInfoSizeW(wstr_file, None)
    if size == 0:
        raise WinError()

    buffer = create_string_buffer(size)

    # getting the file version info data
    if windll.version.GetFileVersionInfoW(wstr_file, None, size, buffer) == 0:
        raise WinError()

    # VerQueryValue() wants a pointer to a void* and DWORD; used both for
    # getting the default language (if necessary) and getting the actual data
    # below
    value = c_void_p(0)
    value_size = c_uint(0)

    if language is None:
        # file version information can contain much more than the version
        # number (copyright, application name, etc.) and these are all
        # translatable
        #
        # the following arbitrarily gets the first language and codepage from
        # the list
        ret = windll.version.VerQueryValueW(
            buffer, wstring_at(r"\VarFileInfo\Translation"),
            byref(value), byref(value_size))

        if ret == 0:
            raise WinError()

        # value points to a byte inside buffer, value_size is the size in bytes
        # of that particular section

        # casting the void* to a LANGANDCODEPAGE*
        lcp = cast(value, POINTER(LANGANDCODEPAGE))

        # formatting language and codepage to something like "040904b0"
        language = "{0:04x}{1:04x}".format(
            lcp.contents.wLanguage, lcp.contents.wCodePage)

    # getting the actual data
    res = windll.version.VerQueryValueW(
        buffer, wstring_at("\\StringFileInfo\\" + language + "\\" + what),
        byref(value), byref(value_size))

    if res == 0:
        raise WinError()

    # value points to a string of value_size characters
    return wstring_at(value.value, value_size.value)


def get_version_from_rc(rc):
    # matching: #define VER_FILEVERSION_STR "2.2.1\0"
    e = re.compile(r'#define VER_FILEVERSION_STR "(.+)\\0"')

    with open(rc, "r") as f:
        for line in f:
            m = e.match(line)
            if m:
                return m[1]

    return None


def byte_size_string(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class FileGatherer:
    def __init__(self, root):
        self.root_ = root
        self.ignore_ = []
        self.files_ = []
        self.total_ = 0

    def ignore(self, list):
        self.ignore_ = [re.compile(s) for s in list]

    def get(self):
        self.files_ = []
        self.total_ = 0

        self.add_dir(self.root_)

        return {"total_size": self.total_, "files": self.files_}

    def add_dir(self, dir):
        for entry in Path(dir).iterdir():
            if self.is_ignored(entry):
                continue

            if entry.is_dir():
                self.add_dir(entry)
            else:
                size = entry.stat().st_size
                path = str(entry)

                if not path.startswith(self.root_):
                    print("path doesn't start with root dir '{}'?", this.root_)
                    raise Exception()

                path = path[len(self.root_):]
                while path[0] == '/' or path[0] == '\\':
                    path = path[1:]

                self.files_.append((path, size))
                self.total_ += size

    def is_ignored(self, f):
        for e in self.ignore_:
            if e.match(f.name):
                return True

        return False

class DevBuild:
    def name(self):
        return "devbuild"

    def create_parser(self, sp):
        p = sp.add_parser(
            self.name(),
            help="creates dev builds",
            description="creates two archives in the current directory: " +
                        "one from install/bin/* and another with the sources "
                        "of projects in modorganizer_super")

        p.add_argument(
            "--no-bin",
            action="store_true",
            help="skips the creation of the binaries archive")

        p.add_argument(
            "--no-src",
            action="store_true",
            help="skips the creation of the sources archive")

        p.add_argument(
            "--pdbs",
            action="store_true",
            help="creates another archive from install/pdbs/*")

        p.add_argument(
            "--output-dir",
            type=str,
            default=os.getcwd(),
            help="sets the output directory instead of the current directory")

        p.add_argument(
            "--version",
            type=str,
            default=None,
            help="sets the version instead of getting it from "
                 "modorganizer.exe or version.rc")

        p.add_argument(
            "--force",
            action="store_true",
            help="ignore file size warnings which could indicate bad paths or "
                 "unexpected files being pulled into the archives")

        p.add_argument(
            "build",
            type=str,
            help="build number")

        p.add_argument(
            "name",
            type=str,
            default="",
            nargs="?",
            help="string to add to the 7z filenames")

        return p

    def run(self, cx):
        if not cx.options.no_bin:
            self.make_bin(cx)

        if cx.options.pdbs:
            self.make_pdbs(cx)

        if not cx.options.no_src:
            self.make_src(cx)

        return 0

    def make_bin(self, cx):
        info("making binary archive")

        install_dir = cx.install_directory()
        destination = cx.options.destination

        src = os.path.join(install_dir, "bin", "*")
        dest = os.path.join(destination, self.bin_filename(cx))
        cx.archive(src, dest)

    def make_pdbs(self, cx):
        info("making pdb archive")

        install_dir = cx.install_directory()
        destination = cx.options.destination

        src = os.path.join(install_dir, "pdb", "*")
        dest = os.path.join(destination, self.pdb_filename(cx))
        cx.archive(src, dest)

    def make_src(self, cx):
        info("making source archive")

        root_dir = cx.super_directory()
        destination = cx.options.destination

        ignore = [
            r"\..+",     # dot files
            r".*\.log",  # logs
            r".*\.tlog", # logs
            r".*\.dll",  # dll
            r".*\.exe",  # exe
            r".*\.lib",  # lib
            r".*\.obj",  # obj
            r".*\.ts",   # ts
            r".*\.aps",  # aps
            r"vsbuild"   # vsbuild
        ]

        fg = FileGatherer(root_dir)
        fg.ignore(ignore)
        r = fg.get()

        # should be below 20MB
        max_expected_size = 20 * 1024 * 1024
        if self.too_large(cx, r, max_expected_size):
            return

        files = []
        for f in r["files"]:
            files.append(f[0])

        dest = os.path.join(destination, self.src_filename(cx))
        cx.archive_files(files, dest, root_dir)

    def too_large(self, cx, r, max):
        if r["total_size"] <= max:
            return

        print("total size of source files would be {}, expected something "
              "below {}, something might be wrong".format(
                    byte_size_string(r["total_size"]),
                    byte_size_string(max)))

        if cx.options.force:
            print("but --force is specified, ignoring")
            return True

        print("use --force to ignore")
        print("dumping top 10 largest files:")

        list = sorted(r["files"], key=lambda f: f[1], reverse=True)

        for i in range(len(list)):
            if i >= 10:
                break

            print(list[i][0] + " " + byte_size_string(list[i][1]))

        return False

    def bin_filename(self, cx):
        return self.build_filename(
            cx.options.name, self.version(cx), cx.options.build)

    def src_filename(self, cx):
        return self.build_filename(
            cx.options.name, self.version(cx), cx.options.build, "-src")

    def pdb_filename(self, cx):
        return self.build_filename(
            cx.options.name, self.version(cx), cx.options.build, "-pdbs")

    def build_filename(self, name, version, build, more=""):
        prefix = "Mod.Organizer"
        suffix = ".7z"

        s = ""

        # version
        if version is not None:
            s += "-" + version

        # name
        if name is not None and name != "":
            s += "-" + name

        # build
        s += "-build" + build

        # more
        s += more

        return prefix + s + suffix

    def version(self, cx):
        exe = os.path.join(cx.install_directory(), "bin", "ModOrganizer.exe")
        rc = os.path.join(cx.super_directory(), "modorganizer", "src", "version.rc")

        v = None
        try:
            v = get_version_string(ec, "FileVersion")
            if v == "" or v is None:
                warn("failed to get FileVersion from '{}'", exe)
                v = None
        except:
            pass

        if v is None:
            v = get_version_from_rc(rc)

        if v is None:
            error("can't get version number")

        return v
