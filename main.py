import spade
from bs4 import BeautifulSoup
import urllib2
import re 
import datetime
from pymongo import MongoClient
import time 

host = "127.0.0.1" 
VimeoID = 129427495 
IdForTwitter = VimeoID 
AId = VimeoID 
# db config
###########
client = MongoClient('localhost', 27017)
db = client.eedb

# Functions:
###########
def createFilm( num): 
        time.sleep(2) 
	entry = db.films.find_one({'id':str(num) })
	if entry is None:
		print 'none' 
		db.films.insert_one({'id':str(num)})
		return 

def createAuthor(num):
        time.sleep(2) 
        entry = db.authors.find_one({'id' : str(num)}) 
	if entry is None:
		print 'New Author' 
		db.authors.insert_one({'id' : str(num)})  

def addAttrToFilm(key , val , num ):
        time.sleep(2) 
	entry = db.films.find_one({'id' : str(num), key : val })
	if entry is None:
		d = db.films.find_one({'id' : str(num)})
		entry = db.films.find_one({'id' : str(num)})
		d[key] = val 
	        db.films.find_and_modify(entry, d )
		print "done addAttrToFilm" 

def addAttrToAuthor(key , val , num ):
        time.sleep(2) 
        entry = db.authors.find_one({'id' : str(num), key : val })
        if entry is None:
                d =  db.authors.find_one({'id' : num})
		td = db.authors.find_one({'id' : num}) 
		d[key] = val
		db.authors.find_and_modify(td, d )

		
	
def insertFilmData( sender, data ):
	print data['vimeoId'] 
	query =  db.films.find( { 'vimeoId' : data['vimeoId']} )
	if query is None:
		films = db.films
   		#film_id = films.count()
  		data['date'] = datetime.datetime.utcnow() 	
  		data['id'] = film_id 
  		films.insert_one(data) 
		print 'One row insert in db..' 
	#else :  updateFilmData() 

def sendMsgToAgent( address , self , msgContent):
	# First, form the receiver AID
        TwiRec = spade.AID.aid(name=address , addresses=["xmpp://" + address ])
        IdForTwitter = self.counter
        # Second, build the message
        self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
        self.msg.setOntology("EagleEyeOntology")        # Set the ontology of the message content
        self.msg.setLanguage("English")           # Set the language of the message content
        self.msg.addReceiver(TwiRec)              # Add the message receiver
        self.msg.setContent(msgContent)              # Set the message content

        # Third, send the message with the "send" method of the agent
        self.myAgent.send(self.msg)




def getAccount( website , url):
	res = urllib2.urlopen(url)
        html = res.read()
	soup = BeautifulSoup(html)
	try:
		reg = '(((http:\/\/|https:\/\/))+|(www\.)?)' + website + '\.com\/(#!\/)?[a-zA-Z0-9_]+'
		res=re.search(reg, html)
		url_res = res.group(0)   
		return url_res 
	except Exception as e:
		return None 

############### Class
class bcolors:
    OKBLUE = '\033[1;36m'
    OKGREEN = '\033[1;32m'
    OKRED = '\033[1;31m'
    ENDC = '\033[0m'


# # Vimeo agent done:
#  1. print Id, author, title 
#  
class VimeoAgent(spade.Agent.Agent):
    class MyBehav(spade.Behaviour.Behaviour):
        def onStart(self):
            print bcolors.OKBLUE + "%s* Starting Vimeo behaviour.." % ("[Vimeo]".ljust(10)) + bcolors.ENDC
            self.counter = VimeoID

        def _process(self):

            try:

