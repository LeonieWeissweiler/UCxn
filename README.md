# UCxn: Typologically Informed Annotation of Constructions Atop Universal Dependencies

Repository for the ongoing UCxn Project to add construction information to [Universal Dependencies](https://universaldependencies.org/) (UD), and code and dataset for "**[UCxn: Typologically Informed Annotation of Constructions Atop Universal Dependencies](https://arxiv.org/abs/2403.17748)**" (Weissweiler et al., LREC-COLING 2024).
It presents an approach to annotating constructions as a layer on top of UD ("UCxn"), with case studies exploring 5 typologically defined construction families in 10 languages, and Grew rules to automatically infer the construction annotations.

This paper can be found in the `docs` folder, alongside a full technical specification for the annotation scheme and construction subtypes in Version 1.

[Grew](https://grew.fr/) queries described by the paper are found in the `grew_rules` folder, and the automatically annotated corpora in `annotated_corpora`. In addition, annotations can be explored in [Grew-match](https://match.grew.fr/), e.g. [the UCxn-enhanced English-GUM corpus](https://universal.grew.fr/?corpus=UD_English-GUM@ucxn).

The UD 2.13 release served as the input for producing the rule-based annotations in `annotated_corpora`. (English-GUM contained some pilot construction annotations in the 2.13 release; those were removed before applying the Grew rules.) Individual treebanks are encouraged to incorporate UCxn annotations, ideally with manual checking, into official UD treebank repositories for future releases.

## Example Annotation
ID | FORM | LEMMA | UPOS | ... | UCxn
--- |--- |--- |--- |--- |--- |
| 1 | what | what | PRON | ... | CxnElt=2:Interrogative-WHInfo-Direct.WHWord
| 2 | happened | happen | VERB | ... | Cxn=Interrogative-WHInfo-Direct\|CxnElt=2:Interrogative-WHInfo-Direct.Clause
| 3 | to | to | ADP | ... | _
| 4 | you | you | PRON | ... | _
| 5 | ? | ? | PUNCT | ... | _

## Annotated Data Statistics

![image](https://github.com/LeonieWeissweiler/UCxn/assets/30300891/43084fc0-b648-4918-bc05-79639013edd0)

## Languages

- English
- German
- Swedish
- French
- Spanish
- Portuguese
- Hindi
- Mandarin
- Hebrew
- Coptic

## Constructions

- Interrogative
- Existential
- Conditional
- Resultative
- NPN

## Citation

If you use the dataset or code, please cite our paper:

```
@inproceedings{weissweiler-etal-2024-ucxn,
    title = "{UC}xn: Typologically Informed Annotation of Constructions Atop {U}niversal {D}ependencies",
    author = {Weissweiler, Leonie  and B{\"o}bel, Nina  and Guiller, Kirian  and Herrera, Santiago  and Scivetti, Wesley  and Lorenzi, Arthur  and Melnik, Nurit  and Bhatia, Archna  and Sch{\"u}tze, Hinrich  and Levin, Lori  and Zeldes, Amir  and Nivre, Joakim  and Croft, William  and Schneider, Nathan},
    editor = "Calzolari, Nicoletta  and Kan, Min-Yen  and Hoste, Veronique  and Lenci, Alessandro  and Sakti, Sakriani  and Xue, Nianwen",
    booktitle = "Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)",
    month = may,
    year = "2024",
    address = "Torino, Italia",
    publisher = "ELRA and ICCL",
    url = "https://aclanthology.org/2024.lrec-main.1471",
    pages = "16919--16932",
}

```
