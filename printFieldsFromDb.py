from bs4 import BeautifulSoup
import urllib2
import re
import datetime
import json
from pymongo import MongoClient


### Cinfig ## 
client = MongoClient('localhost', 27017)
db = client.eedb
accepted_links = "acc_t"


## end of config ##

## lib >>
def isItLeaf(soup):
        if soup.find(True, recursive=False) is None:
                return True
        else:
                return False

def rcs_htd(soup):
        new_d = {}
        name_of_tag = soup.name
        if isItLeaf(soup):
                #print soup.get_text() 
                return soup.string
        else:
                i = 0;
                new_d['text'] = ''.join(soup.find_all( text=True, recursive=False))

                for child in soup.find_all(re.compile('^((?!script).)*$') , recursive=False):
                        i=i+1
                        #print i
                        #print child
                        #print child.string
                        new_d[child.name+str(i)] =  rcs_htd(child)

                return new_d


def htmlToDict(url):
        res = urllib2.urlopen(url)
        html = res.read()
        soup = BeautifulSoup(html).body
        d= rcs_htd(soup)
        return d



if __name__ == "__main__":
	for element in  db.accepted_links.find_all({ "body" : { "$exists" : True } }):
	
	print "Done, all accepted links has their body attached. \n"


