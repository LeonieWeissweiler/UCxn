import os, sys, re
from argparse import ArgumentParser
from glob import glob
from depedit import DepEdit

conll_files = glob("data" + os.sep + "**" + os.sep + "*.conllu",recursive=True)

rule_files = glob("rules" + os.sep + "*_cxn.ini")

depedits = {}


def main(lang="en"):
    """
    Run depedit rules on all .conllu files under data/ matching the chosen language

    :param lang: language code to process files for, e.g. 'en', or 'all' for all languages
    """

    for file_ in rule_files:
        file_lang = os.path.basename(file_).split("_")[0].lower()
        if file_lang == lang or lang.lower() == "all":
            sys.stderr.write("o Reading rules for language: " + lang)
            depedits[file_lang] = DepEdit(config_file=file_)
            rule_count = len(depedits[file_lang].transformations)
            sys.stderr.write(" (" + str(rule_count) + " rules)\n")

    for file_ in conll_files:
        conllu = open(file_).read()
        docname = os.path.basename(file_)
        if "_" in docname:
            doc_lang = docname.split("_")[0].lower()
            if doc_lang == lang or lang == 'all':
                if doc_lang in depedits:
                    sys.stderr.write("o Annotating file: " + docname + "\n")
                    conllu = depedits[doc_lang].run_depedit(conllu)
                    with open(file_,'w',encoding="utf8",newline="\n") as f:  # Overwrite file with updated version
                        f.write(conllu)
                    continue
            else:
                continue
        sys.stderr.write("! No rules file found for language of file: " + file_ + "\n")


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("-l","--lang",default="en",help="Language code (or 'all')")

    opts = p.parse_args()

    main(lang=opts.lang)
