import parsedata as pd
from predict import GraphSearch
from predict import Perceptron
import random

bracket=pd.get_bracket()

data=pd.get_result_data()

gs=GraphSearch()
gs.train(data)

#perc=Perceptron(list(pd.teamdata['Purdue'].keys()))

"""parsedresults=[]
for d in data:
	if int(d['teamscore'])-int(d['oppscore'])<0:
		expected=-1
	else:
		expected=1
	_input=[]
	for attr in perc.attributes:
		_input.append(pd.teamdata[d['team']][attr]-pd.teamdata[d['opponent']][attr])
	parsedresults.append((_input, expected))

perc.train(parsedresults, iter=2)
loss=0
random.shuffle(parsedresults)
for i in range(0, 100):
	r=parsedresults[i]
	perc.forward(r[0])
	if perc.output!=r[1]:
		loss+=1
print(str(loss/100))
matches=[]"""

for i in range(0, 7):
	next_round=[]
	print("ROUND: "+str(i))
	j=0
	while j<len(bracket)-1:
		team1=bracket[j]
		j+=1
		team2=bracket[j]
		j+=1
		#_input=[]
		#for attr in perc.attributes:
		#	_input.append(pd.teamdata[team1][attr]-pd.teamdata[team2][attr])
		
		winner, score=gs.predict_game((team1, team2))
		#perc.forward(_input)
		#if perc.output==-1:
		#	winner=team2
		#else:
		#	winner=team1
		
		print("Winner: "+str(winner))
		next_round.append(winner)
	bracket=next_round[:]
