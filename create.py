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
            "--esm",
            action="store_true",
            help="adds a .esm in every mod")

        p.add_argument(
            "--huge",
            action="store_true",
            help="creates mods with lots of files")

        p.add_argument(
            "count",
            type=int,
            help="number of mods to create")

        p.add_argument(
            "--files",
            type=int,
            default=5,
            help="number of files to create per mod")

        return p

    def run(self, cx):
        cx.clear_directory(cx.mods_directory())

        for i in range(cx.options.count):
            name = "mod-" + str(i + 1)
            m = Mod(name)

            if cx.options.huge:
                self.create_huge(cx, m)
            else:
                for i in range(cx.options.files):
                    self.add_text_file(cx, m, str(i + 1), ".txt")
                    self.add_text_file(cx, m, str(i + 1), ".ini")

                if cx.options.esm:
                    m.add_file(File(name + ".esm", ""))

            m.create(cx)

        return 0

    def create_huge(self, cx, m):
        count = 100000
        txt_count = count
        ini_count = count
        image_count = count
        esp_count = count

        print("txt")
        dir = ""
        for i in range(txt_count):
            if (i % 50) == 0:
                dir = "txt_" + str(i)

            self.add_text_file(cx, m, dir + "/" + str(i + 1), ".txt")

        print("ini")
        dir = ""
        for i in range(ini_count):
            if (i % 50) == 0:
                dir = "ini_" + str(i)

            self.add_text_file(cx, m, dir + "/" + str(i + 1), ".ini")

        print("images")
        image = ""
        with open(cx.res_file("image.png"), "rb") as f:
            image = f.read()

        dir = ""
        for i in range(image_count):
            if (i % 50) == 0:
                dir = "image_" + str(i)

            m.add_file(File(dir + "/" + str(i + 1) + ".png", image))

        print("esp")
        esp = ""
        with open(cx.res_file("dummy.esp"), "rb") as f:
            esp = f.read()

        dir = ""
        for i in range(esp_count):
            if (i % 50) == 0:
                dir = "esp_" + str(i)

            m.add_file(File(dir + "/" + str(i + 1) + ".esp", esp))


    def add_text_file(self, cx, m, name, ext):
        filename = name + ext
        content = m.name() + " " + filename

        m.add_file(File(filename, content))

        if cx.options.duplicate_hidden:
            m.add_file(File(filename + ".mohidden", content))


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


class Overwrite:
    def name(self):
        return "overwrite"

    def create_parser(self, sp):
        p = sp.add_parser(
            self.name(),
            help="creates files in the overwrite directory",
            description="creates files in the overwrite directory")

        return p

    def run(self, cx):
        cx.clear_directory(cx.overwrite_directory())
        File("a.txt", "a").create(cx, cx.overwrite_directory())
        File("b.txt", "b").create(cx, cx.overwrite_directory())
