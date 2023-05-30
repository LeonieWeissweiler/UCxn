# DepEdit for CxG annotation

Rule cascades for adding construction annotations to UD treebank files (.conllu)

## Running the latest scripts

To run all rules and refresh .conllu files with the latest annotations for a language such as English ('en') run:

`> python run_cxn.py --lang en`

Or choose a different language code, or 'all' to run all available languages.

## Getting started for a new language or new rules

To add a new language these are the recommended steps:

  1. Find a good UD treebank in the target language. If multiple treebanks are available for a language, consider factors such as size, quality of the annotation, and likelihood that target constructions will appear (for example: question constructions are rare in news language; informal constructions are more common in spoken data; etc.)
  2. Search for the construction you are targeting using https://universal.grew.fr/. 
    * The interface covers the latest UD corpus releases, and features some example queries on the right to get you started. 
    * When formulating the initial query, try to use simple lexical items which will catch many instances of the constructions (focus on recall, not precision)
    * For example, for English Comparative Correlatives, we can search for the sequence "the more" like this: `pattern { N1 [lemma="the"]; N2 [lemma="more"]; N1 < N2 }`
  3. After finding some examples, look at the graphs for several correct and incorrect results (for example "the more the merrier" is correct, but "the more recent past" is incorrect)
    * Try to figure out what parts of the graph guarantee a correct result
    * It's OK to use many queries to capture different variants of the construction - the most imortant thing is to gradually improve the precision (ruling out false positives), and use multiple queries to improve recall
  4. Once you have figured out the properties of graphs instantiating your construction, add the treebank files to the repo
    * Make a folder in data/ named after the corpus identifier, for example `en_gum/`
    * Copy the current .conllu release files of the corpus from GitHub to the folder (for example from https://github.com/UniversalDependencies/UD_English-GUM/)
  5. Make a script file under `rules/` using the language code as a prefix, for example `en_cxn.ini`.
    * Rules consist of lines with three tab separated columns: a declaration of nodes to find, the relations between the nodes (precedence, dominance, etc.) and what to do to the nodes (for example add a `Cxn=` annotation in the MISC column
    * You can use the existing rule files as examples to get started
    * It is recommended to read the documentation on writing DepEdit rule files at https://gucorpling.org/depedit/
  6. Make sure python and depedit are installed and run: `> python run_cxn.py --lang en`


## Worked rule examples

### Exclamative-What

```
lemma=/what/;lemma=/a/;upos=/NOUN|PROPN/	#3>#2;#3>#1;#1.#2	#3:misc+=Cxn=Exclamative-What
```

This rule finds phrases like 'what a day!' and declares a sequence of three nodes in the first column, separated by semi-colon:

  1. The first has the lemma 'what'
  2. The second has the lemma 'a'
  3. The third has the universal pos tag NOUN or PROPN, expressed using a regular expression disjunction with `|`

The second column defines relations between these nodes:

  * `#3` dominates `#2` and also `#1` as their dependency parent (`#3>#2;#3>#1`)
  * `#1` immediately precedes `#2` (`#1.#2`)

The third column adds a misc annotation, `Cxn=Exclamative-What`

### N-P-N

This pair of rules finds noun-preposition-noun constructions, where the nouns are bare (no article) and have an identical lemma (e.g. 'house by house'):

```
# N-P-N
xpos=/N.*/;func=/det/	#1>#2	#1:storage=has_det
xpos=/N.*/&storage!=/has_det/;func=/case/;xpos=/N.*/&storage!=/has_det/	#1.1,2#2.1,2#3;#1>#3>#2;#1:lemma==#3	#1:misc+=Cxn=Noun-Prep-Noun
```

The first rule looks for nouns (xpos N.*) and determiners (function det). For all nouns with determiners, it uses the hidden `storage` annotation to store the value `has_det`. This allows us to later rule out nouns with determiners.

The second rule looks for three nodes:
  1. a noun which does *NOT* have a determiner (based on rule 1, storage!=/has_det/)
  2. a token with the function 'case'
  3. a second noun without a determiner
  
The relations of the second rule state that:

1. `#1` is within 2 tokens of `#2` (the operator .1,2 - precedence between 1 -- 2 tokens)
2. Similarly `#2` and `#3` are within 2 tokens
3. The dominance chain applies to the dependency chain: `#1>#3>#2`
4. The lemma of `#1` is the same as `#3` (`#1:lemma==#3`)

Finally, in the third column the Cxn annotation is added:

`#1:misc+=Cxn=Noun-Prep-Noun`

## Running a standalone script

You can also run depedit scripts independently to test them. To apply a cascade of rules from a file like `lang_cxn.ini` to a .conllu file with UD annotations using Python:

```
pip install depedit
python -m depedit -c lang_cxn.ini infile.conllu
```

