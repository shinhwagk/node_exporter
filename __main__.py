import argparse

from node_exporter import run

parser = argparse.ArgumentParser()
parser.add_argument('--port', help="port", type=int)
args = parser.parse_args()

if args.port is None:
    run()
    
run(port=args.port)
