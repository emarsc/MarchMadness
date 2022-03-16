#parsing data from bracket and results
import csv

BRACKET_FILE_PATH = "bracket.txt"
RESULT_FILE_PATH = "2022_results.csv"

def get_results():
	with open(RESULT_FILE_PATH, 'r') as file:
		cr=csv.DictReader(file)
		data=list(cr)
	file.close()
	good_data=[]
	for row in data:
		if(row['team']=='NA' or row['opponent']=='NA' or row['teamscore']=='NA' or row['oppscore']=='NA'):
			continue
		good_data.append(row)
	del data[:]
	return good_data

def get_invalid_team_names(bracket, results):
	#returning the team names in bracket that are not found in results
	def is_valid_team_name(team_name):
		for row in results:
			if row['team'] == team_name:
				return True
		return False

	invalid_team_names = []
	for row in bracket:
		#... first four matches noted as <TEAM1>::<TEAM2>
		split_row = row.split("::")
		for team_name in split_row:
			if not is_valid_team_name(team_name):
				invalid_team_names.append(team_name)
	return invalid_team_names

def get_bracket():
	with open(BRACKET_FILE_PATH, 'r') as file:
		bracket=file.read()
	file.close()
	bracket=bracket.split('\n')
	bracket.pop(64)
	good_rows = []
	for row in bracket:
		if row != "":
			good_rows.append(row)
	return good_rows
