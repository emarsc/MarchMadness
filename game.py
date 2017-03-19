import csv
import os.path
def calcWinner(team1, team2, depth, difference):
	gameList=[]
	if os.path.isfile('teamData/'+team1+'.txt'):
		with open ('teamData/'+team1+'.txt', 'r') as file:
			lines=file.readlines()
		file.close
	else:
		return None
		print ('teamData/'+team1+'.txt')
	for line in lines:
		array=line.split(',')
		if array[0]==team2:
			gameList.append(difference+int(array[1]))
		elif depth==5:
			return None
		else:
			newValue=calcWinner(array[0], team2, depth+1, difference+int(array[1]))
			if newValue is not None:
				gameList.append(newValue)
	if len(gameList)>0:
		return (sum(gameList)/len(gameList))/depth

def parseCSV():
	import csv
	with open('2017 Game Results Data.csv') as file:
		cr=csv.reader(file)
		for row in cr:
			if row[5]!='Opponent Score':
				difference=int(row[3])-int(row[5])
				with open('teamData/'+row[1]+'.txt', 'a') as file:
					file.write(row[4]+',' +str(difference)+'\n')

def checkBracket():
	import os.path
	import os
	with open ('bracket.txt', 'r') as file:
		print (os.listdir('teamData/'))
		lines=file.read().splitlines()
	for line in lines:
		line.replace(' ', '')
		path='teamData/'+line+'.txt'
		if not os.path.isfile(path):
			print (line)
		else:
			print('checked')


def makeBracket(bracket, depth):
	i=0
	winners=[]
	while i<len(bracket):
		team1=bracket[i]
		i=i+1
		team2=bracket[i]
		i=i+1
		value1=calcWinner(team1, team2, depth, 0)
		value2=calcWinner(team2, team1, depth, 0)
		if value1 is None or value2 is None:
			print (team1+', '+team2)
		if value1>value2:
			winners.append(team1)
			diff=str(value1-value2)
			print(team1+', '+diff)
		else:
			winners.append(team2)
			diff=str(value2-value1)
			print(team2+', '+diff)
	return winners

def tournament():
	with open('bracket.txt') as file:
		bracket=file.read().splitlines()
	t=0
	while t<6:
		temp=makeBracket(bracket, 1)
		print (temp)
		bracket=temp
		t=t+1
