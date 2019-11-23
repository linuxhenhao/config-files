#!/usr/bin/env python3
from multiprocessing import Process
from subprocess import Popen, check_output, check_call
import os
import re
import time
import sys


CHINA_ROUTE = "/usr/share/doc/chinadns/chnroute.txt"
BATCH_TEMPLATE = "/tmp/iproute_batchfile.txt"


def _get_default_route_ip():
    output = check_output("ip route list default", shell=True)
    ip_regex = re.compile(".* via (?P<ip>(\d|\.)+) dev .*")
    result = ip_regex.match(output.decode("utf-8")).groupdict()
    if "ip" in result:
        return result["ip"]
    raise ValueError("default gateway was not found")


def _get_batch_filename() -> str:
    return BATCH_TEMPLATE


def setup_china_routes():
    default_gateway = _get_default_route_ip()
    with open(CHINA_ROUTE) as f:
        routes = [
            line.strip()
            for line in f.readlines() if ":" not in line
        ]
    batch_filename = _get_batch_filename()
    with open(batch_filename, "w") as f:
        for route in routes:
            f.write(f"route add {route} via {default_gateway}\n")
    check_call(f"ip -batch {batch_filename}", shell=True)


def del_china_routes():
    batch_filename = _get_batch_filename()
    with open(batch_filename) as f:
        content = f.read()
    reverted_content = content.replace("add", "del")
    with open(batch_filename, "w") as f:
        f.write(reverted_content)

    check_call(f"ip -batch {batch_filename}", shell=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: sys.argv[0] up/down")
        sys.exit(0)
    if sys.argv[1] == "up":
        setup_china_routes()
    if sys.argv[1] == "down":
        del_china_routes()