#		url = 'http://vimeo.com/' + str(self.counter)
#                res = urllib2.urlopen(url)
#                html = res.read()                
#                soup = BeautifulSoup(html)  
# 
#		print self.counter
#                author = soup.find('a', rel="author")
#		if author is None:
#			self.counter = self.counter + 1 
#			return 				
#		authorID = authorUrl = author['href'] 
#		author = soup.find('a', rel="author").get_text() 
#		createAuthor( authorID) 
#		createFilm(self.counter)	
#		title = soup.title.get_text()
#                print bcolors.OKBLUE + '[%d] %s | %s' % (self.counter, author.ljust(16), title) + bcolors.ENDC
#                
#		addAttrToFilm('title' , title , self.counter )
#		addAttrToFilm('Author name' , author , self.counter )
#
#		authorUrl = 'http://vimeo.com' + authorUrl
#		print authorUrl 
#		addAttrToFilm('Author Link' , authorUrl , self.counter )
#
#		des = soup.find('div', class_="description_wrapper") 
#		VideoDes = soup.find('div', class_="description_wrapper").get_text() 
#		print VideoDes 
#		addAttrToFilm('Description' , VideoDes , self.counter )
#
#		res_author = urllib2.urlopen(authorUrl) 
#		html_author = res_author.read()
#		soup_author = BeautifulSoup(html_author) 
#		des_author = soup_author.find('section', class_="user_bio") 
#		des_author_text = soup_author.find('section', class_="user_bio").get_text() 
#
#		addAttrToAuthor('Description' , des_author_text , authorID)
#		print des_author_text   
#		
#	 	reg = '(((http://|https://))+|(www\.)+)(?!facebook)(?!twitter)[a-z0-9]+(\.(?!facebook)(?!twitter)[a-z0-9]+)+'	
#                website=re.search(reg, des_author_text)
#		website = website.group(0) 
#                print "The website of the author: " +  website
#
#		facebook = getAccount( 'facebook',  url )  
#		if facebook is None: 
#			facebook = getAccount( 'facebook' , authorUrl)  
#               		if facebook is None: 
#                        		facebook = getAccount( 'facebook' , website)  
#
#		twitter = getAccount( 'twitter',  url )
#                if twitter is None:
#                        twitter = getAccount( 'twitter' , authorUrl)  	
#			if twitter is None:
#		                        twitter = getAccount( 'twitter' , website )  
#		addAttrToAuthor('Website' , website , authorID)
#		
		AId = 'AID' 
	         	
		twitter = 'twitter.com/share'
		facebook = 'facebook.com/google'
		if twitter is not None: 
			print "Twitter: " + twitter    
			#addAttrToAuthor('Twitter' , twitter , AId)
			address = "twitteragent@" + host 
        		IdForTwitter = self.counter
                	#AId = authorID
			sendMsgToAgent(address, self, twitter)	

                if facebook is not None: 
			print "Facebook: " + facebook      
			addAttrToAuthor('Facebook' , facebook , AId)
                	address = "fbagent@" + host 
                	IdForTwitter = self.counter
                	#AId = authorID
			sendMsgToAgent(address, self, facebook )
		 	
		self.counter = self.counter + 1
		
            except:
                self.counter = self.counter + 1 
                return 
            # time.sleep(1)

    def _setup(self):
        print bcolors.OKBLUE +  "[Vimeo]".ljust(10) + "** Starting Vimeo Agent.." + bcolors.ENDC
        # b = self.MyBehav()
        # self.addBehaviour(b, None)

