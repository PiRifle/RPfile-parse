from rpfile_parse import RPFileParser
from utils import parse_arguments
import argparse
import rich

rp_file = RPFileParser("./")

OPTIONS = {"server": rp_file.args.get("SERVER", "http://server.pingus/")}

def _deploy(_from, _to):
    pass

def _copy(_from, _to):
    pass

def _unpack(_from, _to):
    pass

def _pull(_from, _to):
    pass
def _ignore(*args):
    print(f"IGNORING {', '.join(args)}")

INSTRUCTIONS = {
    "DEPLOY": _deploy,
    "COPY": _copy,
    "PULL": _pull,
    "UNPACK": _unpack
}

for step in rp_file.structure:
    INSTRUCTIONS.get(step["instruction"], _ignore)(*parse_arguments(step["value"]))

    # print(parser.parse_args())

# print(rp_file.args)
