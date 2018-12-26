#Automatically deriving concept hierarchies from text using FCA

import nltk
from nltk.tree import *
from nltk.parse import stanford
from nltk.stem import WordNetLemmatizer
import nltk.data
import nltk.draw
import os
import sys

import csv
import pandas as pd
import numpy as np

os.environ['STANFORD_PARSER'] = ''
os.environ['STANFORD_MODELS'] = ''

wordnet_lemmatizer = WordNetLemmatizer()

class SVO(object):
    
    #Class Methods to Extract Subject-Verb Pairs and Object-Verb Pairs from Text
    
    def __init__(self):
        
        #Initialize the SVO Methods
        
        self.noun_types = ["NN", "NNP", "NNPS","NNS","PRP"]
        self.verb_types = ["VB","VBD","VBG","VBN", "VBP", "VBZ"]
        self.adjective_types = ["JJ","JJR","JJS"]
        self.pred_verb_phrase_siblings = None
        self.parser = stanford.StanfordParser()
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    def get_subject(self,sub_tree):
        """
        Returns the Subject and all attributes for a subject, sub_tree is a Noun Phrase
        """
        sub_nodes = []
        sub_nodes = sub_tree.subtrees()
        sub_nodes = [each for each in sub_nodes if each.pos()]
        subject = None
        for each in sub_nodes:
            if each.label() in self.noun_types:
                subject = each.leaves()
                #Converting list to string
                subject = ''.join(subject)
                #print(subject)
                
                #Lemmatization using WordNet lexical database
                subject = nltk.word_tokenize(subject)
                for w in subject:
                    s = wordnet_lemmatizer.lemmatize(w)
                    subject = s.split()
                    
        return {'subject':subject}

    def get_object(self,sub_tree):
        """
        Returns an Object with all attributes of an object
        """
        siblings = self.pred_verb_phrase_siblings
        Object = None
        for each_tree in sub_tree:
            if each_tree.label() in ["NP","PP"]:
                sub_nodes = each_tree.subtrees()
                sub_nodes = [each for each in sub_nodes if each.pos()]

                for each in sub_nodes:
                    if each.label() in self.noun_types:
                        Object = each.leaves()
                        #break
                        #Converting list to string
                        Object = ''.join(Object)
                        Object = nltk.word_tokenize(Object)
                        for w in Object:
                            o = wordnet_lemmatizer.lemmatize(w)
                            Object = o.split()
                break
            else:
                sub_nodes = each_tree.subtrees()
                sub_nodes = [each for each in sub_nodes if each.pos()]
                for each in sub_nodes:
                    if each.label() in self.adjective_types:
                        Object = each.leaves()
                        #break
                        Object = ''.join(Object)
                        
                        #Lemmatization using WordNet lexical database
                        Object = nltk.word_tokenize(Object)
                        for w in Object:
                            o = wordnet_lemmatizer.lemmatize(w)
                            #print(o)
                            Object = o.split()
                            #print("Lemmatised Object",Object)
                # Get first noun in the tree
        
        self.pred_verb_phrase_siblings = None
        return {'object':Object}

    def get_verbs_list(self, sub_tree):
        sub_nodes = []
        sub_nodes = sub_tree.subtrees()
        sub_nodes = [each for each in sub_nodes if each.pos()]
        verb = None
        verb_list = []

        pred_verb_phrase_siblings = []
        sub_tree  = ParentedTree.convert(sub_tree)
        for each in sub_nodes:
            if each.label() in self.verb_types:
                sub_tree = each
                verb = each.leaves()
                #Converting list to string
                verb = ''.join(verb)
                
                #Lemmatization using WordNet lexical database
                verb = nltk.word_tokenize(verb)
                for w in verb:
                    v = wordnet_lemmatizer.lemmatize(w)
                    verb_list.append(v)
        
        return verb_list

    def get_verbs(self, sub_tree):
        """
        Returns the Verb along with its attributes, Also returns a Verb Phrase
        """

        sub_nodes = []
        sub_nodes = sub_tree.subtrees()
        sub_nodes = [each for each in sub_nodes if each.pos()]
        verb = None
        verb_list = []


        pred_verb_phrase_siblings = []
        sub_tree  = ParentedTree.convert(sub_tree)
        for each in sub_nodes:
            if each.label() in self.verb_types:
                sub_tree = each
                verb = each.leaves()
                #Converting list to string
                verb = ''.join(verb)
                # print(verb)

                #Lemmatization using WordNet lexical database
                verb = nltk.word_tokenize(verb)
                for w in verb:
                	v = wordnet_lemmatizer.lemmatize(w)
                	#print(v)
                	verb = v.split()
                	

        #get all pred_verb_phrase_siblings to be able to get the object
        sub_tree  = ParentedTree.convert(sub_tree)
        if verb:
             pred_verb_phrase_siblings = self.tree_root.subtrees()
             pred_verb_phrase_siblings = [each for each in pred_verb_phrase_siblings if each.label() in ["NP","PP","ADJP","ADVP"]]
             self.pred_verb_phrase_siblings = pred_verb_phrase_siblings
             #print(pred_verb_phrase_siblings)

        return {'verb':verb}

    def process_parse_tree_verb_subject(self,parse_tree):
        """
        Returns the Subject-Verb-Object Representation of a Parse Tree.
        Can Vary depending on number of 'sub-sentences' in a Parse Tree
        """
        self.tree_root = parse_tree
        # Step 1 - Extract all the parse trees that start with 'S'
        svo_list = [] # A List of SVO pairs extracted
        
        #List containing subject-verb pairs 
        output_list_sv = []
        #Dictionary containing subject-verb pairs
        output_dict_sv ={}
        verb_list = []
        output_list = []
        verb_dict = {}
        i=0

        for idx, subtree in enumerate(parse_tree[0].subtrees()):
            subject =None
            verb = None
            Object = None
            if subtree.label() in ["S", "SQ", "SBAR", "SBARQ", "SINV", "FRAG"]:
                children_list = subtree
                children_values = [each_child.label() for each_child in children_list]
                children_dict = dict(zip(children_values,children_list))


                # Extract Subject, Verb-Phrase, Objects from Sentence sub-trees
                if children_dict.get("NP") is not None:
                    subject = self.get_subject(children_dict["NP"])

                if children_dict.get("VP") is not None:
                    # Extract Verb and Object
                    
                    verb = self.get_verbs(children_dict["VP"])
                    # print(verb)
                    
                    
                #Printing only the subject and verb
                try:
                	if subject['subject'] and verb['verb']:
                		output_dict_sv['verb'] = verb['verb']
                		output_dict_sv['subject'] = subject['subject']
                		output_list_sv.append(output_dict_sv)
                except Exception as e:
                        #print(e)
                        continue
                
                
        return output_dict_sv
    

    def process_parse_tree_verb_object(self,parse_tree):
        """
        Returns the Subject-Verb-Object Representation of a Parse Tree.
        Can Vary depending on number of 'sub-sentences' in a Parse Tree
        """
        self.tree_root = parse_tree
        # Step 1 - Extract all the parse trees that start with 'S'
        svo_list = [] # A List of SVO pairs extracted
        
        output_list_ov = []
        #Dictionary containing subject-verb pairs
        output_dict_ov = {}

        output_list = []
        i=0

        for idx, subtree in enumerate(parse_tree[0].subtrees()):
            subject =None
            verb = None
            Object = None
            if subtree.label() in ["S", "SQ", "SBAR", "SBARQ", "SINV", "FRAG"]:
                children_list = subtree
                children_values = [each_child.label() for each_child in children_list]
                children_dict = dict(zip(children_values,children_list))


                # Extract Subject, Verb-Phrase, Objects from Sentence sub-trees
                if children_dict.get("NP") is not None:
                    subject = self.get_subject(children_dict["NP"])

                if children_dict.get("VP") is not None:
                    # Extract Verb and Object
                    
                    verb = self.get_verbs(children_dict["VP"])
                    #print(verb)
                    Object = self.get_object(children_dict["VP"])

                try:
                	if verb['verb'] and Object['object']:
                		output_dict_ov['verb'] = verb['verb']
                		output_dict_ov['object'] = Object['object']
                		if output_dict_ov.keys() is verb:
                			print("SLEEP", list(output_dict_ov.values()))
                		output_list_ov.append(output_dict_ov)

                except Exception as e:
                        #print(e)
                        continue

        return output_dict_ov
    
    def sentence_split(self,text):
        """
        returns the Parse Tree of a Sample
        """
        sentences = self.sent_detector.tokenize(text)
        return sentences


    def get_parse_tree(self,sentence):
        """
        returns the Parse Tree of a Sample
        """
        parse_tree = self.parser.raw_parse(sentence)

        return parse_tree

    
