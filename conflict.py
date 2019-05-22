from .mod import Mod, File

class Conflict:
    def name(self):
        return "conflict"

    def create_parser(self, sp):
        p = sp.add_parser(
            self.name(),
            help="creates three mods with conflicting files",
            description="Creates three mods: the first with files named 1 to N, the" +
                 "second with files named 1 to N*3 and a third with files named " +
                 "N*2 to N*3. All files from the first mods will be overwritten " +
                 "by the second mod, all files from the third mod will overwrite " +
                 "files from the second mod, and the second mod will have N " +
                 "files not overwritten by anything")

        p.add_argument(
            "file_count",
            type=int,
            help="number of conflicting files")

        return p

    def run(self, cx):
        count = cx.options.file_count

        cx.clear_directory(cx.mods_directory())

        a = Mod("mod-1")
        for i in range(count):
            filename = str(i + 1)
            content = a.name() + " " + filename
            a.add_file(File(filename, content))

        b = Mod("mod-2")
        for i in range(count * 3):
            filename = str(i + 1)
            content = a.name() + " " + filename
            b.add_file(File(filename, content))

        c = Mod("mod-3")
        for i in range(count):
            filename = str(count*2 + (i + 1))
            content = a.name() + " " + filename
            c.add_file(File(filename, content))

        a.create(cx)
        b.create(cx)
        c.create(cx)

        return 0
