#prediction algorithms

class GraphSearch():

	def __init__(self):
		self.graph={}

	def train(self, data):
		self.graph={}
		for row in data:
			self.graph[row['team']]=[]
			self.graph[row['opponent']]=[]
		for row in data:
			if(row['team']!="NA" and row['teamscore']!="NA" and row['oppscore']!='NA'):
				self.graph[row['team']].append((row['opponent'], int(row['teamscore'])-int(row['oppscore'])))
		#print(self.graph)

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
