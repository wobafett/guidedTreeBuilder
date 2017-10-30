'''
Questions:
'''

'''
To Do:
1) Add tree build to htmlConvert
2) Add GUI
'''

'''
CODE SNIPS
'''

mainheader = '<guided-review xmlns:gk="GateKeeper">\n'

questionsOpen = '  <questions>\n'
questionOpen = '    <question qid="%s">\n'
questionClose = '    </question>\n'
questionsClose = '  </questions>\n\n'

optionOpen = '      <option oid="%s">\n'
optionClose = '      </option>\n'

actionsOpen = '  <actions>\n'
actionOpen = '    <action\n    aid="%s"\n    decision="%s"\n    adminactionid="%s">\n'
actionClose = '    </action>\n'
actionsClose = '  </actions>\n\n'

treesOpen = '  <trees>\n'
treeOpen = '    <tree tid="%s"\n'
askOpen = '      <ask qid="%s">\n'
ifOpen = '        <if oid="%s">\n'
ifClose = '        </if>\n'
askClose = '      </ask>\n'
treeClose = '    </tree>\n'
treesClose = '  </trees>\n'

mainCloser = '  <preview />\n</guided-review>'

'''
TYPES
'''

'''action = {
	"list":[],
	"ids":[],
	"decisions":[],
	"adminIds":[]
}

question = {
	"list":[],
	"ids":[],
	"noOfOptions":[],
	"options":None,
	"opIds":None
}

tree = {
	"ids":[],
	"quactions":{
		"ids":[],
		"options":[]
	}
}'''

'''
TEST TYPES
'''

action = {
	"list":['sue them','feed them'],
	"ids":['st','ft'],
	"decisions":['sue','feed'],
	"adminIds":['123','456']
}

question = {
	"list":['how is bob?','how is sal?'],
	"ids":['hib','his'],
	"noOfOptions":[2,2],
	"options":[['good','bad'],['sweet','tangy']],
	"opIds":[['g','b'],['s','t']]
}

tree = {
	"ids":['t1'],
	"quactions":['hib','his'],
	"options":[['his', 'ft'], ['st', 'ft']]
}

'''
FUNCTIONS
'''

### get number of X
#
# noOfWhat : string : plural thing you want to count, i.e. questions
## return : number : int : the resulting number, initiating as a blank
def getNo(noOfWhat):
	while True:
			try:
				number = int(input("Please enter the number of %s: " % noOfWhat))
				break
			except ValueError:
				print("Please enter a valid number")
	return number

## flesh out things
#
# noOfThing : int : usually number obtained using getNo()
# word : string : singular version of thing you want fleshed out
# thing : object : object containing a space for a list of things, their ids and perhaps more
## return : object : with all the info you gathered
def fleshOut(noOfThing,word,thing):
	i = 0
	j = 0
	while noOfThing > 0:
		questionNo = len(question["list"])
		if (word == "option" and questionNo == 1 and j == 0):
			thing["options"] = [[input("Please enter %s #%s: " % (word,str(i+1)))+'\n']]
			thing["opIds"] = [[input("Please enter an ID for this %s: " % word)]]
			j += 1
		elif (word == "option" and questionNo > 1 and j == 0):
			thing["options"].append([input("Please enter %s #%s: " % (word,str(i+1)))+'\n'])
			thing["opIds"].append([input("Please enter an ID for this %s: " % word)])
			j += 1
		elif (word == "option" and j > 0):
			thing["options"][questionNo-1].append(input("Please enter %s #%s: " % (word,str(i+1)))+'\n')
			thing["opIds"][questionNo-1].append(input("Please enter an ID for this %s: " % word))
			j += 1			
		else:
			thing["list"].append(input("Please enter %s #%s: " % (word,str(i+1))) +'\n')
			thing["ids"].append(input("Please enter an ID for this %s: " % word))
		if word == 'action':
			thing["decisions"].append(input("Please enter a decision for this %s: " % word))
			thing["adminIds"].append(input("Please enter an Admin Action ID for this %s: " % word))
		if word == 'question':
			question["noOfOptions"].append(getNo('options'))
			question["options"] = fleshOut(question["noOfOptions"][i],'option',question)
		noOfThing -= 1
		i += 1
	if (word == "action" or word == "question"):
		return thing
	if (word == "option"):
		return thing["options"]