svo = SVO()

#Change directory for the file here
file = open(r"C:\Users\mehar\Desktop\IIIT_Winter\pizza.txt", "r")
sentence = file.read()
    
sentences =  svo.sentence_split(sentence)
val_sub_verb = []
val_obj_verb = []

val = []
verb_list_final = ['']
for sent in sentences:
    root_tree = svo.get_parse_tree(sent)
    val_sub_verb.append(svo.process_parse_tree_verb_subject(next(root_tree)))
    

print("Subject-Verb Pairs")

df_sv = pd.DataFrame(val_sub_verb)
print(df_sv)
df_sv_2 = df_sv.dropna()
print(df_sv_2)
print(df_sv_2['subject'].apply(''.join))

df_sv_final = pd.concat([df_sv_2['subject'].apply(''.join),pd.get_dummies(df_sv_2['verb'].apply(''.join))],axis=1)
print("FINALLLY")
print(df_sv_final)


df_sv_final.to_csv("final_5.csv",index=False)

print(*val_sub_verb, sep = "\n")

for sent in sentences:
    root_tree = svo.get_parse_tree(sent)
    val_obj_verb.append(svo.process_parse_tree_verb_object(next(root_tree)))

print("Object-Verb Pairs")

df_ov = pd.DataFrame(val_obj_verb)
print(df_ov)
df_ov_2 = df_ov.dropna()
print(df_ov_2)
print(df_ov_2['object'].apply(''.join))

