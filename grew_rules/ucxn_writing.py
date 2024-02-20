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
from grewpy import GRS, GRSDraft, Rule, Request
from grewpy.grew import GrewError

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

def count_empty_nodes(draft, sent_id, stop):
    c = 0
    for i in range(1, stop):
        if draft[sent_id][str(i)]['wordform'] == "__EMPTY__":
            c += 1
    return c

def read_treebanks(paths):
    """
    Remove EUD annotations
    """
    treebank = []
    for p in paths:
        with open(p, encoding="utf-8") as in_stream:
            for line in in_stream:
                if line.startswith("#") or line.startswith("\n"):
                    treebank.append(line)
                else:
                    splitted = line.split("\t")
                    if "." in splitted[0]:
                        continue
                    else:
                        splitted[8] = "_"
                        treebank.append("\t".join(splitted))
    return "".join(treebank)
        


if __name__ == "__main__":
    cmd = argparse.ArgumentParser()
    cmd.add_argument("-i", "--input", type=str, required=True, help="a conllu file or a directory of conllu files")
    cmd.add_argument("-o", "--output", type=str, required=True)
    cmd.add_argument("-cxn_grs", "--cxn_grs", type=str, required=True, help="a ucxn.grs format")
    args = cmd.parse_args()

    with open(args.cxn_grs) as f:
        cxn_grs = f.read()

    if Path(args.input).is_dir():
            paths = [p for p in Path(args.input).glob("*.conllu")]
            corpus = Corpus(read_treebanks(paths))
    else:
        corpus = Corpus(read_treebanks([args.input]))

    print(args.input.split("/")[-1])

    draft = CorpusDraft(corpus)
    grs_draft = GRSDraft(cxn_grs)

    for package, rules in grs_draft.items():
        if package != "main": #TODO: need to be generalize
            print(f"Package: {package}")
            for e, (rule_name, rule) in enumerate(rules.items(), start=1):
                print(f"- {e}/{len(rules.keys())} rule name: {rule_name}")
                matching_sentences = set(m['sent_id'] for m in corpus.search(rule.request))
                for sent_id in matching_sentences:
                    basic_rule = deepcopy(rule)
                    basic_rule.request.append('global',f'sent_id="{sent_id}"')
                    cxn_commands = list(basic_rule.commands)
                    cxn_name = cxn_commands[0].split("=")[1].replace('"', '')
                    print(basic_rule)
                    for i, match in enumerate(corpus.search(basic_rule.request)):
                        print()
                        # if rule_name == "Existential-HavePred-ItExpl-ThereExpl":
                        #     for m in corpus.search(basic_rule.request):
                        #         print(m)
                        #     print("---")

                        anchor_id = match['matching']['nodes']['_anchor_']

                        if 'Cxn' in draft[sent_id][anchor_id]:
                            cxn_feat = draft[sent_id][anchor_id]['Cxn']
                            if cxn_name in cxn_feat:
                                n_cxns = re.split(r"[;#]",draft[sent_id][anchor_id]['Cxn']).count(cxn_name)
                                new_cxn = f'{cxn_name.split("#")[0]}#{n_cxns+1}'
                            else:
                                new_cxn = f'{cxn_name}#1'
                            draft[sent_id][anchor_id]['Cxn'] = f"{cxn_feat};{new_cxn}"
                        else:
                            new_cxn = f'{cxn_name}#1'
                            draft[sent_id][anchor_id]["Cxn"] = new_cxn

                        for command in rule.commands[1:]:
                            node = command.split('=')[0].split('.')[0]
                            node_id = match['matching']['nodes'][node]
                            cxn_elt_name = command.split('=')[1].replace('"', '')
                            new_cxn_elt = f'{anchor_id}:{new_cxn}.{cxn_elt_name}'

                            if "CxnElt" in draft[sent_id][node_id]:
                                cxn_elt_feat = draft[sent_id][node_id]['CxnElt']
                                draft[sent_id][node_id]["CxnElt"] = f"{cxn_elt_feat};{new_cxn_elt}"
                            else:
                                draft[sent_id][node_id]["CxnElt"] = new_cxn_elt

    with open(args.output, "w", encoding="utf-8") as f:
        conllu = sort_misc_in_conllu(draft.to_conll())
        f.write(conllu)