
### This file is to generate summaries via our system using the books in the evaluation set

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import sumy

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


# Helper functions

def read_article(file_name):
    file = open(file_name, "r", encoding="UTF-8")
    filedata = file.readlines()
    # print(filedata)
    
    filedata_new = " ".join(filedata)               # join every elements in the list into a single element
    paragraph = filedata_new.replace("\n \n ", ".") # replace newlines between paragraphs by periods(there are usually 2 or 3 newlines between paragraphs, so replace by at least 2 newlines)
    paragraph = paragraph.split(".")                # Split all periods, so we get sentence by sentence
    # print(paragraph)
    
    sentences = []
    for sentence in paragraph:
        sentence = sentence.replace("\n", "") # remove the extra newlines between sentences
        # print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
        
    sentences = [[string for string in sublist if string] for sublist in sentences] # Remove the empty elements in every sentences if any
    sentences = [string for string in sentences if string] # remove empty lists if any
    # sentences.pop() # Drop the last two empty elements
    end=0
    for test in sentences:
        if ('***END' in test) or (('END' in test)&('***' in test)):
            break
        end=end+1

    if end!=len(sentences):
        del sentences[end:]
    
    start=0
    for test in sentences:
        if ('***START' in test )or (('START' in test)&('***' in test)):
            break
        start=start+1
    if start!=len(sentences): 
        del sentences[:start+1]
    
    return sentences


def split(input_book):

    cnt=0
    idx=dict()

    for i in input_book:
        if ('chapter' in map(str.lower, i[:1])) & (len(i)>=2) :
            idx[tuple(i)]=cnt
            
        elif ('chapitre' in map(str.lower, i[:1])) & (len(i)>=2) :
            idx[tuple(i)]=cnt   
            
        elif ('chap' in map(str.lower, i[:1])):
            idx[tuple(i)]=cnt
            
        elif ('section' in map(str.lower, i[:1])):
            idx[tuple(i)]=cnt    

        cnt=cnt+1

    page=sorted(idx.values())
    # print(idx)
    chapter=dict()
    cnt=0
    while cnt <=len(page)-1:

        if cnt!=len(page)-1:
            chapter[cnt+1]=input_book[page[cnt]:page[cnt+1]]

        else:
            chapter[cnt+1]=input_book[page[cnt]:]
        cnt=cnt+1
    return chapter


def chap_string(input_para):
    string=[]
    for tok in input_para:
        string.append(' '.join(tok))
    string='. '.join(string)
    return(string)


def agg_sum(input_sum):
    in_sum=[]
    for sens in input_sum:
        in_sum.append(str(sens))
    in_sum=' '.join(in_sum)
    return(in_sum)




input_path='C:/Users/Owner/Documents/USC/ISE 540/Project/evaluation_all/temp'                      
output_path='C:/Users/Owner/Documents/USC/ISE 540/Project/evaluation_all/temp'               
book_list=os.listdir(input_path) 

book_list


for k in range(len(book_list)):
    book=read_article(input_path+'/'+book_list[k])  #single book
    cur_book=book_list[k]                           #book name 

    print(book_list[k])

    chap=split(book)
    #chap = {}
    if chap =={}:
        point=1
        for page in range(300,len(book),300):
            if (page+300)>len(book):
                chap[point]=book[page-300:page]
                chap[point+1]=book[page:]
            else:
                chap[point]=book[page-300:page]
            point=point+1

    tot_sum=[]

    for i in chap:

        if len(chap[i])>500 :
            tot_sum.append(agg_sum(chap[i][:2]))
            continue

        chap_sum=[]
        for j in chap[i]:
            chap_sum.append(' '.join(j))
        chap_sum=' '.join(chap_sum) 

        data=[chap_sum]
        vectorizer = TfidfVectorizer( )
        vector1 = vectorizer.fit_transform(data)
        tf_sum=sum(vector1.toarray()[0]) 

        tf_len=len(vector1.toarray()[0]) 
        
        parser = PlaintextParser.from_string(chap_string(chap[i]),Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document,4)

        tot_sum.append(agg_sum(summary))

    tot_sum=' '.join(tot_sum)

    # print(tot_sum)
    textfile = open(output_path+'/'+book_list[k]+"_summary.txt", "w", encoding="utf-8")
    textfile.write(tot_sum)
    textfile.close()


