import argparse
import secrets


def make_argv():
    return ["--key=" + secrets.token_urlsafe(48)]


def parse(argv):
    p = argparse.ArgumentParser(exit_on_error=False)
    p.add_argument("--key", required=True)
    return p.parse_args(argv)
