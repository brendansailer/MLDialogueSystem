import pandas as pd
import random

random.seed(1337) # Get the same random ints each time so the data doesn't change run to run of the script

# Open each template file
#qFile = open("data/questions.txt","w") # Normal question file
qFile = open("data/questions_deduction.txt","w") # Question file with deduction question
#cFile = open("data/contexts.txt","w") # For context broken up by commas, not in sentence form
#cFile = open("data/contexts_sentence.txt","w") # For context in sentence form, but not jumbled
#cFile = open("data/contexts_jumbled.txt","w") # For context in sentence form and jumbled
cFile = open("data/contexts_deduction.txt","w") # For context with deduction question
#aFile = open("data/answers.txt", "w") # Normal answer file
aFile = open("data/answers_deduction.txt", "w") # Answer file with deduction question

# Create data frame from data file
df = pd.read_csv("data/data.csv")

# Loop for each row in our data
for i in range(0, 245):
    # Get the different column values we need
    season = df.loc[i, "season"]
    coach = df.loc[i, "coach"]
    winner = df.loc[i, "winner"]
    rank = df.loc[i, "rank"]
    conference = df.loc[i, "conference"]
    home_points = df.loc[i, "home_points"]
    away_points = df.loc[i, "away_points"]
    if home_points > away_points:
        difference = home_points - away_points
    else:
        difference = away_points - home_points
    # Randomize what order
    sentence = random.randint(1, 3)
    # Write to each file
    if sentence == 1:
        qFile.writelines(["<s> what year was the game ? </s>\n", 
                    "<s> in what year was the game played ? </s>\n",
                    "<s> tell me the year the game was played . </s>\n",
                    "<s> when was the game ? </s>\n",
                    "<s> when did the game take place ? </s>\n",
                    "<s> when did they play the game ? </s>\n",
                    "<s> which team won ? </s>\n",
                    "<s> who won the game ? </s>\n",
                    "<s> what was the result of the game ? </s>\n",
                    "<s> who had the higher score ? </s>\n",
                    "<s> did Notre Dame win ? </s>\n",
                    "<s> who was the winning team ? </s>\n",
                    "<s> who was the coach ? </s>\n",
                    "<s> tell me who the coach . </s>\n",
                    "<s> what was the name of the coach ? </s>\n",
                    "<s> who coached the team ? </s>\n",
                    "<s> what was the head coach's name ? </s>\n",
                    "<s> who was the team coached by ? </s>\n",
                    # For deduction question file
                    "<s> how much did the winner win by ? </s>\n",
                    "<s> what was the point differential ? </s>\n",
                    "<s> what was the difference in score ? </s>\n",
                    "<s> tell me the point spread . </s>\n",
                    "<s> how much did they win by ? </s>\n",
                    "<s> what was the score difference ? </s>\n"
                    ])
        #for _ in range(0, 18):
        for _ in range(0, 24): # For deduction context
            #cFile.write("<s> " + str(season) + " , " + str(coach) + " , " + str(winner) + " , " + str(rank) + " , " + str(conference) + " </s>\n") # For context broken up by commas, not in sentence form
            #cFile.write("<s> The game was played in " + str(season) + ". The head coach was " + str(coach) + ". The winner of the game was " + str(winner) + ". Notre Dame was ranked " + str(rank) + ". Notre Dame was a part of the " + str(conference) + " conference.</s>\n") # For context in sentence form, but not jumbled
            #cFile.write("<s> The game was played in " + str(season) + ". The head coach was " + str(coach) + ". The winner of the game was " + str(winner) + ". Notre Dame was ranked " + str(rank) + ". Notre Dame was a part of the " + str(conference) + " conference.</s>\n") # For context in sentence form and jumbled
            cFile.write("<s> " + str(season) + " , " + str(coach) + " , " + str(winner) + " , " + str(rank) + " , " + str(conference) + " , " + str(home_points) + " , " + str(away_points) + " </s>\n")# For context with deduction question
        for _ in range(0, 6):
            aFile.write("<s> the game occurred in " + str(season) + " . </s>\n")
        for _ in range(0, 6):
            aFile.write("<s> " + str(winner) + " won the game . </s>\n")
        for _ in range(0, 6):
            aFile.write("<s> " + str(coach) + " was the coach . </s>\n")
        for _ in range(0, 6): # For deduction answer file
            aFile.write("<s> " + str(winner) + " won by " + str(difference) + " points. </s>\n")
    elif sentence == 2:
        qFile.writelines(["<s> what year was the game ? </s>\n", 
                    "<s> in what year was the game played ? </s>\n",
                    "<s> tell me the year the game was played . </s>\n",
                    "<s> when was the game ? </s>\n",
                    "<s> when did the game take place ? </s>\n",
                    "<s> when did they play the game ? </s>\n",
                    "<s> which team won ? </s>\n",
                    "<s> who won the game ? </s>\n",
                    "<s> what was the result of the game ? </s>\n",
                    "<s> who had the higher score ? </s>\n",
                    "<s> did Notre Dame win ? </s>\n",
                    "<s> who was the winning team ? </s>\n",
                    "<s> who was the coach ? </s>\n",
                    "<s> tell me who the coach . </s>\n",
                    "<s> what was the name of the coach ? </s>\n",
                    "<s> who coached the team ? </s>\n",
                    "<s> what was the head coach's name ? </s>\n",
                    "<s> who was the team coached by ? </s>\n",
                    # For deduction question file
                    "<s> how much did the winner win by ? </s>\n",
                    "<s> what was the point differential ? </s>\n",
                    "<s> what was the difference in score ? </s>\n",
                    "<s> tell me the point spread . </s>\n",
                    "<s> how much did they win by ? </s>\n",
                    "<s> what was the score difference ? </s>\n"
                    ])
        #for _ in range(0, 18): 
        for _ in range(0, 24): # For deduction context 
            #cFile.write("<s> " + str(season) + " , " + str(coach) + " , " + str(winner) + " , " + str(rank) + " , " + str(conference) + " </s>\n")
            #cFile.write("<s> The game was played in " + str(season) + ". The head coach was " + str(coach) + ". The winner of the game was " + str(winner) + ". Notre Dame was ranked " + str(rank) + ". Notre Dame was a part of the " + str(conference) + " conference.</s>\n") # For context in sentence form, but not jumbled
            #cFile.write("<s> Notre Dame was ranked " + str(rank) + ". The game was played in " + str(season) + ". The head coach was " + str(coach) + ". The winner of the game was " + str(winner) + ". Notre Dame was a part of the " + str(conference) + " conference.</s>\n") # For context in sentence form and jumbled
            cFile.write("<s> " + str(season) + " , " + str(coach) + " , " + str(winner) + " , " + str(rank) + " , " + str(conference) + " , " + str(home_points) + " , " + str(away_points) + " </s>\n")# For context with deduction question
        for _ in range(0, 6):
            aFile.write("<s> the game occurred in " + str(season) + " . </s>\n")
        for _ in range(0, 6):
            aFile.write("<s> " + str(winner) + " won the game . </s>\n")
        for _ in range(0, 6):
            aFile.write("<s> " + str(coach) + " was the coach . </s>\n")
        for _ in range(0, 6): # For deduction answer file
            aFile.write("<s> " + str(winner) + " won by " + str(difference) + " points. </s>\n")
    elif sentence == 3:
        qFile.writelines(["<s> what year was the game ? </s>\n", 
                    "<s> in what year was the game played ? </s>\n",
                    "<s> tell me the year the game was played . </s>\n",
                    "<s> when was the game ? </s>\n",
                    "<s> when did the game take place ? </s>\n",
                    "<s> when did they play the game ? </s>\n",
                    "<s> which team won ? </s>\n",
                    "<s> who won the game ? </s>\n",
                    "<s> what was the result of the game ? </s>\n",
                    "<s> who had the higher score ? </s>\n",
                    "<s> did Notre Dame win ? </s>\n",
                    "<s> who was the winning team ? </s>\n",
                    "<s> who was the coach ? </s>\n",
                    "<s> tell me who the coach . </s>\n",
                    "<s> what was the name of the coach ? </s>\n",
                    "<s> who coached the team ? </s>\n",
                    "<s> what was the head coach's name ? </s>\n",
                    "<s> who was the team coached by ? </s>\n",
                    # For deduction question file
                    "<s> how much did the winner win by ? </s>\n",
                    "<s> what was the point differential ? </s>\n",
                    "<s> what was the difference in score ? </s>\n",
                    "<s> tell me the point spread . </s>\n",
                    "<s> how much did they win by ? </s>\n",
                    "<s> what was the score difference ? </s>\n"
                    ])
        #for _ in range(0, 18): 
        for _ in range(0, 24): # For deduction context 
            #cFile.write("<s> " + str(season) + " , " + str(coach) + " , " + str(winner) + " , " + str(rank) + " , " + str(conference) + " </s>\n")
            #cFile.write("<s> The game was played in " + str(season) + ". The head coach was " + str(coach) + ". The winner of the game was " + str(winner) + ". Notre Dame was ranked " + str(rank) + ". Notre Dame was a part of the " + str(conference) + " conference.</s>\n") # For context in sentence form, but not jumbled
            #cFile.write("<s> The head coach was " + str(coach) +  ". Notre Dame was ranked " + str(rank) + ". The winner of the game was " + str(winner) + ". The game was played in " + str(season) + ". Notre Dame was a part of the " + str(conference) + " conference.</s>\n") # For context in sentence form and jumbled
            cFile.write("<s> " + str(season) + " , " + str(coach) + " , " + str(winner) + " , " + str(rank) + " , " + str(conference) + " , " + str(home_points) + " , " + str(away_points) + " </s>\n")# For context with deduction question
        for _ in range(0, 6):
            aFile.write("<s> the game occurred in " + str(season) + " . </s>\n")
        for _ in range(0, 6):
            aFile.write("<s> " + str(winner) + " won the game . </s>\n")
        for _ in range(0, 6):
            aFile.write("<s> " + str(coach) + " was the coach . </s>\n")
        for _ in range(0, 6): # For deduction answer file
            aFile.write("<s> " + str(winner) + " won by " + str(difference) + " points. </s>\n")

# Close files  
qFile.close()
cFile.close()
aFile.close()