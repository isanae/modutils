import os

class DevBuild:
    def name(self):
        return "devbuild"

    def create_parser(self, sp):
        p = sp.add_parser(
            self.name(),
            help="creates dev builds",
            description="creates two 7z archives in the current directory: " +
                 "Mod.Organizer-NAME.7z from install/bin/* and " +
                 "Mod.Organizer-NAME-pdbs.7z from install/pdbs/*")

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
        install_dir = cx.options.install_dir
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

    def make_filename(self, cx, s=""):
        if not s.startswith("build"):
            s = "build" + s

        s += cx.options.build

        prefix = "Mod.Organizer-2.2.1-"
        suffix = ".7z"

        return prefix + cx.options.name + s + suffix
