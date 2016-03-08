# This script to push all sublinks in given website. 
# Copywrite Wael Almattar (c) 2015
from bs4 import BeautifulSoup
import urllib2
import re
import datetime
from pymongo import MongoClient
import time

##############  Start of Config #######
client = MongoClient('localhost', 27017)
db = client.eedb
website_link = "http://the-camelia.blogspot.de" 	# usually it's link
link_accept = re.compile( r'^{0}\/2015\/[-a-zA-Z0-9@:%_\+.~&//=]*.html$'.format(website_link) )     # usually it's regex
link_rang = re.compile( r'%s[-a-zA-Z0-9#:_\+.~&//=]*'%website_link)   # usually it's regex

# we should have possible links table and accepting links table
possible_links = "rang_t"
accepted_links = "acc_t"


############## End of config ##########



def get_all_links():
	t= data = db.possible_links.find_one({'checked' : 'false'})	
	if data is None:
		return 
	res = urllib2.urlopen(data['link']) 
        html = res.read()                
        soup = BeautifulSoup(html).body  
	for new_link in soup.find_all('a', {'href':True }):
		new_link = new_link['href']
		#print "New links found: %s"%new_link
		if link_accept.match(new_link):
			if db.accepted_links.find_one({ 'link': new_link }) is None:
				db.accepted_links.insert_one( {  'link': new_link } )
				print "Accepted!"
		if link_rang.match(new_link) :
			if db.possible_links.find_one( { 'link': new_link } ) is None:
				db.possible_links.insert_one( {  'link': new_link, 'checked': 'false' } )
				print "In Rang!"
	db.possible_links.update(
		{ '_id': data['_id']} ,
	    	{ '$set' : {'checked' : 'true'}  }
	)

	#print data 
	get_all_links(); 


#### MAIN ######
if __name__ == "__main__":
        print "Welcome to EAGLE EYE get possible links from website.\nCreated by Wael Almattar, All Copyrights reserved(R)."
	if not db.possible_links.find_one( {'link' : website_link} ):
		db.possible_links.insert_one( { 'link' : website_link , 'checked' : 'false'})
	get_all_links();
	print "Done!"

	