## flesh out trees
#
# noOfTrees : int : the number of trees desired
# tree : object : the prebuilt tree object
## return : object : with all gathered info - for chaining
def makeTree(noOfTrees,tree):
	i = 0
	done = False
	while noOfTrees > 0:
		i += 1
		tree["ids"].append(input("Please enter an ID for tree #%s: " % (i)))
		noOfTrees -= 1
		j = 0
		while done == False:
			j += 1
			while True:
				try:
					currentQuestion = input("Please input the ID of question #%s of tree #%s.\n(If finished please enter DONE): " % (j,i))
					if currentQuestion.lower() == "done":
						done = True
						break
					questionIndex = question["ids"].index(currentQuestion)
					noOfOptions = question["noOfOptions"][questionIndex]
					tree["quactions"].append(currentQuestion)
					break
				except ValueError:
					print("Please enter a valid question ID (or DONE)")
			k = 0
			optionIndex = 0
			while noOfOptions > 0:
				k += 1
				while True:
					try:
						currentFollowUp = input("Option %s/%s (ID: %s) of question #%s (ID: %s) is %s. Please enter the desired result for this option: " % (k,question["noOfOptions"][questionIndex],question["opIds"][questionIndex][optionIndex],j,question["ids"][questionIndex],question["options"][questionIndex][optionIndex]))
						idExists = question["ids"].index(currentFollowUp)
						break
					except ValueError:
						pass
					try:
						idExists = action["ids"].index(currentFollowUp)
						break
					except ValueError:
						print("Please enter a valid action or question ID!")
				print(k)
				if optionIndex == 0:
					tree["options"].append([currentFollowUp])
				else:
					tree["options"][j-1].append(currentFollowUp)
				optionIndex += 1
				noOfOptions -= 1
	return tree

#compile html
def htmlConvert(noOfQuestions,question,noOfActions,action):

	htmlOut = mainheader+questionsOpen
	qCounter = 0
	while noOfQuestions > 0:
		htmlOut += questionOpen % (question["ids"][qCounter])
		htmlOut += '      '+question["list"][qCounter]
		qSubCounter = 0
		while question["noOfOptions"][qCounter] > 0:
			htmlOut += optionOpen % (question["opIds"][qCounter][qSubCounter]) + '        ' + question["options"][qCounter][qSubCounter] + optionClose
			question["noOfOptions"][qCounter] -= 1
			qSubCounter += 1
		htmlOut += questionClose
		noOfQuestions -= 1
		qCounter += 1
	htmlOut += questionsClose+actionsOpen
	aCounter = 0
	while noOfActions > 0:
		htmlOut += actionOpen % (action["ids"][aCounter],action["decisions"][aCounter],action["adminIds"][aCounter])
		htmlOut += '      '+action["list"][aCounter]
		htmlOut += actionClose
		noOfActions -= 1
		aCounter += 1
	htmlOut += actionsClose
	htmlOut += treesOpen
	tCounter = 0
	'''
	while noOfTrees > 0:
		htmlOut += treeOpen % tree["ids"][tCounter]
		tCounter += 1
		noOfTrees -= 1
		while something > 0:
			htmlOut += askOpen % 
	htmlOut += mainCloser
	'''
	return htmlOut

'''
EXECUTION
'''
'''
# get # of questions
noOfQuestions = getNo('questions')
# flesh out questions
question = fleshOut(noOfQuestions,'question',question)
print(question)

# get # of actions
noOfActions = getNo('actions')
# flesh out actions
action = fleshOut(noOfActions,'action',action)
'''
# get # of trees
noOfTrees = getNo('trees')
# flesh out trees
tree = print(makeTree(noOfTrees,tree))

noOfQuestions = 2
noOfActions = 2

print(htmlConvert(noOfQuestions,question,noOfActions,action))


