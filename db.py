from pymongo import MongoClient
import datetime

correntDiary = 0 

# db config
###########
client = MongoClient('localhost', 27017)
db = client.eedb

# dic of actions
###########

actions = { 1:	{ "id":'1', "des":"Insert attribute.", "func" : "insertAttr" },
	    2:	{ "id":"2", "des":"Delete attribute."  , "func" : "delAttr"   },
	    3:	{ "id":"3", "des":"Print attribute." , "func" : "printAttr"  },
	    4:  { "id":"4", "des":"Insert diary." , "func" : "insertDia"  },
            5:  { "id":"5", "des":"Select/print diary." , "func" : "selectDia"  },
            #6:  { "id":"5", "des":"Select/print diary." , "func" : "addAttrDia"  },
	}

def addAttrToDia(diaId):
	printAttr()
	attrId = raw_input("Select attribute id:")
	daAttr = db.attribs.find_one( { 'id':attrId } )
	nameAttr = str(daAttr['name']) 
	body = raw_input(nameAttr+":")
        d = daDiary = db.diary.find_one({'id':str(diaId)})
	daDiary[nameAttr]=body 
	db.diary.findAndModify(d , daDiary )  	
	printDia(diaId)
	
def delAttrFromDia(diaId, attrId):
	pass
	
def printAllDiaries():
	diaries = db.diary.find()
	for d in diaries:
		print "Id: %s, Fact: %s" % (str(d['id']).ljust(4) , d['fact']) 	
def selectDia():
	printAllDiaries()
	diaryId = raw_input("Select diary number:")
	printDia(diaryId)

def printDia(diaId):
	daDiary = db.diary.find_one({'id':str(diaId)})
	print daDiary 
	for k,v in daDiary.iteritems():
			print "%s: %s" % (k , v ) 
	print "\n	 1. Add attribute."
	print "	 2. Remove attribute." 
	print "	 3. Edit attribute."
	print "	 4. Main Menu"

	num = raw_input("what to do:")
	if num == '1':
		addAttrToDia(diaId)
	elif num == '4':
		pass
	#else if num == 2:
	#	delAttrFromDia(diaId, attrId)
	#else:
		
	
def insertDia():
	fact = raw_input("Enter fact for this diary:")
	data = { "date" :  datetime.datetime.utcnow()} 
        data['id'] = (db.diary.find_one(sort=[("id", -1)]) or '1')
        data['fact'] = fact
	correntDiary = data['id'] 
	db.diary.insert_one(data)
	printDia(correntDiary)

		
	
def insertAttr():
	try:
		name = raw_input("name of attribute:")
		attribs = db.attribs 
		data = { "date" :  datetime.datetime.utcnow()} 
		data['id'] = (db.attribs.find_one(sort=[("uid", -1)]) or '1' )
		data['name'] = name 
		attribs.insert_one(data) 
		print "Done."
        except:
                print "error!"

def printAttr():
	attribs = db.attribs
	atts = db.attribs.find()
	for result_object in atts:
	    print "Id: %s Name: %s Date: %s" % (str(result_object['id']).ljust(3),result_object['name'].ljust(20), result_object['date'] ) 


def delAttr():
	try:
		name = raw_input("name of attribute:")
		db.attribs.remove({"name":name})
 		print "Done."
	except:
		print "error!"

if __name__ == "__main__":
	print "Welcome to EAGLE EYE core system.\nCreated by Wael Almattar, All Copyrights reserved(R)."
	while(True):
		# function to print all actions()
		mission = input("Select action please:")
		func = actions[mission]["func"] 
		globals()[func]()
					
	