df_ov_final = pd.concat([df_ov_2['object'].apply(''.join),pd.get_dummies(df_ov_2['verb'].apply(''.join))],axis=1)
print("FINALLLY")
df_ov_final.reindex(index=range(len(df_ov_final)))
print(df_ov_final)

df_ov_final.to_csv("final_6.csv", index=False)
print(*val_obj_verb, sep = "\n")

result = pd.concat([df_sv_final,df_ov_final], axis =0)
print(result)

result = result.replace(np.nan, '', regex = True)
result['final'] = result["object"].map(str) + result["subject"]
print(result)

result.pop('object')
result.pop('subject')
print(result)
result.to_csv("final_7.csv", index=False)

result_new = result[['final']].copy()
print(result_new)

result_new_2 = result.drop('final', axis = 1)
print(result_new_2)

result_final = pd.concat([result_new, result_new_2], axis = 1)
result_final['final'].str.lower()
result_final_final = result_final.sort_values('final')
result_final_final.replace('', np.nan, inplace=True)
result_final_final.fillna("0", inplace=True)
print(result_final_final)
r = result_final_final.groupby('final', as_index=False).sum()
print(r)
result_final_final = r.replace(2, 1)
print(result_final_final)

result_final_final.to_csv("final_CONTEXT.csv", index=False)

for sent in sentences:
    root_tree = svo.get_parse_tree(sent)
    val.append(svo.get_verbs_list(next(root_tree)))
    # val_sub_verb.append(svo.process_parse_tree_verb_subject(next(root_tree)))
print("Verb_list",val)
for sublist in val:
    for item in sublist:
        verb_list_final.append(item)
print("Verb_list",verb_list_final)

#Keeping the list unique
verb_list_final = list(set(verb_list_final))
print("Verb_list unique",verb_list_final)


#THE OUTPUT IS SAVED IN FINAL_CONTEXT.CSV FILE. 
#TAKE THE OUTPUT AND OPEN IN THE SODTWARE FOR THE CONCEPT LATTICE
#http://sourceforge.net/projects/conexp).

#DOWNLAOD AND OPEN THE FILE CONEXP.BAT TO RUN IT
#OPEN THE FINAL_CONTEXT.CSV FILE AND CLICK ON BUILD LATTICE OPTION