class TwitterAgent(spade.Agent.Agent):
        class MyBehav(spade.Behaviour.Behaviour):
                def onStart(self):
                        print bcolors.OKRED + "[Twitter]".ljust(10) + "* Starting Twitter behaviour.." + bcolors.ENDC
                        self.counter = 0

                
        class ReceiveBehav(spade.Behaviour.Behaviour):
        
                def _process(self):
		    while(True):
			 self.msg = None             
                	 # Blocking receive for 10 seconds
                	 self.msg = self._receive(True)
                	 content = self.msg.getContent()
			 self.msg = None   
			
                    	 # Check wether the message arrived
                   	 if content :
                   	     print bcolors.OKRED + 'Twitter found: %s ' % content + bcolors.ENDC
                   	     res = urllib2.urlopen("http://" + content)
                   	     html = res.read()

                   	     soup = BeautifulSoup(html) 
			      
                   	     address = soup.find('span', class_="ProfileHeaderCard-locationText u-dir").get_text()
                  	     print bcolors.OKRED + 'address: %s ' % ( address.ljust(16) ) + bcolors.ENDC
                             twitter_bio = soup.find('p' , class_="ProfileHeaderCard-bio u-dir").get_text() 
          		     print bcolors.OKRED + 'Biography from twitter: %s ' % ( twitter_bio ) + bcolors.ENDC
			     website = soup.find('span', class_="ProfileHeaderCard-urlText u-dir" ).get_text()
                             print bcolors.OKRED + 'Website from twitter: %s ' % ( website ) + bcolors.ENDC
			     if website != None:
				addAttrToAuthor('Website' , website , AId)

			     if address != None:
				addAttrToAuthor('Address' , address , AId)

			     if twitter_bio != None:
				addAttrToAuthor('Biography' , twitter_bio  , AId)
	
			     content = None 

        def _setup(self):
                b = self.MyBehav()
                self.setDefaultBehaviour(b)

		Btemplate = spade.Behaviour.ACLTemplate()
		Btemplate.setOntology("EagleEyeOntology")
		mt = spade.Behaviour.MessageTemplate(Btemplate)
		
		rb = self.ReceiveBehav()
		self.addBehaviour(rb,mt)
                print bcolors.OKRED + "[Twitter]".ljust(10) + "** Starting Twitter Agent.." + bcolors.ENDC

class FBAgent(spade.Agent.Agent):
        class MyBehav(spade.Behaviour.Behaviour):
                def onStart(self):
                        print bcolors.OKGREEN + "[FB]".ljust(10) + "* Starting Facebook behaviour.." + bcolors.ENDC
                        self.counter = 0

        class ReceiveBehav(spade.Behaviour.Behaviour):

                def _process(self):
                    while(True):
                        self.msg = None
                        # Blocking receive for 10 seconds
                        self.msg = self._receive(True)
			content  = self.msg.getContent()
 			self.msg = None 
                        # Check wether the message arrived
                        if content :
                             print bcolors.OKGREEN + 'Facebook found: %s ' % content + bcolors.ENDC
                             content = content + "/info?tab=page_info"
			     res = urllib2.urlopen("https://" + content )
                             html = res.read()
			     m = re.search('<ul class="uiList fbSettingsList _4kg _4ks">(.*?)<\/ul>', html)
			     info = m.group(0) 	 
                             soup = BeautifulSoup(info)
			     for row in soup.find_all('div' , {'class' : "clearfix _2pi4"} ):
				name =  row.find('div', {'class': '_50f8 _50f4'})
				print name 
				value = row.find('div', class_="_4bl9") 
				print value 
				addAttrToAuthor(name , value , AId)
			
			content = None 

        def _setup(self):
                b = self.MyBehav()
		self.setDefaultBehaviour(b)

		Btemplate= spade.Behaviour.ACLTemplate() 
		Btemplate.setOntology("EagleEyeOntology")
		mt = spade.Behaviour.MessageTemplate(Btemplate)
		
		rb = self.ReceiveBehav()
		self.addBehaviour(rb, mt)
                print bcolors.OKGREEN + "[FB]".ljust(10) + "** Starting Facebook Agent.." + bcolors.ENDC

if __name__ == "__main__":
    # # Create the agents ans start them.. 
    vimeo = VimeoAgent("vimeoagent@" + host , "secret")
    twitter = TwitterAgent("twitteragent@" + host , "secret")
    fb = FBAgent("fbagent@" + host , "secret")

    vimeo.start()
    twitter.start()
    fb.start()
    
    # # create vimeo behav which will start scrapping vimeo videos..
    b = vimeo.MyBehav()
    vimeo.addBehaviour(b, None)

