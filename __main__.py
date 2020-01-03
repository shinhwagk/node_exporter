import argparse

from node_exporter import run

parser = argparse.ArgumentParser()
parser.add_argument('--port', help="port", type=int)
args = parser.parse_args()

run(port=args.port)
