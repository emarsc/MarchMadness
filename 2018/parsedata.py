import csv
import urllib
import urllib.request
import difflib

#csv_path="NCAA_Hoops_Results_3_9_2018.csv"
csv_path="2019_results.csv"
file_path="2019/"

def make_bracket():
	with open(csv_path, 'r') as file:
		cr=csv.DictReader(file)
		data=list(cr)
	file.close()
	print("Num Games: "+str(len(data)))
	teams=[]
	for row in data:
		if row['team'] not in teams:
			teams.append(row['team'])
	bracket=[]
	i=1
	while(i<=64):
		team=input("Input Team "+str(i)+": ")
		if team not in teams:
			print("team not found")
			print("Matches:\n"+str(difflib.get_close_matches(team, teams)))
		else:
			i+=1
			bracket.append(team)
	with open(file_path+"bracket.txt", "w+") as file:
		file.writelines(bracket)
	file.close()
	print("Bracket successfully created")

def check_data_row(row):
	if(row['team']=='NA' or row['opponent']=='NA' or row['teamscore']=='NA' or row['oppscore']=='NA'):
		return False
	return True

"""def fix_bracket():
	with open ("bracket.txt", 'r') as file:
		line=file.read()
		print(line)
	file.close()
	characters=list(line)
	print(str(characters))
	with open(csv_path, 'r') as file:
		cr=csv.DictReader(file)
		data=list(cr)
	file.close()
	print("Num Games: "+str(len(data)))
	teams=[]
	for row in data:
		if row['team'] not in teams:
			teams.append(row['team'])
	team_string=""
	new_bracket=""
	for char in characters:
		team_string+=char
		if team_string in teams:
			print(team_string)
			new_bracket+=team_string+"\n"
			team_string=""
	with open("fixed_bracket.txt", "w+") as file:
		file.write(new_bracket)
	file.close()"""

def get_bracket():
	with open(file_path+'bracket.txt', 'r') as file:
		bracket=file.read()
	file.close()
	bracket=bracket.split('\n')
	bracket.pop(64)
	return bracket

	
	
	
"""def score_result_graph(data):
	graph={}
	for row in data:
		graph[row['team']]=[]
	for row in data:
		if(row['team']!="NA" and row['teamscore']!="NA" and row['oppscore']!='NA'):
			graph[row['team']].append((row['opponent'], int(row['teamscore'])-int(row['oppscore'])))	
	return graph"""

def get_result_data():
	with open(file_path+csv_path, 'r') as file:
		cr=csv.DictReader(file)
		data=list(cr)
	file.close()
	goodData=[]
	for row in data:
		if check_data_row(row):
			goodData.append(row)
	del data[:]
	return goodData

def check_teamdata():
	with open('teamdata.csv', 'r') as file:
		teamdata=list(csv.DictReader(file))
	file.close()
	print(teamdata[0])
	teams=[teamdata[i]['School'] for i in range(0, len(teamdata))]
	#bracket=get_bracket()
	resultData=get_result_data()
	resultTeams=[]

	for row in resultData:
		if row['team'] not in resultTeams:
			resultTeams.append(row['team'])
	moddedteamdata=[]
	for i in range(0, len(teamdata)):
		row=teamdata[i]
		school=row['School']
		school=school.replace("State", "St.")
		school=school.replace(" NCAA", "")
	
		while school  not in resultTeams:
			print(school+" not found")
			matches=difflib.get_close_matches(school, resultTeams)
			print("Matches:\n"+str(difflib.get_close_matches(row['School'], resultTeams)))
			school=input("Change School Name: ")
			if school=="Remove":
				break
		if school!="Remove":
			row['school']=school
			moddedteamdata.append(row)
	teamdata=moddedteamdata

	with open('modteamdata.csv', 'w+') as file:
		writer=csv.DictWriter(file, fieldnames=list(teamdata[0].keys()))
		writer.writeheader()
		for line in teamdata:
			writer.writerow(line)
		file.close()

teamdata={}
with open('modteamdata.csv', 'r') as file:
	csvr=csv.DictReader(file)
	for row in csvr:
		for key in list(row.keys()):
			if key=="":
				row.pop(key, None)
			if key=="school":
				row['School']=row['school']
				row.pop('school', None)
			elif key!="" and key!='school' and key!='School':
				#print(row[key])
				row[key]=float(row[key])

		school=row.pop('School', None)
		teamdata[school]=row
	file.close()

print(teamdata['Purdue'])

"""def result_graph_search(team1, team2, current_score, graph, depth, max_depth=4 ):
	if(depth>max_depth):
		return None
	scores=[]
	for game in resultGraph[team1]:
		if (game[0]==team2):
			scores.append(int(game[1]))
		else:
			score=result_graph_search(game[0], team2, game[1], graph, depth+1, max_depth=max_depth)
			if score!=None:
				scores.append(score)
	if ( not scores):
		return None
	return current_score+sum(scores)/len(scores)"""
	
"""def predict_score(team1, team2, graph, method=result_graph_search):
	score = result_graph_search(team1, team2, 0, graph,  1)
	winner=team1
	if (score<0):
		winner=team2
		score=score*-1
	return winner, score"""


def predict_bracket():
	with open(csv_path, 'r') as file:
		cr=csv.DictReader(file)
		data=list(cr)
	file.close()
	graph=score_result_graph(data)
	with open('bracket.txt', 'r') as file:
		bracket=file.read()
	file.close()
	bracket=bracket.split("\n")
	bracket.pop(64)
	next_round=[]
	for i in range(1, 7):
		next_round=[]
		print("ROUND :"+str(i))
		j=0
		while j<len(bracket):
			team1=bracket[j]
			j+=1
			team2=bracket[j]
			j+=1
			winner, score=predict_score(team1, team2, graph)
			next_round.append(winner)
			print(winner+": "+str(score)+'\n')
		bracket=next_round[:]


	
"""def zero_one_loss(function, num_tests=100):
	import random

	avgScoreDiff=0
	losses=0
	with open(csv_path, 'r') as file:
		cr=csv.DictReader(file)
		data=list(cr)
	file.close()
	random.shuffle(data)
	test_data=data[0:100]
	train_data=data[100:len(data)]

	graph=score_result_graph(train_data)

	validTests=0
	for i in range(0, num_tests):
		row=test_data[i]
		if check_data_row(row):
			validTests+=1
			team1=row['team']
			team2=row['opponent']
			winner, score=predict_score(team1, team2, graph, method=function)
			realScore=int(row['teamscore'])-int(row['oppscore'])
			realWinner=team1
			if realScore<0:
				realWinner=team2
				realScore=realScore*-1
			if winner!=realWinner:
				print(team1+", "+team2+", WINNER: "+realWinner+" predicted score: "+str(score)+", real score:" +str(realScore))
				losses+=1
				avgScoreDiff+=score
				avgScoreDiff+=realScore
			else:
				avgScoreDiff+=abs(realScore-score)
			avgScoreDiff+=abs(score-realScore)
	return float(losses/validTests), avgScoreDiff/validTests"""
	
#make_bracket()
#g=score_result_graph()
#print(str(g))
#if __name__=='__main__':
	#s=predict_score("Virginia", "UMBC")
	#print(str(s))
	#predict_bracket()
	#check_teamdata()
