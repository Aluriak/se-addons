"""Definition of the music context model,
allowing to read and write the related configuration files.

"""


from dataclasses import dataclass
from textx import metamodel_from_str, get_children_of_type


GRAMMAR_CONFIG = r"""
Model:   contexts*=Context;
Context: iscomment?=CommentMarker type=Type target=Target '{' 'Files' '(' files*=File ')' '}';
Type:    /"?[a-zA-Z]+"?/;
Target:  /"?[a-zA-Z \t0-9\/\\]+"?/;
File:    '"' /[\w \t\[\]\(\)\._\&\'-]+/ '"' ','?;
CommentMarker: /\/\/ ?/;
"""
METAMODEL = metamodel_from_str(GRAMMAR_CONFIG)


@dataclass
class Context:
    "Description of one context declaration"
    objtype:str
    target:str
    files:tuple
    iscomment:bool

    def __str__(self):
        type_, target = self.objtype.strip('"'), self.target.strip('"')
        files = ' '.join(map(lambda x: '"' + x.strip('"').replace('"', r'\"') + '"', self.files))
        comment = '// ' if self.iscomment else ''
        return f'{comment}{type_}\t{target}\t{{\tFiles\t( {files} )\t}}'


@dataclass
class Model:
    "Description of a .cfg file"
    contexts:tuple

    def write(self, outfile:str):
        with open(outfile, 'w') as fd:
            for line in self.gen_str_repr():
                fd.write(line + '\n')

    def gen_str_repr(self):
        yield from map(str, self.contexts)

    @staticmethod
    def from_file(filename:str) -> object:
        "Return a Model instance initialized with given filename containing .cfg data"
        return Model.from_textx_model(METAMODEL.model_from_file(filename))

    @staticmethod
    def from_string(text:str) -> object:
        "Return a Model instance initialized with given string containing .cfg data"
        return Model.from_textx_model(METAMODEL.model_from_string(text))

    @staticmethod
    def from_textx_model(textxmodel) -> object:
        "Return a Model instance initialized with given textx model"
        contexts = []
        for context in textxmodel.contexts:
            type_, target = context.type.strip('"'), context.target.strip('"')
            files = tuple(map(lambda x: x.strip('"'), context.files))
            contexts.append(Context(type_, target, files, context.iscomment))
        return Model(contexts)
