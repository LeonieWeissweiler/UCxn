# UCxn: Typologically Informed Annotation of Constructions Atop Universal Dependencies

Repository for the ongoing UCxn Project to add construction information to Universal Dependencies, and code and dataset for [Typologically Informed Annotation of Constructions Atop Universal Dependencies](https://arxiv.org/abs/2403.17748)

Full technical specifications for Version 1, as described in the paper, are in the `docs` folder. Grew-match queries matching the paper are found in the `grew_rules` folder, and the matching annotated corpora in `annotated_corpora`. To try out the rules and see a visual representation, go to the [https://match.grew.fr/](grew-match website).

## Example Annotation
ID | FORM | LEMMA | UPOS | ... | UCxn
--- |--- |--- |--- |--- |--- |
| 1 | You | you | PRON | ... | _
| 2 | have | have | VERB | ... | Cxn=Interrogative-Polar-Direct
| 3 | a | a | DET | ... | _
| 4 | pencil | pencil | NOUN | ... | _
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
@misc{weissweiler2024ucxn,
      title={UCxn: Typologically Informed Annotation of Constructions Atop Universal Dependencies}, 
      author={Leonie Weissweiler and Nina B\"{o}bel and Kirian Guiller and Santiago Herrera and Wesley Scivetti and Arthur Lorenzi and Nurit Melnik and Archna Bhatia and Hinrich Sch\"{u}tze and Lori Levin and Amir Zeldes and Joakim Nivre and William Croft and Nathan Schneider},
      year={2024},
      eprint={2403.17748},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
