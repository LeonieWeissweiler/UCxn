# UCxn: Construction Annotation in UD

This document summarizes the technical implementation of a project known as UCxn, which consists of construction annotations as a layer of treebank annotation atop Universal Dependencies (UD, specifically UDv2). The effort is detailed in Weissweiler et al. (LREC-COLING 2024), which examines 5 construction families across 10 languages.

For the selected constructions, morphosyntactic rules have been written and applied to treebanks in these 10 languages. Here we describe the data format and naming conventions in the resulting data. 

## Overview

To illustrate briefly the sort of construction we annotate in the data, consider existentials:

	There is no answer [English]
	Il n’ y a pas de reponse [French]

The English construction uses an expletive ‘there’ and a copula alongside the Pivot, the underlined phrase expressing a content element whose existence is being affirmed or denied. French uses two expletives as well as a form of the verb meaning ‘have’.

UCxn annotates sentences like these by marking that a construction is present and also marking its construction elements, the components that are realized by individual words/phrases. The annotated construction elements have semantic names, e.g. Pivot, which can be qualified with the construction name: e.g. Existential.Pivot. Here we are assuming for purposes of illustration a simple construction name, “Existential”, which is defined based on meaning in a way that generalizes across languages. Construction name subtyping is also possible, with hyphen-separated parts of increasing specificity. Some of the parts can reflect strategies that differentiate how languages realize the meaning morphosyntactically. 

Finally, a word about tokens vs. types: In principle, a Constructicon (lexicon-of-constructions) would define the meaning-bearing grammatical types of the language. UCxn takes inspiration from Constructicon resources that have been developed for several languages. However, UCxn is merely a standard for annotating instances. That is, UCxn itself does not propose a formal notation for construction type definitions; it merely assumes the list of construction types, their elements, and associated type-level properties (such as the range of kinds of phrases that can fill a given element, optionality of elements, agreement constraints, etc.) are known to the annotator. 

## Format Specification

The UCxn layer is currently implemented in the CoNLL-U format—the standard for UD treebanks—within the final (MISC) column, which supports arbitrary key-value pairs. For each construction instance, or construct, UCxn supports annotation in two fields: 
- the **Cxn** field for the name of the construction and specification of its elements—once per construct
- the **CxnElt** field for each construct element to be listed separately, anchored on a node representing that element.

An example sentence illustrating resultative and interrogative constructions (with simplified names), showing annotation lines for all words/UD nodes (underscore = “no UCxn annotation on this node”):

	Who let the dogs out ?
	1	Who	…	2	nsubj	…	CxnElt=2:Interrogative.WHWord
	2	let	…	0	root	…	Cxn=Interrogative,Resultative|CxnElt=2:Interrogative.Clause,2:Resultative.Event
	3	the	…	4	det	…	_
	4	dogs	…	2	obj	…	_
	5	out	…	2	xcomp	…	CxnElt=2:Resultative.ResultState
	6	?	…	2	punct	…	_

### Construction Name

A construction (or construction element) name is a string that must begin and end with alphanumeric characters. Internal characters must be alphanumerics, hyphens, and/or underscores.

In principle, namespaces of constructions might be specified in the .conllu file, e.g. in a document metadata comment. This would enable formal linking to Constructicon resources such that a file could refer to constructions from different sources, and validation, for example to make sure that construction names are spelled correctly and contain valid construction element names. However, this is not part of the present spec.

### Locus of Annotation

As a matter of convention, we need to establish where in the UD tree—i.e., on which node—a construct is anchored. The name of the construction will be listed on this node in the Cxn field.

The simplest convention for determining the anchor is to use the lowest node in the tree which (i) is part of the construct, and (ii) dominates any other word that is in some part of the construct—content as well as functional elements. There is no requirement that the anchor dominate only words that belong to some part of the construct—in particular, additional modifiers or conjuncts (if a first element of a coordination) may be present as dependents.

If multiple constructs share the same anchor, they are sorted alphabetically by construction name and separated by commas. This will be quite common: for one thing, some of the constructs may represent modification constructions (of which there are an unbounded number); and moreover, constructions may overlap—e.g., a conditional and an existential (“If there are any good ideas…”), or an interrogative and a resultative (“Who let the dogs out?”).

