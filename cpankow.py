from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk.chunk.regexp import RegexpParser
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests, re, urllib, warnings
from urllib.parse import urlparse
from urllib.error import HTTPError
import operator
import numpy as np
import nltk
from collections import Counter

def checkAppropriateURL(url):
    parsedURL = urlparse(url)   
    # print (parsedURL)
    extn = parsedURL.path.split(".")[-1]
    site = parsedURL.netloc.split(".")
    path = parsedURL.path.split("/")[-1]
    # print (site)
    if extn in ["pdf","doc","docx","xls","xlsx","ppt","pptx","odt"]:
        return False
    if any(i in site for i in ["pinterest"]):
        return False
    r = dict(requests.head(url).headers)["Content-Type"].split(";")[0]
    if(not r=="text/html"):
        print ("Failed",url,r)
        return False
    return True

def scrapeGoogleForAbstracts(query, count):
    # print (query)
    words = query.split()
    q = ("+").join(words)
    print(q)
    gurl = "https://www.google.co.in/search?limit=20&q=" + q
    print ("gurl is:",gurl)
    data = requests.get(gurl).text
    soup = BeautifulSoup(data, "lxml")
    divText = soup.find(id="resultStats").text
    numberString = re.match("About (.*) results", divText).group(1)
    number = int("".join(numberString.split(",")))
    h3Rows = soup.find_all("h3", {"class":"r"})
    urls = []
    # print (soup.prettify(), h3Rows)
    for h3Row in h3Rows:
        try:
            url = h3Row.find("a")['href']
            if(url[0]=="/"):
                continue
            print ("url is:",url)
        except (GeneratorExit, KeyboardInterrupt, SystemExit):
            raise
        except:
            continue
        par = urllib.parse.parse_qs(urlparse(url).query)
        try:
            appendingURL = par['q'][0]
        except:
            continue
        print (appendingURL)
        if(not checkAppropriateURL(appendingURL)):
            print ("no",appendingURL)
            continue
        # print ("yes",appendingURL)
        urls.append(appendingURL)
    # print(len(urls),urls)
    start = 20
    i = 1
    while(len(urls)<count):
        # print (len(urls),number)
        tempurl = gurl+ "&start=" +str(i*20)
        i+=1
        data = requests.get(tempurl).text
        soup = BeautifulSoup(data, "lxml")
        h3Rows = soup.find_all("h3", {"class":"r"})
        for (j,h3Row) in enumerate(h3Rows):
            try:
                url = h3Row.find("a")['href']
            except (GeneratorExit, KeyboardInterrupt, SystemExit):
                raise
            except:
                continue
            par = urllib.parse.parse_qs(urlparse(url).query)
            try:
                appendingURL = par['q'][0]
                if(not checkAppropriateURL(appendingURL)):
                    print ("no",appendingURL)
                    continue
                print ("yes",appendingURL)
                urls.append(appendingURL)
                print (j, par['q'][0])
            except (GeneratorExit, KeyboardInterrupt, SystemExit):
                raise
            except:
                continue
    print ("This is list of all URLs",urls[:count])
    return (number, urls[:count])

def getInstances(text):
    grammar = """
        PRE:   {<NNS|NNP|NN|NP|JJ|UH>+}
        MID: {<DT|IN|POS|FW|-|NP|NPS|NN|NNS>+}
        INSTANCE:   {(<DT+>)?(<JJ+>)?<PRE>(<MID><PRE>)?}
    """
    chunker = RegexpParser(grammar)
    taggedText = pos_tag(word_tokenize(text))
    textChunks = chunker.parse(taggedText)

    # print (textChunks)
    
    current_chunk = []

    for i in textChunks:
        if (type(i) == Tree and i.label() == "INSTANCE"):
            # print (i.leaves())
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))

    # print (current_chunk)
    return current_chunk

def getConcepts(text):
    grammar = """
        CONCEPT:   {(<DT>)?(<JJ>)?<NN|NNS>+}
    """
    chunker = RegexpParser(grammar)
    taggedText = pos_tag(word_tokenize(text))
    textChunks = chunker.parse(taggedText)
    current_chunk = []
    for i in textChunks:
        if (type(i) == Tree and i.label() == "CONCEPT"):
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
    return current_chunk

