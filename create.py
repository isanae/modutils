import random
from .mod import Mod, File, Download

DEFAULT_EXTENSION = "7z"

class CreateMods:
    def name(self):
        return "mods"

    def create_parser(self, sp):
        p = sp.add_parser(
            self.name(),
            help="creates mods with files in each",
            description="creates mods with files in each")

        p.add_argument(
            "--duplicate-hidden",
            action="store_true",
            help="creates a duplicate of each file by appending .mohidden to " +
                 "filenames")

        p.add_argument(
            "count",
            type=int,
            help="number of mods to create")

        p.add_argument(
            "files",
            type=int,
            help="number of files to create per mod")

        return p

    def run(self, cx):
        cx.clear_directory(cx.mods_directory())

        for i in range(cx.options.count):
            m = Mod("mod-" + str(i + 1))

            for i in range(cx.options.files):
                filename = str(i + 1)
                content = m.name() + " " + filename

                m.add_file(File(filename, content))

                if cx.options.duplicate_hidden:
                    m.add_file(File(filename + ".mohidden", content))

            m.create(cx)

        return 0


class CreateDownloads:
    def name(self):
        return "dls"

    def create_parser(self, sp):
        p = sp.add_parser(
            self.name(),
            help="creates dummy downloads",
            description="creates dummy downloads")

        p.add_argument(
            "--no-meta",
            action="store_true",
            help="disables creation of .meta files")

        p.add_argument(
            "--no-nexus",
            action="store_true",
            help="disables generation of random nexus ids")

        p.add_argument(
            "--ext",
            type=str,
            default=DEFAULT_EXTENSION,
            help="specifies extension (defaults to " +
                 "'" + DEFAULT_EXTENSION + "')")

        p.add_argument(
            "count",
            type=int,
            help="number of downloads to create")

        return p

    def run(self, cx):
        cx.clear_directory(cx.downloads_directory())

        for i in range(cx.options.count):
            name = "mod " + str(i + 1)
            d = self.create_download(cx, name)
            d.create(cx)

    def create_download(self, cx, name):
        nexus_id = None
        file_id = None
        version = self.generate_version()
        ext = cx.options.ext
        meta = not cx.options.no_meta

        if not cx.options.no_nexus:
            nexus_id = self.generate_nexus_id()
            file_id = self.generate_file_id()

        return Download(name, nexus_id, file_id, version, ext, meta)

    def generate_nexus_id(self):
        return random.randint(1000, 10000)

    def generate_file_id(self):
        return random.randint(1000, 10000)

    def generate_version(self):
        s = ""

        for i in range(random.randint(2, 3)):
            if s != "":
                s += "."

            s += str(random.randint(1, 10))

        return s
