# UniCoDeX 1st Meeting Notes

## Present: Peter, Nurit, Archna, Nina, Amir, Leonie, Nathan

## Logistics
- zoom link for the future: https://georgetown.zoom.us/j/92993543037?pwd=RWljM3pySzZrWi9Za0FnV1VIZENKZz09 
- when2meet for next meeting: https://www.when2meet.com/?20193688-aAyPT 

## Outcomes
- we will meet again next week, to discuss more specific todos and a workflow
- we will wait with crosslingual comparison for Group A/Joakim to make progress on the Swadesh list
- we will wait with subword-level constructions for the UniMorph-UD group to develop a standard
- we have to figure out which constructions to select
- we also have to figure out where to put our automatic and gold annotations and how and when to release them

## Full Notes

Amir is showing us more about his reply to Nathan’s github issue. He filtered out constructions that are more frequent than 10% of sentences and single-word constructions. 
Peter is suggesting leaving out things that are already included in UD annotations, like transitivity. 
Nurit thinks we should think about the goal and the users to figure out what the goals will be. 
Peter thinks people working in language learning or analysing text will want to find instances, but then there are also construction grammarians who want to build a constructicon. Amir says that we heard from Lori that she would like to find things like all excess constructions, on the other hand it ties into UD for linguistic comparison and typology. 
Leonie says that we should decide on a tool. 
Peter says we shouldn’t limit ourselves. 
Amir says that it’s important to make this accessible. 
Leonie says we might want a universal rule format so that we can have them in a list that’s independent of formalisms. 
Amir says that this means that we’re using CONLL-U format because that’s universal to all tools except SPIKE. Nurit says that we should maybe pick 10 languages to start with but that would be very different than looking at just one language. 
Peter says all constructions should be an instance of some meta-construction like Croft’s strategies. 
Amir says that the actual constructions are very language-specific. 
Leonie says that we should maybe wait for group A so that we don’t have to double up on the cross-linguistic comparison. Peter says that Joakim will be starting on that in autumn. 
Peter says that him and Lori have gotten started on the Dagstuhl report and shows us the draft of the document and asks if anyone is interested in helping to write the summary. 
Nathan joins. 
The idea of doing morphology as well is floated but postponed until the UniMorph group comes up with a standard. 
Peter raises the issue of how to catch false negatives. 
Amir says either you do an exhaustive annotation of a subset, which is a problem for rare constructions, or to rely on a different annotation layer, for example using pragmatic annotations that are already there. 
Peter says that you could maybe also automatically relax the query to find matches that are close, but not quite, and Nathan suggests embeddings for similar sentences. Nathan talks about a paper of his that searched for rare senses of frequent words using embeddings (BERT has uncommon sense). 
Nathan is worried about maintaining the distinction between automatically and manually annotated constructions in the UD file. Leonie asks if we want to also release the automatically annotated or just the gold data. 
Amir proposes to decide construction by construction how much checking you think you need to do. Nathan says that the issue of gold-ness of the annotation is heightened in the case of constructions because the processes might be different. 
Amir says we need a giant spreadsheet of constructions and datasets and notes on how confident we feel about each of them. 
Nathan asks if there’s harm in having an in-progress field in the UD file and Amir thinks that this would be overloading. 
Nathan says that it would be an extra field for constructions, or two if there’s also status, Amir thinks that’s not clean enough. 
Nathan worries about there being no standard for the treebanks. 
Peter says that we don’t know how much detail we want yet. 
Amir says that there are many things we don’t know about each treebank’s source and we shouldn’t cram it into the file. 
Nathan says that we should think about what documentation we want in our repo. 
Nurit asks what our goals are. Leonie says we talked about LREC in October. 
Peter says that we should focus on one treebank and one language. 
Nathan says that the workflow and annotation format are the first thing and it would be good to have some pilots from a few different treebanks. 
Peter doesn’t think we’ll have a resource by October, Nathan says it could be a prototype, Leonie thinks that’s already publishable. Nathan asks about a regular meeting slot. 
Nathan proposes to meet again next week. The meeting times would be from 10am for Nathan and until 8pm for Nurit. 
