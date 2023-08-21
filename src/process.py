from os import listdir, stat, kill
from typing import Dict
from datetime import datetime
from time import sleep
from typing import Optional, Iterator

SIGSTOP = 19
SIGCONT = 18
SIGKILL = 9
SIGTERM = 15


class Process:
    def __init__(self, pid: int | str):
        self.pid = int(pid)

        self.path = f"/proc/{pid}"

    def __repr__(self) -> str:
        pid = self.pid
        name = self.name

        return f"Process({pid=}, {name=})"

    def _read(self, name: str) -> str:
        with open(f"{self.path}/{name}", "r") as fp:
            return fp.read().strip().strip("\0")

    @property
    def env(self) -> dict:
        env = self._read("environ")

        keys_values = env.split("\0")

        env = {i.split("=")[0]: i.split("=")[1] for i in keys_values}

        return env

    @property
    def cmdline(self) -> list[str]:
        cmdline = self._read("cmdline")

        cmdline = cmdline.split("\0")

        return cmdline

    @property
    def started(self) -> datetime:
        stats = stat(self.path)

        return datetime.utcfromtimestamp(stats.st_ctime)

    @property
    def name(self) -> str:
        cmdline = self.cmdline
        first_arg = cmdline[0].strip("/")
        path = first_arg.split("/")
        name = path[-1]

        if not name:
            comm = self._read("comm")
            name = f"[{comm}]"

        return name

    def suspend(self, resume_after: Optional[int] = None):
        kill(self.pid, SIGSTOP)

        if resume_after:
            sleep(resume_after)
            self.resume()

    def resume(self) -> None:
        kill(self.pid, SIGCONT)

    def kill(self, force: bool = False) -> None:
        kill(self.pid, [SIGTERM, SIGKILL][force])


def get_processes(process_name: Optional[str] = None) -> Iterator[Process]:
    for entry in listdir("/proc"):
        if not entry.isdigit():
            continue
        process = Process(entry)

        if not name:
            yield process

        elif process.name == name:
            yield process


__all__ = [Process, get_processes]