### Units

As UD does not provide a theory of phrase structure, and all dependents of a construct anchor are not necessarily part of the construct, we cannot necessarily rely on full subtrees of a given node to express units of a construct. E.g., when annotating an existential construction:

	According1 to the teacher , there6 is a8 right answer10 and a wrong answer14 , but I am not sure which is which .

It would be reasonable to consider just the highlighted portion to be the span of the existential construct as a whole, and the underlined portion as the span of the Pivot element. However, “answer10” is the root of the full sentence, so simply anchoring the Existential construct (and its Pivot element) on node 10 is not very specific.

Token spans (or multispans for discontinuous expressions) would offer the most flexibility to express units. However, toolchains may focus on graph relations rather than token spans, and there may be substantial ambiguity resolution necessary to determine the precise span (e.g., including the nominal conjunct “and a wrong answer” but excluding the clausal conjunct “but I am not sure which is which”).

For maximum flexibility, at the format level, 4 kinds of units are available:
- A **span** (or multispan), which is specified in terms of UD word indices, and must contain a hyphen. (“13-13” is an example of a single-word span.)
- A **node**, without specifying what (if any) dependents may be involved in the unit.
- A **full subtree** (in the basic UD tree), which we notate as a node index followed by “f”, e.g. “13f”
- A **partial subtree**, which we notate as a node index followed by “p”, e.g. “13p”. This stands in contrast with a full subtree, indicating that not all dependents belong in the unit, but does not specify precisely which.

In the existential example, the rule for identifying the construction might specify “10p” as the Pivot element, whereas a more precise annotation might specify “8-14”.

### Multiple constructs of the same construction and anchor

It may be necessary to disambiguate these: e.g., in a clause with multiple protasis modifiers, there could be multiple Conditional labels on the same anchor:

	If you try3 to sound like an opera singer , it 'll just come14 to you if you have19 the ear

These require disambiguation, which is indicated with an index after “#”, where the order follows the order of the construct elements in the sentence (in this case, the Protasis elements):

	14	come	Cxn=Conditional#1,Conditional#2

Comparing construct element anchor tuples (3,14) and (14,19), 3 < 14, so the “if you try” construct is annotated first. If the full construction name only occurs once on an anchor, “#” indexations are not provided.

### Construct Elements

Elements of a construct are anchored on a node and linked via the CxnElt to the construct anchor. The unit information for the element, if specified, goes at the end following an “@” sign.

In the above example, this would look like
```
3	try	CxnElt=14:Conditional#1.Protasis@f

14	come	CxnElt=14:Conditional#1.Apodosis@p,14:Conditional#2.Apodosis@p

19	have	CxnElt=14:Conditional#2.Protasis@f
```

### Construction Elements

A construction may contain two kinds of construction elements: **content elements** (the constituent phrases carrying semantic weight) and **functional elements** (grammatical markers associated with the strategy that offer little independent meaning). Reflecting our meaning-based definitions of constructions as well as UD’s principle of favoring relations between content words, **only content elements are explicitly marked in our current implementation**. Thus, for example, the word “if” would not be individually marked as an element in an if-conditional (though its parent, the predicate serving as protasis, would). Neither would the tense of the predicate be marked as an element of the construction, even if it is part of the rule for detecting that construction. Finally, at present, **we only mark overt content elements**, never empty/omitted/implicit elements. Functional or empty construction elements may, however, be added in a future version.

## Inventory of Nomenclature

The full construction names currently included in UCxn are included below.

The nomenclature we use in the data—particularly for form/strategy subtypes—should be regarded as convenient to help disambiguate which rule (or group of closely related rules) produced which annotation. As such, the names reflect intralinguistic variety in the morphosyntactic patterns that fall under a construction family. For the full morphosyntactic details it is necessary to consult the rule itself.

Each name begins with the construction family name from the paper (“Conditional”, “Existential”, “Interrogative”, “Resultative”, or “NPN”; note that NPN is a form-based category as described in the paper, whereas the others are meaning-based constructions). Additional subtypes are provided in hyphenated parts, with more general/cross-linguistic/meaning-based ones preceding more specific/form-based ones.

