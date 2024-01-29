# -*- coding: utf-8 -*-
"""
The script is part of the paper
'Typologically-Informed Annotation of Constructions atop Universal~Dependencies'submitted to LREC-COLING 2024.
It takes the rules of .ucxn.grs file, a custom format of Grew writing rules specified for this project, 
and apply them to UD treebanks following the UCxn Specification v0.1.
"""

import re
import argparse
from copy import deepcopy
from pathlib import Path

from grewpy import Corpus, CorpusDraft
from grewpy import GRS, GRSDraft


def cxnelt_sort_key(misc_values):
    """
    Custom sort key for the CxnElts
    """
    values = misc_values.split(':')

    # Digit part into an integer for sorting
    head_id = int(values[0])

    # Further split the rest of the string by '#' if it exists
    subvalues = values[1].split('#')
    if len(subvalues) > 1:
        cxn_id = int(subvalues[1].split('.')[0]) if subvalues[1][0].isdigit() else float('inf')
        return (head_id, 1, cxn_id, subvalues[1])
    else:
        # If '#' is not present, use a default low value (-1) to ensure these come first
        return (head_id, 0, -1, subvalues[0])


def sort_cxns_in_misc(misc: str) -> str:
    """
    Take a misc string and order the Cxn and CxnElt misc feats:
        - Cxn=Resultative#2;Resultative;Interrogative-Indirect -> Interrogative-Indirect;Resultative;Resultative#2
        - CxnElt=10:Int-Indirect#2.Clause;10:Int-Indirect.Clause;10:Int-Indirect#3.Clause;8:Resultative.Event \
        -> 8:Resultative.Event;10:Int-Indirect.Clause;10:Int-Indirect#2.Clause;10:Int-Indirect#3.Clause
    """
    if misc == '_':
        return misc
    else:
        miscs_feats = misc.split('|')
        for i in range(len(miscs_feats)):
            if miscs_feats[i].startswith('Cxn'):
                cxn_feat, cxn_values = miscs_feats[i].split("=")
                splitted_cxn_values = cxn_values.split(';')
                if cxn_feat == "Cxn":
                    splitted_cxn_values.sort()
                else:
                    splitted_cxn_values.sort(key=cxnelt_sort_key)
                cxn_values = ';'.join(splitted_cxn_values)
                miscs_feats[i] = f"{cxn_feat}={cxn_values}"
        misc = '|'.join(miscs_feats)
        return misc
    

def sort_misc_in_conllu(input_conllu_text: str) -> str:
    """
    Sort misc in conllu file.
    """
    output_lines = []
    for line in input_conllu_text.split('\n'):
        if line == '':
            output_lines.append('')
        elif line.startswith('#'):
            output_lines.append(line)
        elif line[0].isdigit():
            splitted = line.split('\t')
            misc = splitted[9]
            ordered_misc = sort_cxns_in_misc(misc)
            splitted[9] = ordered_misc
            line = '\t'.join(splitted)
            output_lines.append(line)
    return '\n'.join(output_lines)


if __name__ == "__main__":
    cmd = argparse.ArgumentParser()
    cmd.add_argument("-i", "--input", type=str, required=True, help="a conllu file or a directory of conllu files")
    cmd.add_argument("-o", "--output", type=str, required=True)
    cmd.add_argument("-cxn_grs", "--cxn_grs", type=str, required=True, help="a ucxn.grs format")
    args = cmd.parse_args()

    # Avoid enhanced edges
    with open(args.cxn_grs) as f:
        cxn_grs = re.sub(r"(?<!\])->", "-[!enhanced]->", f.read())

    if Path(args.input).is_dir():
        corpus = Corpus([p.as_posix() for p in Path(args.input).glob("*.conllu")])
    else:
        corpus = Corpus(args.input)

    draft = CorpusDraft(corpus)
    grs_draft = GRSDraft(cxn_grs)

    for package, rules in grs_draft.items():
        if package != "main":
            for rule_name, rule in rules.items():
                matching_sentences = set(m['sent_id'] for m in corpus.search(rule.request))
                for sent_id in matching_sentences:
                    cxn_rule = deepcopy(rule)    
                    cxn_rule.request.append('global',f'sent_id={sent_id}')
                    cxn_commands = list(cxn_rule.commands)
                    cxn_name = cxn_commands[0].split("=")[1].replace('"', '')

                    for i, match in enumerate(corpus.search(cxn_rule.request)):
                        cxn_rule = deepcopy(rule)
                        anchor_id = match['matching']['nodes']['_anchor_']
                        # Build Cxn label and safe commands
                        if 'Cxn' in draft[sent_id][anchor_id]:
                            if cxn_name in draft[sent_id][anchor_id]['Cxn']:
                                n_cxns = re.split(r"[;#]",draft[sent_id][anchor_id]['Cxn']).count(cxn_name)
                                cxn_value = f'{cxn_name}#{n_cxns+1}'
                            else:
                                cxn_value = cxn_name

                            cxn_rule.request.append('without',f'_anchor_[Cxn=re".*{cxn_value}.*"]')
                            cxn_rule.commands[0] = f'_anchor_.Cxn=_anchor_.Cxn + ";" + "{cxn_value}"'

                        else:
                            cxn_value = cxn_name
                            cxn_rule.request.append('without',f'_anchor_[Cxn]')

                        #CxnElts
                        for j, command in enumerate(rule.commands[1:], start=1):
                            node = command.split('=')[0].split('.')[0]
                            node_id = match['matching']['nodes'][node]
                            cxn_elt_name = command.split('=')[1].replace('"', '')
                            cxn_elt_value = f'{anchor_id}:{cxn_value}.{cxn_elt_name}'

                            # CxnElt safe command
                            cxn_rule.request.append('without',f'{node}[CxnElt=re".*{cxn_elt_value}.*"]')

                            if "CxnElt" in draft[sent_id][node_id]:
                                cxn_rule.commands[j] = f'{node}.CxnElt= {node}.CxnElt + ";" + "{cxn_elt_value}"'
                            else:
                                cxn_rule.commands[j] = f'{node}.CxnElt="{cxn_elt_value}"'

                        # Graph transformation
                        cxn_grs = GRS(GRSDraft({"cxn": cxn_rule, "main": "cxn"}))
                        transformed_graphs = cxn_grs.run(draft[sent_id])
                        
                        if transformed_graphs:
                            if len(transformed_graphs) > 1:
                                # Handle several matchings with the same anchor
                                draft[sent_id] = transformed_graphs[i]
                            else:
                                draft[sent_id] = transformed_graphs.pop()

    with open(args.output, "w", encoding="utf-8") as f:
        conllu = sort_misc_in_conllu(draft.to_conll())
        f.write(conllu)