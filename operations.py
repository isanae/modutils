import os
import subprocess
import abc
import time
import shutil

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

    def archive(self, input, output):
        self.run_process([SEVENZ, "a", output, "-r", "-mx=5", input])

    def archive_string(self, path, content):
        return self.popen([SEVENZ, "a", "d.zip", "-si" + path, "-so"], content)

    @abc.abstractmethod
    def run_process(self, input, output):
        pass

    @abc.abstractmethod
    def popen(self, args):
        pass


class DryOperations(OperationsImpl):
    def clear_directory(self, path):
        for f in os.listdir(path):
            fp = os.path.join(path, f)

            if os.path.isfile(fp):
                print("  . file " + fp)
            else:
                print("  . dir   " + fp)

    def create_directory(self, path):
        pass

    def write_file(self, path, content):
        pass

    def run_process(self, args):
        print("would run: " + " ".join(args))
        pass

    def popen(self, args, send):
        print("would run: " + " ".join(args))
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

    def run_process(self, args):
        subprocess.run(args)

    def popen(self, args, send):
        p = subprocess.Popen(
            args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        out, err = p.communicate(send)
        if err is not None:
            print(err)

        return out
