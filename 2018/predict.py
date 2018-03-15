import csv 
import random
import parsedata as pd
import random
import math
import numpy as np

class GraphSearch():
	
	def __init__(self):
		self.graph={}
		
	def train(self, data):
		self.graph={}
		for row in data:
			self.graph[row['team']]=[]
		for row in data:
			if(row['team']!="NA" and row['teamscore']!="NA" and row['oppscore']!='NA'):
				self.graph[row['team']].append((row['opponent'], int(row['teamscore'])-int(row['oppscore'])))
	
	def graph_search(self, team1, team2, current_score, depth, max_depth=4):
		if(depth>max_depth):
			return None
		scores=[]
		for game in self.graph[team1]:
			if (game[0]==team2):
				scores.append(int(game[1]))
			else:
				score=self.graph_search(game[0], team2, game[1], depth+1, max_depth=max_depth)
				if score!=None:
					scores.append(score)
		if ( not scores):
			return None
		return current_score+sum(scores)/len(scores)
	

	def predict_game(self, game):
		score=self.graph_search(game[0], game[1], 0, 1)
		if score<0:
			winner=game[1]
			score=score*-1
		else:
			winner=game[0]
		return winner, score

	def predict(self, rows):
		predictions=[]
		for r in rows:
			predictions.append(self.predict_game(r))
		return predictions

class Perceptron:

	def __init__(self, attributes):
		self.attributes=attributes
		self.weights=[]
		self.bias=random.uniform(0, 1)
		self.activation=0
		self.output=None
		self._input=None
		for attr in attributes:
			self.weights.append(random.uniform(0, 1))

	def activate(self):
		a=0
		for i in range(0, len(self.weights)):
			a=a+self.weights[i]*self._input[i]
		self.activation=a+self.bias
	
	def update(self, error):
		for i in range(0, len(self.weights)):
			self.weights[i]=self.weights[i]+self._input[i]*error
		self.bias=self.bias+error

	def forward(self, _input):
		self._input=_input
		self.activate()
		if self.activation<0:
			self.output=-1
		else:
			self.output=1

	def train(self, results, iter=1):
		for i in range(0, iter):
			random.shuffle(results)
			for r in results:
				self.forward(r[0])
				if self.output!=r[2]:
					self.update(r[2]-self.output)
		
			

class NNet():
	
	def __init__(self, stat_attributes, numneurons=2):
		self.attributes=list(stat_attributes)

		self.hidden=[]
		for i in range(0, numneurons):
			neuron=[]
			for j in range(0, 2*len(self.attributes)):
				neuron.append(random.uniform(0, 1))
			self.hidden.append(neuron)
		self.olayer=[]
		for i in range(0, numneurons):
			o=[]
			for j in range(0, numneurons):
				o.append(random.uniform(0, 1))
			self.olayer.append(o)
		self.net=[self.hidden, self.olayer]
		self.bias=[[0]*numneurons, [0]*numneurons]
		
	def activate(self, neuron, input, bias):
		a=0
		for i in range(0, len(neuron)):
			a=a+input[i]*neuron[i]
		return a+bias

	def feed_activation(self, a):
		return 1/(1+np.exp(-a))
	
	def derivative(self, output):
		return 1*(1-output)

	def ascent(self, input):
		inputx=input
		forward=[]
		for j in range(0, len(self.net)):
			out=[]
			forward.append(inputx)
			for i in range(0, len(self.net[j])):
				out.append(self.activate(self.net[j][i], inputx, self.bias[j][i]))
			inputx=[]
			for v in out:
				inputx.append(self.feed_activation(v))
			out=inputx
		return forward, out

	def update(self, neuron, error, input):
		for i in range(0, len(neuron)):
			neuron[i]=neuron[i]+error*input[i]*2


	def descent(self, expected, output, forward):
		backerror=[0]*len(self.attributes)
		errors=[]
	#	print(forward)
		for i in range(0, len(output)):
			#print(str(expected[i]))
			#print(str(output[i]))
			errori=(expected[i]-output[i])*self.derivative(output[i])
			errors.append(errori)
			for j in range(0, len(self.net[-1][i])):
				backerror[j]=backerror[j]+self.net[-1][i][j]*errori
			self.update(self.net[-1][i], errori, forward[-1])
			self.bias[-1][i]=self.bias[-1][i]+errori*2
		output=forward[-1]
		#print(output)
		input=forward[0]
		for i in range(0, len(output)):
			error=(backerror[i])*self.derivative(output[i])
			self.update(self.net[0][i], error, input)
			self.bias[0][i]=self.bias[0][i]+error*2
	def format_input(self, team1, team2):
		input=[]
		for attr in self.attributes:
			input.append(pd.teamdata[team1][attr])
		for attr in self.attributes:
			input.append(pd.teamdata[team2][attr])
		return input

	def train(self, results, iter=4):
		training=[]
		errors=[]
		for row in results:
			team1=row['team']
			team2=row['opponent']
			scorediff=int(row['teamscore'])-int(row['oppscore'])
			if scorediff<0:
				expected=[0, 1]
			else:
				expected=[1, 0]
			training.append((team1, team2, expected))
		for i in range(0, iter):
			sumerr=0
			for t in training:
				input=self.format_input(t[0], t[1])
				forward, out=self.ascent(input)
				self.descent(t[2], out, forward)
				if ((out[1]-out[0])*(t[2][1]-t[2][0]))<0:
					sumerr+=1
			errors.append(sumerr)
	
			print(str(self.net))
			print(str(errors))
		#print(str(self.net))
			
	def predict(self, rows):
		predictions=[]
		for r in rows:
			team1=r[0]
			team2=r[1]
			input=self.format_input(team1, team2)
			forward, out=self.ascent(input)
			if out[0]>out[1]:
				predictions.append((team1, out[0]-out[1]))
			else:
				predictions.append((team2, out[1]-out[0]))
		return predictions
		
		

