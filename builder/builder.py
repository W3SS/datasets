import argparse
import yaml
import glob
from pprint import pprint

# Builder specific
from compile import Compiler
from auxiliary import to_dict
from build import build_dir
from languages.build_python import build_python
from languages.build_csv import build_csv

try:
    import progressbar
except ImportError:
    progressbar = None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="The main Builder tool")

    parser.add_argument('spec', help='Location of a spec file (or source directory with -a).')
    parser.add_argument('-l', '--language', help='The desired output language bindings. If not present, defaults to all known languages.')
    parser.add_argument('-v', '--validate', help='Only validates the spec, skips compilation.', action='store_true')
    parser.add_argument('-f', '--fast', help='Only builds the supporting files, skips database building.', action='store_true')
    parser.add_argument('-a', '--all', help='Builds all the .corgis files in the source directory.', action='store_true')
    parser.add_argument('target', help="Build output location.")

    args = parser.parse_args()
    
    if args.all:
        args.spec = glob.glob(args.spec+'*.corgis')
    else:
        args.spec = [args.spec]
    
    if len(args.spec) > 1 and progressbar is not None:
        pbar = progressbar.ProgressBar(widgets=[progressbar.ReverseBar('<'),
           ' ', progressbar.Percentage(), ' ', progressbar.ETA()]).start()
    else:
        pbar = list
    for a_spec in pbar(args.spec):
        print a_spec
        with open(a_spec, 'r') as specification_file:
            specification = yaml.load(specification_file)
            #pprint(specification)
            compiled, warnings, errors = Compiler(a_spec, specification).run()
            #print("*"*10)
            if warnings: print "\tWarnings!"
            for warning in warnings:
                print "\t\t", warning
            if errors: print "\tErrors!"
            for error in errors:
                print "\t\t", error
            #print("*"*10)
            #pprint(to_dict(compiled))
            if args.language.lower() == "python":
                files, moves = build_python(to_dict(compiled), args.fast)
                build_data, build_errors = build_dir(files, moves, args.target)
            elif args.language.lower() == "csv":
                files, moves = build_csv(to_dict(compiled))
                build_data, build_errors = build_dir(files, moves, args.target)