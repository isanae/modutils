from .mod import Mod, File

class Conflict:
    def name(self):
        return "conflict"

    def create_parser(self, sp):
        p = sp.add_parser(
            self.name(),
            help="creates three mods with conflicting files",
            description="creates three mods with conflicting files")

        return p

    def run(self, cx):
        cx.clear_directory(cx.mods_directory())

        a = Mod("mod-1")
        b = Mod("mod-2")
        c = Mod("mod-3")

        a.add_file(File("1.txt", "mod-1 1"))
        a.add_file(File("1-2.txt", "mod-1 1-2"))
        a.add_file(File("1-2-3.txt", "mod-1 1-2-3"))

        b.add_file(File("2.txt", "mod-2 2"))
        b.add_file(File("1-2.txt", "mod-2 1-2"))
        b.add_file(File("2-3.txt", "mod-2 2-3"))
        b.add_file(File("1-2-3.txt", "mod-2 1-2-3"))

        c.add_file(File("3.txt", "mod-3 3"))
        c.add_file(File("2-3.txt", "mod-3 2-3"))
        c.add_file(File("1-2-3.txt", "mod-3 1-2-3"))

        a.create(cx)
        b.create(cx)
        c.create(cx)

        return 0
