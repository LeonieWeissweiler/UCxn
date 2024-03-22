# -*- coding: utf-8 -*-
"""
The script is part of the paper
'UCxn: Typologically Informed Annotation of Constructions atop Universal~Dependencies' submitted to LREC-COLING 2024.
It takes the rules of .ucxn.grs file, a custom format of Grew writing rules specified for this project, 
and apply them to UD treebanks following the UCxn Specification v0.1.
"""

import re
import argparse
from pathlib import Path
import logging

from grewpy import Corpus, CorpusDraft
from grewpy import GRSDraft, GRS

def remove_enhanced(grs_draft):
    s = str(grs_draft)
    sub_string = re.sub(r'\-\[(.+?=[^\]]+)]->', r'-[\1, !enhanced]->', s)
    result = re.sub(r'(?<!\])\->', "-[!enhanced]->", sub_string)
    return result

def remove_existing_cxns(corpus):
    grs = """
    package remove_cxns {
        rule remove { % remove existing cxns
            pattern { X[Cxn] }
            commands { del_feat X.Cxn}
        }
    }
    strat main { Onf(remove_cxns) }
    """
    return GRS(grs).apply(corpus)

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
        - Cxn=Resultative#2,Resultative,Interrogative-Indirect -> Interrogative-Indirect,Resultative,Resultative#2
        - CxnElt=10:Int-Indirect#2.Clause,10:Int-Indirect.Clause,10:Int-Indirect#3.Clause,8:Resultative.Event \
        -> 8:Resultative.Event,10:Int-Indirect.Clause,10:Int-Indirect#2.Clause,10:Int-Indirect#3.Clause
    """
    if misc == '_':
        return misc
    else:
        miscs_feats = misc.split('|')
        for i in range(len(miscs_feats)):
            if miscs_feats[i].startswith('Cxn'):
                cxn_feat, cxn_values = miscs_feats[i].split("=")
                splitted_cxn_values = cxn_values.split(',')
                if cxn_feat == "Cxn":
                    splitted_cxn_values.sort()
                else:
                    splitted_cxn_values.sort(key=cxnelt_sort_key)
                cxn_values = ','.join(splitted_cxn_values)
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

def check_first_command(command, rule_name, file):
    node, misc = command.split("=")[0].split(".")
    if node != "_anchor_" or misc != "Cxn":
        logging.error(f"rule {rule_name}: The first command does not define a Cxn on the _anchor_ node; {file}")
        return False
    return True

def check_rule(rule, rule_name, file):
    commands = rule.commands
    res = check_first_command(commands[0], rule_name, file)

    cxn_anchor_count = sum(1 for command in commands if command.split("=")[0].split(".")[1] == "Cxn")
    cxn_elts_count = sum(1 for command in commands if command.split("=")[0].split(".")[1] == "CxnElt")
    
    if cxn_anchor_count > 1:
        logging.error(f"rule {rule_name}: more than one Cxn; {file}")
        res = False
    if cxn_elts_count == 0:
        logging.error(f"rule {rule_name}: no CxnElt were found; {file}")
        res = False
    return res
        
        
if __name__ == "__main__":
    cmd = argparse.ArgumentParser()
    cmd.add_argument("-i", "--input", type=str, required=True, help="a conllu file or a directory of conllu files")
    cmd.add_argument("-o", "--output", type=str, required=True)
    cmd.add_argument("-cxn_grs", "--cxn_grs", type=str, required=True, help="a ucxn.grs format")
    args = cmd.parse_args()

    logging.basicConfig(filename='errors.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

    with open(args.cxn_grs, encoding="utf-8") as f:
        cxn_grs = f.read()

    if Path(args.input).is_dir():
            paths = [p.as_posix() for p in Path(args.input).glob("*.conllu")]
            corpus = remove_existing_cxns(Corpus(paths))
            #GRS.UD2bUD.apply(corpus) #to remove enhanced annotations
    else:
        corpus = remove_existing_cxns(Corpus(args.input))
        #GRS.UD2bUD.apply(corpus)

    print(f"Length: {len(corpus)} phrases")

    draft = CorpusDraft(corpus)
    grs_draft = GRSDraft(remove_enhanced(cxn_grs))

    for package_name, package in grs_draft.items():
        if not isinstance(package, str):
            print(f"Package: {package_name}")
            for e, (rule_name, rule) in enumerate(package.items(), start=1):

                check = check_rule(rule, rule_name, args.cxn_grs)
                if check == False:
                    continue

                print(f"- {e}/{len(package.keys())} rule name: {rule_name}")
                matchings = 0

                for match in corpus.search(rule.request):
                    matchings += 1
                    cxn_commands = list(rule.commands)
                    cxn_name = cxn_commands[0].split("=")[1].replace('"', '')
                    sent_id = match['sent_id']
                    anchor_id = match['matching']['nodes']['_anchor_']
                    
                    if anchor_id == "0":
                        logging.warning(f"Anchor ID is 0; rule {rule_name}; matching {match}; file {args.cxn_grs}")
                        continue

                    if 'Cxn' in draft[sent_id][anchor_id]:
                        cxn_feat = draft[sent_id][anchor_id]['Cxn']
                        if cxn_name in cxn_feat:
                            n_cxns = re.split(r"[,#]",draft[sent_id][anchor_id]['Cxn']).count(cxn_name)
                            new_cxn = f'{cxn_name.split("#")[0]}#{n_cxns+1}'
                        else:
                            new_cxn = f'{cxn_name}'
                        draft[sent_id][anchor_id]['Cxn'] = f"{cxn_feat},{new_cxn}"
                    else:
                        new_cxn = f'{cxn_name}'
                        draft[sent_id][anchor_id]["Cxn"] = new_cxn

                    for command in rule.commands[1:]:
                        node = command.split('=')[0].split('.')[0]
                        node_id = match['matching']['nodes'][node]
                        cxn_elt_name = command.split('=')[1].replace('"', '')
                        new_cxn_elt = f'{anchor_id}:{new_cxn}.{cxn_elt_name}'

                        if node_id == "0":
                            logging.warning(f"CxnElt ID is 0; rule {rule_name}; matching {match}")
                            continue

                        if "CxnElt" in draft[sent_id][node_id]:
                            cxn_elt_feat = draft[sent_id][node_id]['CxnElt']
                            draft[sent_id][node_id]["CxnElt"] = f"{cxn_elt_feat},{new_cxn_elt}"
                        else:
                            draft[sent_id][node_id]["CxnElt"] = new_cxn_elt
                print("-- Machings:", matchings)

    with open(args.output, "w", encoding="utf-8") as f:
        conllu = sort_misc_in_conllu(draft.to_conll())
        f.write(conllu)