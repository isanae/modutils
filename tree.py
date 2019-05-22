from .mod import Mod, File

class Tree:
    def name(self):
        return "tree"

    def create_parser(self, sp):
        p = sp.add_parser(
            self.name(),
            help="creates one mod with a varied file tree",
            description="creates one mod with a varied file tree")

        return p

    def run(self, cx):
        cx.clear_directory(cx.mods_directory())

        m = Mod("mod")

        m.add_files(["1", "2", "3"])
        m.add_files(["a/1", "a/2", "a/3"])
        m.add_files(["a/aa/1", "a/aa/2", "a/aa/3"])
        m.add_files(["b/1", "b/2", "b/3"])
        m.add_files(["b/bb/1", "b/bb/2", "b/bb/3"])

        m.create(cx)

        return 0