def getCluesPatternsTuple():
    Hearsts = []
    Hearsts.append((["(CONCEPT\,?)",".*?","( such as )", "(INSTANCE)"]," such as ","first"))
    #Hearsts.append((["(CONCEPT\,?)",".*?","(\( ?especially \,?)","(INSTANCE)"]," especially ","first"))
    #Hearsts.append((["(CONCEPT\,?)",".*?","( including )","(INSTANCE)"],"including","first"))
    #Hearsts.append((["(CONCEPT\,?)",".*?","( include )","(INSTANCE)"],"include","first"))
    #Hearsts.append((["(CONCEPT\,?)",".*?","( included in )","(INSTANCE)"],"included in","first"))
    #Hearsts.append((["(INSTANCE\,?)",".*?","( and other )","(CONCEPT)"]," and other ","last"))
    #Hearsts.append((["(INSTANCE\,?)",".*?","( or other )","(CONCEPT)"]," or other ","last"))
    #Hearsts.append((["(CONCEPT\,?)",".*?","( like )","(INSTANCE)"]," like ","first"))
    return (Hearsts)

def URLInput():
    url = 'https://www.webstaurantstore.com/article/101/types-of-pizza.html'
    text = getTextFromURL(url)
    return text

def DocInput():
    file = open("C:/Python34/Internship/Algorithms/Algorithm 7/pizza_document_2.txt")
    text = file.read()
    return text

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    # Scraping a Web Document

    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def getTextFromURL(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}
    # print (url)
    html = urllib.request.urlopen(urllib.request.Request(url, headers=hdr))
    inputText = text_from_html(html)
    return inputText

def getAbstracts(query, count):
    (number, urls) = scrapeGoogleForAbstracts(query, count)
    # print ("lenght",len(urls))
    texts = []
    for url in urls:
        print (url)
        try:
            text = getTextFromURL(url)
        except (GeneratorExit, KeyboardInterrupt, SystemExit):
            raise
        except:
            continue
        texts.append((url,text.strip()))
    return (number, texts)

stopwords_en = stopwords.words("english")

def preprocessing(raw):
    wordlist = word_tokenize(raw)
    text = [w.lower () for w in wordlist if w not in stopwords_en]
    return text

def simDoc(text1, text2):
    word_set = set(text1).union(set(text2))

    freqd_text1 = FreqDist(text1)
    text1_count_dict = dict.fromkeys(word_set, 0)
    for word in text1:
        text1_count_dict[word] = freqd_text1[word]

    freqd_text2 = FreqDist(text2)
    text2_count_dict = dict.fromkeys(word_set, 0)
    for word in text2:
        text2_count_dict[word] = freqd_text2[word]

    taggeddocs = []
    doc1 = TaggedDocument(words = text1, tags = [u'NEWS_1'])
    taggeddocs.append(doc1)
    doc2 = TaggedDocument(words = text2, tags = [u'NEWS_2'])
    taggeddocs.append(doc2)

    #build the modwl
    model = Doc2Vec(taggeddocs, dm =0, alpha=0.025, vector_size=20, min_alpha=0.025, min_count=0)

    model.train(taggeddocs, epochs=model.iter, total_examples=model.corpus_count)
    #print ("FF",len(text1),len(text2))
    similarity = model.n_similarity(text1, text2)
    return similarity

def calcThreshold(allAbstracts):
    sim_lst = []
    for cnt,(url,abstract) in enumerate(allAbstracts):
        #print (len(abstract))
        text1 = preprocessing(abstract)
        text2 = preprocessing(text)
        #print ("ssF",len(text1),len(text2))
        if(not len(text1)):
            continue
        similarity = simDoc(text1, text2)
        #print("Simi", similarity)
        sim_lst.append(similarity)
        #print("List", sim_lst)
        threshold = np.mean(sim_lst)
    return threshold

