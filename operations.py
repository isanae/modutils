import os
import subprocess
import abc
import time
import shutil
import tempfile
from .log import *

SEVENZ = r"C:\Program Files\7-Zip\7z.exe"

class OperationsImpl(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def clear_directory(self, path):
        pass

    @abc.abstractmethod
    def create_directory(self, path):
        pass

    @abc.abstractmethod
    def write_file(self, path, content):
        pass

    @abc.abstractmethod
    def delete_file(self, path):
        pass

    @abc.abstractmethod
    def temp_file(self):
        pass

    def archive(self, input, output, exclude=[]):
        if os.path.exists(output):
            raise Exception("file {} already exists".format(output))

        args = [SEVENZ, "a", output, "-r", "-mx=5", input]
        for e in exclude:
            args.append("-xr!" + e)

        self.run_process(args, None)

    def archive_string(self, path, content):
        # filename doesn't matter because the archive is dumped in stdout, but
        # the extension dictates the compression type
        return self.popen([SEVENZ, "a", "d.zip", "-si" + path, "-so"], content)

    def archive_files(self, listfile, output, cwd):
        if os.path.exists(output):
            raise Exception("file {} already exists".format(output))

        self.run_process([SEVENZ, "a", output, "@" + listfile], cwd)

    @abc.abstractmethod
    def run_process(self, input, output, cwd):
        pass

    @abc.abstractmethod
    def popen(self, args):
        pass


class DryOperations(OperationsImpl):
    def clear_directory(self, path):
        for f in os.listdir(path):
            fp = os.path.join(path, f)

            if os.path.isfile(fp):
                log_op("  . file {}", fp)
            else:
                log_op("  . dir  {}",fp)

    def create_directory(self, path):
        pass

    def write_file(self, path, content):
        pass

    def delete_file(self, path):
        pass

    def temp_file(self):
        return "tempfile"

    def run_process(self, args, cwd):
        if cwd is None:
            log_op("would run: \"{}\"", " ".join(args))
        else:
            log_op("would run: \"{}\" with cwd={}", " ".join(args), cwd)

    def popen(self, args, send):
        log_op("would run: \"{}\"", " ".join(args))
        return ""


class RealOperations(OperationsImpl):
    def clear_directory(self, path):
        for f in os.listdir(path):
            fp = os.path.join(path, f)

            if os.path.isfile(fp):
                os.unlink(fp)
            else:
                shutil.rmtree(fp)

        time.sleep(0.3)

    def create_directory(self, path):
        os.makedirs(path, exist_ok=True)

    def write_file(self, path, content):
        mode = "w"
        if isinstance(content, bytes):
            mode += "b"

        with open(path, mode) as f:
            f.write(content)

    def delete_file(self, path):
        os.remove(path)

    def temp_file(self):
        f = tempfile.mkstemp()
        os.close(f[0])
        return f[1]

    def run_process(self, args, cwd):
        subprocess.run(args, cwd=cwd)

    def popen(self, args, send):
        p = subprocess.Popen(
            args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        out, err = p.communicate(send)
        if err is not None:
            error(err)

        return out
