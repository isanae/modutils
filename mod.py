import os
import itertools

MOD_META_CONTENT = """[General]
modid=0
version=
newestVersion=
category=0
installationFile=

[installedFiles]
size=0
"""

# note that in fileTime, } is escaped by making it }} instead
DL_META_CONTENT = r"""[General]
gameName={game_name}
modID={mod_id}
fileID={file_id}
url=
name={name}
description={description}
modName={mod_name}
version={version}
newestVersion={newest_version}
fileTime="@DateTime(\0\0\0\x10\0\0\0\0\0\0%=\x9d\x3\x94}}\xf8\0)"
fileCategory=1
category=83
repository=Nexus
userData=@Variant(\0\0\0\b\0\0\0\0)
installed=false
uninstalled=false
paused=false
removed=false
"""

DL_META_CONTENT_NO_NEXUS = """[General]
installed=true
uninstalled=false"""


class File:
    def __init__(self, name, content):
        self.name_ = name
        self.content_ = content

    def name(self):
        return self.name_

    def content(self):
        return self.content_


class Mod:
    def __init__(self, name):
        self.name_ = name
        self.files_ = []
        self.internal_files_ = []

        self.add_internal_file(File("meta.ini", MOD_META_CONTENT))

    def name(self):
        return self.name_

    def add_file(self, file):
        self.files_.append(file)

    def add_files(self, files):
        for f in files:
            if isinstance(f, str):
                self.add_file(File(f, f))
            else:
                self.add_file(f)

    def add_internal_file(self, f):
        self.internal_files_.append(f)

    def create(self, cx):
        path = os.path.join(cx.mods_directory(), self.name_)
        self.create_files(cx, path)

    def create_files(self, cx, dir):
        for f in itertools.chain(self.internal_files_, self.files_):
            path = os.path.join(dir, f.name())
            parent = os.path.dirname(path)

            cx.create_directory(parent)
            cx.write_file(path, f.content())


class Download:
    def __init__(self, name, nexus_id, file_id, version, ext, meta):
        self.name_ = name
        self.nexus_id_ = nexus_id
        self.file_id_ = file_id
        self.version_ = version
        self.ext_ = ext
        self.meta_ = meta
        self.filename_ = self.make_filename()

    def make_filename(self):
        s = self.name_

        if self.nexus_id_ is not None:
            s += "-" + str(self.nexus_id_)

        s += "-" + self.version_.replace(".", "-")

        return s + "." + self.ext_

    def create(self, cx):
        dl = os.path.join(cx.downloads_directory(), self.filename_)
        meta = os.path.join(cx.downloads_directory(), self.filename_ + ".meta")

        cx.write_file(dl, self.make_archive(cx))

        if self.meta_:
            cx.write_file(meta, self.meta_content())

    def make_archive(self, cx):
        return cx.archive_string("data/textures/" + self.name_ + ".dds", "")

    def meta_content(self):
        if self.nexus_id_ is None:
            return self.meta_content_no_nexus()
        else:
            return self.meta_content_nexus()

    def meta_content_no_nexus(self):
        return DL_META_CONTENT_NO_NEXUS

    def meta_content_nexus(self):
        return DL_META_CONTENT.format(
            game_name="SkyrimSE",
            mod_id=self.nexus_id_,
            file_id=self.file_id_,
            name=self.name_,
            description=self.name_ + " description",
            mod_name=self.name_,
            version=self.version_,
            newest_version=self.version_)
