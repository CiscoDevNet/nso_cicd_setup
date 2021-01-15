from pyats.easypy import run
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--targets', help='YAML file specifying ping targets')

def main(runtime, **kwargs):
     args, sys.argv[1:] = parser.parse_known_args(sys.argv[1:])
     run(testscript = 'pyats_pingtest.py', runtime = runtime, targets=args.targets)