def main(text):
    instances = getInstances(text)
    finalList = []
    for instance in instances:
        #Add Code for iterating through patterns and clues here
        cluesPatternsTuple = getCluesPatternsTuple()
        
        hits = {}
        for c,(pattern,clue,order) in enumerate(cluesPatternsTuple):
            #print(list(enumerate(cluesPatternsTuple)))
            # 0 is such as, 1 is especially, 2 is including...
            #print(clue)#'such as' for first iteration
            #print(order)
            if(order=="first"):
                clue_i = clue+instance
            else:
                clue_i = instance+clue

            #print(clue_i)#such as Pizza Base
            
            (number, allAbstracts) = getAbstracts(clue_i,20)
            # print ("Allll", allAbstracts)
            for (url,abstract) in allAbstracts:
                filename = ''.join(e for e in url if e.isalnum())
                #f = open(filename[:15]+".txt","w+")
                f = open(filename+".txt","w+", encoding = 'utf-8')
                f.write(abstract)
                f.close()

            threshold = calcThreshold(allAbstracts)
            print("Threshold is ", threshold)

            #for sentence in abstract.split('.'):
            #    if list(set("Secret") & set(sentence.split(' '))):
            #        print("Sent", sentence)

            for cnt,(url,abstract) in enumerate(allAbstracts):
                #print (len(abstract))
                text1 = preprocessing(abstract)
                text2 = preprocessing(text)
                #print ("ssF",len(text1),len(text2))
                if(not len(text1)):
                    continue
                similarity = simDoc(text1, text2)
                print("Simi", similarity)

                if similarity>threshold:
                    print (c,"::",cnt,":",url)
                    concepts = getConcepts(abstract)
                    #print(concepts)
                    conceptRegex = "|".join(concepts)
                    conceptRegex = conceptRegex.replace(".","\.").replace("*","\*").replace("+","\+").replace("[","\[").replace("]","\]").replace("{","\{").replace("}","\}").replace("^","\^").replace("$","\$").replace("(","\(").replace(")","\)").replace("?","\?").replace("-","\-")
                    
                    print("Pattern", pattern)
                    pattern_str = ''.join(pattern) #changing pattern list to a string
                    #print(pattern_str)
                    '''match = re.findall(clue, abstract)
                    print("Matchhh", match)
                    if(match):
                        if match[0] in hits:
                            hits[match[0]] += 1
                        else:
                            hits[match[0]] = 1
                    
                    print("Yayy", hits[match[0]])

                    '''
                    p = [clue]
                    concept_lst = []
                    sent_tokenize_list = nltk.sent_tokenize(abstract)    
                    for sentence in sent_tokenize_list:
                        for word in p:
                            if word in sentence:
                                #this is sentence with match
                                #match =  sentence
                                print("Sentence:  ", sentence)
                                word_tokenize_list = nltk.word_tokenize(sentence)
                                print("hhh", word_tokenize_list)
                                #concepts = ' '.join(concepts) #converting from list to string
                                for sent in word_tokenize_list:
                                    for con in concepts:
                                        if con in sentence:
                                            print("these concepts", con)
                                            concept_lst.append(con)
        #max_hits = max(concept_lst, key=concept_lst.count)
        #print(max_hits)

        most_common = Counter(concept_lst).most_common(1)[0]
        print("Yayyy", most_common)

        finalList.append((most_common,instance))
    print(finalList)
    return instances
        
    '''tempPattern = pattern[:]
                    concept_idx = [idx for idx,i in enumerate(tempPattern) if "CONCEPT" in i][0]
                    tempPattern[concept_idx] = tempPattern[concept_idx].replace("CONCEPT",conceptRegex)

                    instance_idx = [idx for idx,i in enumerate(tempPattern) if "INSTANCE" in i][0]
                    tempPattern[instance_idx] = tempPattern[instance_idx].replace("INSTANCE",instance)

                    regex = " \?".join(tempPattern)
                    print("Regex", regex)
                    try:
                        match = re.findall(regex,abstract)
                        print("Match", match)
                    except:
                        print (regex,abstract,url)
                    if(match):
                        if match[0] in hits:
                            hits[match[0]] += 1
                        else:
                            hits[match[0]] = 1
        
        concept = max(hits.items(), key=operator.itemgetter(1))[0]
        finalList.append((concept,instance))
        '''
        #Uncomment the line below. clue[i] represents the query, ie. the clue for the ith Instance
        #number, texts = getAbstracts(clue[i])

        #Insert Code for doc2Vec over here and similarity
    #print (finalList)
    #return instances

# text = URLInput()
#text = DocInput()
text = "Pepperoni_Pizza"
#threshold = 0.1
main(text)
