**1st June 2018**

Reading the book "Ontology Learning and Population from Text" and the algorithms mentioned till chapter 4.
Start implementation from Monday.

**4th June 2018**

Understanding and implementing the algorithms. Implementation of first algorithm (Naive FCA Algorithm) done

**5th June 2018**

Implemented second algorithm (Ganter's FCA Algorithm). Started to implement the next one

**6th June 2018**

Read about clustering in unsupervised problems and have implemented the third algorithm (K Means Algorithm). Started to implement the next ones which are on hierarchical clustering.

**7th June 2018**

Read about Hierarchical clustering approaches like Agglomerative Clustering, Divisive Clustering and Bi-Section KMeans and understood the algorithms given in the text (Leaving the implementation part for Algo 4, 5, 6) 

**8th June 2018**
Reading chapter 6 of the book that looks into concept hierarchy induction and the common approaches to learning the concept hierachies.
Read about the apporoach based on FCA which groups and hierarchically orders words or terms according to use or behaviour in corpus. Need to implement Algorithm 7 where we will form the lattice from the respective document and hence the concept hierarchy. 

**11th and 12th June 2018**

Implementing Algorithm 7 - Constructing a concept hierarchy for terms in a document using Formal Concept Analysis. 
This algorithm divided into several parts. 
1. Firstly, we find a specific corpus (I have taken a small document about types of pizza)
2. The corpus is POS taggered. The book mentions the use of TreeTagger which I had implemented by didnt find useful and found using nltk much easier and better results
3. It is then parsed. The text mentions a LoPar parser which I couldnt implement. Tried several other parsers. 
4. V-Subj, V-Obj, V-PP dependencies are extracted from the parsed texts/trees. I have extracted the verbs from the text in one way and also tried to extract triples (subject-predicate-object) using the Stanford Parser
5. Verbs are then lemmatized
6. The pairs are smoothed. 
7. There are some problems that arise. Either the output of the parser could be errorenous or want to delete some of the pairs. so we weight the pairs and consider only those that are above a certain threshold. We can use conditional probabitity measure, or PMI or Resnik. It has been found that the first one yeilds better results than the other two. Also, much easier to implement. 
8. Transformed to a formalConcept to which FCA is now applied. 
9. We get the corresponding lattice...
10. After this, we transform it to partial order (closer to the final desired output). It is compacted to get final concept hierarchy. 

I also tried implemeting this algo using SpaCy as it is faster in terms of speed and gives results with higher precision. Faced a few difficulties. Will still try to finish after a few days. 
