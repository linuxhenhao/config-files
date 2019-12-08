#!/usr/bin/env python3
from subprocess import check_output, check_call
import re
import sys
import socket
import argparse


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


def _get_endpoint_ip(endpoint_host: str) -> str:
    return socket.gethostbyname(endpoint_host)


def setup_default_gateway_for_endpoint(default_gateway, endpoint_host):
    end_point_ip = _get_endpoint_ip(endpoint_host)
    check_call(f"ip route add {end_point_ip} via {default_gateway}", shell=True)
    

def setup_china_routes(china_route_path: str):
    default_gateway = _get_default_route_ip()
    with open(china_route_path) as f:
        routes = [
            line.strip()
            for line in f.readlines() if ":" not in line
        ]
    batch_filename = _get_batch_filename()
    with open(batch_filename, "w") as f:
        for route in routes:
            f.write(f"route add {route} via {default_gateway}\n")
    check_call(f"ip -batch {batch_filename}", shell=True)


def setup(endpoint_host: str, china_route_path: str):
    default_gateway = _get_default_route_ip()
    setup_default_gateway_for_endpoint(
        default_gateway=default_gateway,
        endpoint_host=endpoint_host
    )
    setup_china_routes(china_route_path)


def del_default_gateway_for_endpoint(endpoint_host: str):
    end_point_ip = _get_endpoint_ip(endpoint_host=endpoint_host)
    check_call(f"ip route del {end_point_ip}", shell=True)


def del_china_routes():
    batch_filename = _get_batch_filename()
    with open(batch_filename) as f:
        content = f.read()
    reverted_content = content.replace("add", "del")
    with open(batch_filename, "w") as f:
        f.write(reverted_content)

    check_call(f"ip -batch {batch_filename}", shell=True)


def delete(config_path: str):
    del_default_gateway_for_endpoint(config_path)
    del_china_routes()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e", "--endpoint-host", required=True,
        help="hostname/ip for real endpoint"
    )
    parser.add_argument(
        "-u", "--up", required=False,
        action="store_true",
        help="setup phase, always in wg config's post_up option"
    )
    parser.add_argument(
        "-d", "--down", required=False,
        action="store_true",
        help="deleting phase, always in wg config's pre_del option"
    )
    parser.add_argument(
        "-r", "--route-file", required=False,
        default=CHINA_ROUTE,
        help="path of china route file",
    )
    return parser


if __name__ == "__main__":
    parser = build_arg_parser()
    args = parser.parse_args()
    if not (args.down ^ args.up):
        # both up and down are the same
        parser.print_help()
        sys.exit(0)
    if args.up:
        setup(endpoint_host=args.endpoint_host, china_route_path=args.route_file)
    if args.down:
        delete(args.endpoint_host)
