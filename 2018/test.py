import parsedata as pd
import csv
import random
import predict
from predict import GraphSearch
from predict import NNet
from predict import Perceptron

def zero_one_loss(numTest):
	data=pd.get_result_data()
	random.shuffle(data)
	test=data[0:numTest]
	train=data[numTest:len(data)]
	realWinners=[]
	toPredict=[]
	for row in test:
		toPredict.append((row['team'], row['opponent']))
		score=int(row['teamscore'])-int(row['oppscore'])
		if score<0:
			score=score*-1
			realWinners.append((row['opponent'], score))
		else:
			realWinners.append((row['team'], score))

	gs=GraphSearch()
	gs.train(train)
	gsPredictions=gs.predict(toPredict)
	"""nn=NNet(pd.teamdata['Purdue'].keys())
	nn.train(train)
	nnPredictions=nn.predict(toPredict)"""
	avgScoreDiff=0
	loss=0	
	for i in range(0, numTest):	
		if gsPredictions[i][0]!=realWinners[i][0]:
			avgScoreDiff=avgScoreDiff+gsPredictions[i][1]+realWinners[i][1]
			loss+=1
		else:
			avgScoreDiff+=abs(realWinners[i][1]-gsPredictions[i][1])
				
	print("0/1 Loss: "+str(loss/numTest))
	print("Average Score Difference: "+str(avgScoreDiff/numTest))

def test_perceptron():
	perc=Perceptron(list(pd.teamdata['Purdue'].keys()))
	unparsedResults=pd.get_result_data()
	results=[]
	for r in unparsedResults:
		if(int(r['teamscore'])-int(r['oppscore']))<0:
			outcome=-1
		else:
			outcome=1
		result=[[], int(r['teamscore'])-int(r['oppscore']), outcome]
		for attr in perc.attributes:
			result[0].append(pd.teamdata[r['team']][attr]-pd.teamdata[r['opponent']][attr])
		results.append(result)
	random.shuffle(results)
	test=results[0:100]
	train=results[100:len(results)]
	perc.train(train, iter=2)
	loss=0
	#print(test)
	for i in range(0, 100):
		perc.forward(test[i][0])
		if perc.output!=test[i][2]:
			loss+=1
	print("0/1 Loss: "+str(loss/100))

if __name__=="__main__":
	zero_one_loss(100)	
	#test_perceptron()
