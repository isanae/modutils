import os
import re
from ctypes import *

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


class DevBuild:
    def name(self):
        return "devbuild"

    def create_parser(self, sp):
        p = sp.add_parser(
            self.name(),
            help="creates dev builds",
            description="creates two 7z archives in the current directory " +
                        "from install/bin/* and install/pdbs/*")

        p.add_argument(
            "--no-bin",
            action="store_true",
            help="skips the creation of the binaries archive")

        p.add_argument(
            "--no-pdbs",
            action="store_true",
            help="skips the creation of the pdbs archive")

        p.add_argument(
            "--output-dir",
            type=str,
            default=os.getcwd(),
            help="sets the output directory instead of the current directory")

        p.add_argument(
            "--version",
            type=str,
            default=None,
            help="sets the version instead of getting it from version.rc")

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
        install_dir = cx.install_directory()
        output_dir = cx.options.output_dir

        if not cx.options.no_bin:
            src = os.path.join(install_dir, "bin", "*")
            dest = os.path.join(output_dir, self.make_filename(cx))

            cx.archive(src, dest)

        if not cx.options.no_pdbs:
            src = os.path.join(install_dir, "pdb", "*")
            dest = os.path.join(output_dir, self.make_filename(cx, "-pdbs"))

            cx.archive(src, dest)

        return 0

    def make_filename(self, cx, more=""):
        prefix = "Mod.Organizer"
        suffix = ".7z"

        s = ""

        # version
        v = self.version(cx)
        if v is not None:
            s += "-" + v

        # name
        s += "-" + cx.options.name

        # build
        if not s.startswith("build"):
            s += "build"
        s += cx.options.build

        # more
        s += more

        return prefix + s + suffix

    def version(self, cx):
        exe = os.path.join(cx.install_directory(), "bin", "ModOrganizer.exe")
        rc = os.path.join(cx.src_directory(), "version.rc")

        v = None
        try:
            v = get_version_string(rc, "FileVersion")
            if v == "":
                v = None
        except:
            pass

        if v is None:
            v = get_version_from_rc(rc)

        if v is None:
            print("can't get version number")

        return v
