#main - making bracket
import sys
import parse_data
from predict import GraphSearch

def predict_first_four(bracket, winner_prediction_function):
    #first four matches marked as a single row in bracket in the form <TEAM1>::<TEAM2>
    for i in range(0, len(bracket)):
        row = bracket[i]
        split_row = row.split("::")
        if len(split_row) > 1:
            winner, score = winner_prediction_function(split_row[0], split_row[1])
            print("FIRST FOUR: "+split_row[0]+" VS "+split_row[1])
            print("Winner: "+winner+". Score: "+str(score))
            bracket[i] = winner
    return bracket

if __name__ == "__main__":
    print("getting bracket ...")
    bracket = parse_data.get_bracket()

    print("getting season results ...")
    results = parse_data.get_results()

    print("parsing team names ...")
    invalid_team_names = parse_data.get_invalid_team_names(bracket, results)
    if (len(invalid_team_names)):
        print("INVALID TEAM NAMES IN BRACKET.  Ensure that team names in bracket match the team names in results")
        print("invalid names: ")
        print(invalid_team_names)
        sys.exit(1)

    print("training model ...")
    gs = GraphSearch()
    gs.train(results)

    def prediction_function(team1, team2):
        winner, score = gs.predict_game([team1, team2])
        return winner, score

    print("predicting the first four ...")
    bracket = predict_first_four(bracket, prediction_function)

    print("predicting the tournament ...")
    round_num = 1
    while len(bracket) > 1:
        print("ROUND "+str(round_num))
        i = 0
        next_round = []
        while i<len(bracket):
            team1 = bracket[i]
            team2 = bracket[i+1]
            print(team1+" VS "+team2)
            winner, score = prediction_function(team1, team2)
            print("WINNER: "+winner+", "+str(score))
            next_round.append(winner)
            i += 2
        bracket = next_round
        round_num += 1
