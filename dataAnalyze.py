def calcWinner(team1, team2, depth, difference)
	if depth>6: 
		return None
	gameList=[]
	with open ('teamData/'+team1+'.txt', 'r') as file:
		lines=file.readlines()
	file.close		
	for line in lines:
		line.split(',')
		if line[3]==team2:
			i=0:
			while i<5:
				gameList.append(difference+(int(line[5])-int(line[6])))/depth
		else:
			oldDif=difference
			difference=difference+(int(line[5])-int(line[6]))
			newValue=calcWinner(line[3], team2, depth+1, difference)
			if newValue is not None:
				if newValue*(int(line[5])-int(line[6])<0:
					gameList.append(0)
				else:
					gameList.append(newValue)
	return avg(gameList)
			
		
		
