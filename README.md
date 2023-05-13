# Group B: Standard for construction annotation layer in UD

## ToDos

### Concrete First Steps

Start small: choose a limited family of constructions to annotate
- age constructions (very limited)
- idiosyncratic, lexicalised constructions, such as X-and-X (Swedish), X-über-X (German), N-after-N (English)
- rates (mph etc), comparatives, resultatives...

### Decisions
- naming convention for constructions
- integration with existing annotation tools
- annotating/marking candidates that have been checked and are *not* a certain construction
- put the annotation on the highest element in the basic UD tree - which one if it's disconnected? 

### Putting our head in the sand
- cross-sentential constructions
- nesting and composition of constructions

### Publications/venues:
- LREC (deadline 13.10.2023)
- UDW (2024?)
- ICCG (deadline in spring 2024)
- Phraseology & multi-word expressions (LangSciPress)

## Example

Example Sentence:
 1:the  2:more  3:you  4:post  5:,  6:the  7:more  8:money  9:you  10:make (assuming the first comparative word is the head – 2:more)
 
 ### Simple (only construction name)
 2:more CxN (comparative-correlative)
 
 ### Medium (include the span)
 CxN (comparative-correlative=110)
 
 ### Full
 Cxn(comparative-correlative, Condition=1-4, Result=6-10, ConditionDegree=2, ResultDegree=7)

### Dependent-based
- 2:more the Simple
- 8:money CxNElt(2, Result)
- 7:more CxNElt(2, ResultDegree)


# Group C: Searching for constructions in UD treebanks

## Methods
- formulating search queries that can find examples of a given construction with good recall but probably less good precision
- developing semi-automatic techniques for extracting the search queries from an existing constructicon entry
- increase recall by using approximative tree matching or loosening some constraints


## Outputs
- candidates for manual annotation by Group B
- an in-development English constructicon? 
- guidelines for others to write queries


# Interesting Links

## Existing Constructicons

Overview: CAW, November 2022 https://www.globalframenet.org/caw2022 

- English: https://constructicon.de/ and https://www.google.com/url?q=http://sato.fm.senshu-u.ac.jp/frameSQL/cxn/CxNeng/cxn00/21colorTag/index.html&sa=D&source=editors&ust=1683996774758710&usg=AOvVaw2nAtAknV5pnjpNFFLeU15U
- German: https://gsw.phil.hhu.de/ 
- Swedish: https://spraakbanken.gu.se/karp/#?mode=konstruktikon
- Brazilian Portuguese: https://www2.ufjf.br/framenetbr-en/ 
- Japanese: https://jfn.st.hc.keio.ac.jp/ 
- Russian: https://site.uit.no/russian-constructicon/ 

## Database of Croft's Comparative Concepts: https://spraakbanken.github.io/ComparativeConcepts/

## Search/query engines
- Grew-match: https://match.grew.fr/ 
- Corpus workbench (for large corpora): several sites use CWB
- SPIKE (query-by-example): https://spike.apps.allenai.org/datasets/wikipedia/search 

