"""CLI interface to handle SpaceEngine's context.cfg files.

"""


import textx
import argparse

MM = textx.metamodel_from_str(
"""
Model: entries*=Entry;

Entry: type=Type /\s*/ objtype=Class '{' 'Files' '(' /\s*/ files*=File ')' '}';

Type: 'Class' | 'Object';
Class[noskipws]: '"' value=/[^"]+/ '"';
File[noskipws]:  '"' value=Filename '"' /[\s,]*/ ;
Filename:  /([^"]+)/ ;

Comment: /\/\/.*$/;
""")


def parse_context_file(fname:str) -> [(str, str, [str])]:
    "Yield entries found in given file"
    model = MM.model_from_file(fname)
    for entry in model.entries:
        files = tuple(obj.value for obj in entry.files)
        objtype = entry.objtype.value
        yield entry.type, objtype, files

def gen_context_file(entries:[(str, str, [str])]) -> [str]:
    "Yield lines of context file representing given entries"
    for type, objtype, files in entries:
        files_repr = ' '.join('"' + fname + '"' for fname in files)
        yield f'{type}\t"{objtype}"\t{{\tFiles\t( {files_repr} )\t}}'




def parse_cli():
    parser = argparse.ArgumentParser(description=__doc__)

    # subparsers:
    #  - merge: merge multiple existing context file
    #  - create: assist creation of context file   (TODO: how ?)

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_cli()
    print('CLI ARGS:', args)

    entries = parse_context_file('./contexts-files/context.cfg')
    for line in gen_context_file(entries):
        print(line)