At this point we do not impose a rigorous structure on construction names in the data. A mapping to more elaborate names (based on Morphosyntax; Croft 2022) clarifies which parts of the name correspond to different kinds of concepts, like construction vs. semantics vs. strategy. In future efforts with more constructions, it may become necessary to disambiguate terms in the data itself, e.g. “LocativeCxn” vs. “LocativeStr”.

| Cxn Family: Conditional | Content CxnElts: Protasis, Apodosis | |
| ----------- | ----------- | ----------- |
| Full Name in Data | Languages | Details |
|`Conditional-Interrogative` | hi, en | “What if” (Apodosis=“what”, Protasis=“if…”) |
|`Conditional-NegativeEpistemic`|cop, es, fr, he, hi, pt, zh | Negative epistemic stance a.k.a. counterfactual (“If you had arrived on time, we would have finished by now”: conditional event stipulated to have not occurred) |
|`Conditional-NegativeEpistemic-NoInversion` | en | Subject is present (nonreduced) and precedes the verb |
|`Conditional-NegativeEpistemic-Reduced` | en | |
|`Conditional-NegativeEpistemic-SubjVerbInversion` | en | |
|`Conditional-NeutralEpistemic` | cop, es, fr, he, hi, pt, zh | Neutral epistemic stance (“If you touch it, it will explode": conditional event may or may not occur) |
|`Conditional-UnspecifiedEpistemic-NoInversion` | en | |
|`Conditional-UnspecifiedEpistemic-Reduced` | en | |
|`Conditional-UnspecifiedEpistemic-SubjVerbInversion` | en | |
|`Conditional-Marker` | en | |
|`Conditional-Marker-Complex` | de | |
|`Conditional-Marker-Simple` | de | |
|`Conditional-Marker-Subjunctive` | hi | |
|`Conditional-Reduced` | fr, de | Reduced means no subject, e.g. “if possible”: Conditional_cxn-Deranked_str |
|`Conditional-SubjVerbInversion` | sv, de | |

| Cxn Family-Subfamily: Interrogative-Alternative | Content CxnElts: Clause, Choice1, Choice2, ... | |
| ----------- | ----------- | ----------- |
| Full Name in Data | Languages | Details |
|`Interrogative-Alternative` | es, fr, pt | AlternativeQuestion_cxn |

| Cxn Family-Subfamily: Interrogative-WHInfo | Content CxnElts: Clause, WHWord | |
| ----------- | ----------- | ----------- |
| Full Name in Data | Languages | Details |
|`Interrogative-WHInfo` | cop | AlternativeQuestion_cxn |
|`Interrogative-WHInfo-Direct` | de, en, es, fr, hi, he, pt, sv, zh | InformationQuestion_cxn |
|`Interrogative-WHInfo-Indirect` | de, en, es, fr, hi, he, pt, sv | InterrogativeComplement_cxn-InformationQuestion_inf |

| Cxn Family-Subfamily: Interrogative-Polar | Content CxnElts: Clause | |
| ----------- | ----------- | ----------- |
| Full Name in Data | Languages | Details |
|`Interrogative-Polar` | cop | |
|`Interrogative-Polar-Direct` | de, en, es, fr, hi, he, pt, sv, zh | PolarityQuestion_cxn |
|`Interrogative-Polar-Indirect` | de, en, es, fr, hi, he, pt, sv | InterrogativeComplement_cxn-PolarityQuestion_inf |

| Cxn Family-Subfamily: Interrogative-Reduced | Content CxnElts: Clause | |
| ----------- | ----------- | ----------- |
| Full Name in Data | Languages | Details |
|`Interrogative-Reduced` | zh | Contains a question mark but doesn’t match other queries; context-dependent interpretation |

| Cxn Family: Existential | Content CxnElts: Pivot, sometimes Coda | |
| ----------- | ----------- | ----------- |
| Full Name in Data | Languages | Details |
|`Existential-CopPred` | hi, he | Hebrew past & future |
|`Existential-CopPred-HereExpl` | en | Technically this “be” is tagged as a VERB in English, but we can think of it as recruited from the copula “be”. |
|`Existential-CopPred-ThereExpl` | de, en |  |
|`Existential-ExistPred` | cop, sv, pt |  |
|`Existential-ExistPred-FullVerb` | he | קיים |
|`Existential-ExistPred-NoExpl` | en | a path to victory exists” (in contrast with Existential-ExistPred-ThereExpl “There exists a path to victory”); cf. Existential-ExistPred-FullVerb in Hebrew |
|`Existential-ExistPred-ThereExpl` | en | “There exist” (unattested in EN data; but would be a case of overlap between current ThereExpl and ExistPred rules) |
|`Existential-ExistPred-VblPart` | he | Verb-like particle (tagged as VERB in UD but not a full verb): יש |
|`Existential-GivePred-ItExpl` | en | |
|`Existential-HavePred` | es, pt, zh | |
|`Existential-HavePred-ItExpl-ThereExpl` | fr | "il y a" |
|`Existential-MannerPred-ThereExpl` | en | “There stretched…new vistas of trees and paths…” |
|`Existential-NotExistPred` | cop | |
|`Existential-NotExistPred-VblPart` | he | |

| Cxn Family: Resultative | Content CxnElts: Event, ResultState | |
| ----------- | ----------- | ----------- |
| Full Name in Data | Languages | Details |
|`Resultative` | zh | |

| Cxn Family: NPN | Content CxnElts: N1, N2, P | |
| ----------- | ----------- | ----------- |
| Full Name in Data | Languages | Details |
|`NPN` | cop, de, en, es, fr, (hi), he, pt, sv, | |

## List of annotated treebanks

| Treebank | Language | Constructions Covered | Strategies Covered | Contact | 
| ----------- | ----------- | ----------- | ---------- |
| German HDT | German | Conditional, Interrogative, Existential, NPN | `Conditional-Marker-Complex, Conditional-Marker-Simple, Conditional-Reduced, Conditional-SubjVerbInversion, Interrogative-WHInfo-Direct, Interrogative-WHInfo-Indirect, Interrogative-Polar-Direct, Interrogative-Polar-Indirect, Existential-CopPred-ThereExpl, NPN` | Leonie Weissweiler |

## How to add constructions and languages

### Adding a new language

- decide on a treebank
- check standards of the treebank: manual, semi-automatic, or automatic?
- go through list of existing constructions and strategies and decide which apply
- if you think a strategy in your language might overlap with an existing one and you want to discuss, open a github issue and copy in the responsible annotators

### Adding a new construction

- check the Morphosyntax database

## Annotating for UCxn with Grew Rules

Below are examples of rules, selected to illustrate a range of construction families. The full suite of rules is hosted in the repository at https://github.com/LeonieWeissweiler/UCxn.

### Customization of query language for specifying rules

The Grew system for expressing and applying patterns required a slight extension for this project. Grew itself is not expressive enough to support construct-append operations (where multiple constructs occur on the same anchor, and multiple constructs of the same construction require disambiguation) or linking of elements to their construct anchors. We therefore designate a special variable name for anchors and apply postprocessing to populate the Cxn and CxnElt fields. Here is a Swedish example:

```
rule r3a { % Conditionals with 'om'
	pattern {
		_anchor_ -["advcl"|"advmod"]-> P;
		P-[mark]->M;
		M[lemma="om"|"ifall"];
	}
	commands {
		_anchor_.Cxn="Conditional-Marker";
		P.CxnElt="Protasis";
		_anchor_.CxnElt="Apodosis";
	}
}
```

In our rules, the special name _anchor_ is used for the variable matching the construct anchor node. In the commands block, the _anchor_ is always assigned a construction name in its Cxn property, and then nodes may be identified as elements (understood to belong to the same construct). The full string values for the MISC column (with node indices and comma separators and so forth) are constructed under the hood. Note that a rule can match multiple times per sentence and a node may serve as the anchor for multiple constructs of the same or different constructions. However, only one construct can be annotated per application of a rule.

The script for this customized annotation can be found at https://github.com/LeonieWeissweiler/UCxn/blob/main/grew_rules/ucxn_writing.py 

### A Conditional Rule in Swedish

```
rule Conditional-NegativeEpistemic {
	pattern {
		_anchor_-[advcl]->P;
		P->A;
		A[Mood=Sub, Tense=Imp, lemma=haber];
		P-[mark]->S1;
		S1[upos=SCONJ,lemma=si]
	}
	without {
		P-[mark]->S2;
		S2[upos=SCONJ,lemma=como]
	}
	commands {
		_anchor_.Cxn = "Conditional-NegativeEpistemic";
		_anchor_.CxnElt = "Apodosis@p";
		P.CxnElt = "Protasis@f"
	}
} 	
```

### Existential rules in Coptic and French, respectively

```
rule ExistentialNegative {
    pattern {
      _anchor_ [lemma="ⲙⲛ",xpos=EXIST];
  	_anchor_ -[nsubj]-> SBJ;
    }
    commands {
       _anchor_.Cxn="Existential-NotExistPred";
       SBJ.CxnElt="Pivot";
    }
  }

rule Existential-HavePred-ItExpl-ThereExpl {
	pattern {
		_anchor_ [lemma="avoir"]; N1[lemma="y"];
		_anchor_-[expl:comp]->N1;
		_anchor_ -[obj]->N2;
		N2[upos=NOUN]
	}   
	commands {
		_anchor_.Cxn = "Existential-HavePred-ItExpl-ThereExpl";
		N2.CxnElt = "Pivot@f"
	}
}
```

### Interrogative rules in Hebrew, Hindi, and Portuguese, respectively

```
rule r1a { %  Main clause polar with particle
	pattern {
		PRT [lemma = "שמא"|"האם"];  
		_anchor_-[mark:q]->PRT ;  
		Q [form="?"];
	}
	commands {
		_anchor_.Cxn="Interrogative-Polar-Direct";
		_anchor_.CxnElt="Clause";
	}
}

rule int-direct-info { % Interrogatives - Direct information questions
	pattern {
		W [lemma="क्या"|"कौन"|"कहाँ"|"कहां"|"कब"|"कैसे"|"कितना"|"किस"];
		_anchor_ -[^root]-> W;
	}
	without { SC [form="कि"]; _anchor_ -[mark]-> SC }
	without { V1 [upos=VERB]; V1 -[advcl]-> _anchor_; }
	commands {
		_anchor_.Cxn="Interrogative-WHInfo-Direct";
		_anchor_.CxnElt="Clause";
		W.CxnElt="WHWord"
	}
}

rule InterrogativeAlternativeRule1 {
	pattern {
		OR [lemma="ou"];
		IN [lemma="?"];
		_anchor_-[^root]->CH1;
		CH1-[conj]->CH2;
		CH2-[cc]->OR;
		CH1->IN;
	}
	without { CH1-[conj]->CH3; }
	commands {
		_anchor_.Cxn = "Interrogative-Alternative";
		_anchor_.CxnElt = "Clause";
		CH1.CxnElt = "Choice1";
		CH2.CxnElt = "Choice2";
	}
}
```

### Interrogative rules in Hebrew, Hindi, and Portuguese, respectively

```
rule NPN {
	pattern {
		_anchor_[upos=NOUN];
		N2[upos=NOUN];
		_anchor_.form = N2.form;
		P[upos=ADP];
		_anchor_ < P;
		P < N2
	}
	without {
		A[upos=ADP];
		A < _anchor_
	}
	commands {
		_anchor_.Cxn="NPN";
		_anchor_.CxnElt="N1";
		P.CxnElt="P";
		N2.CxnElt="N2"
	}
}
```

### A Resultative rule in Chinese

```
rule r1 {
	pattern {
		_anchor_ -[compound:vv]-> RES;
	}
	commands {
		_anchor_.Cxn=Resultative;
	_anchor_.CxnElt=Event;
	RES.CxnElt=ResultState;
	}
}
```

## How to cite

When using this work, please cite 

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
