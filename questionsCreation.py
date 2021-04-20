import pandas as pd
import random

# Open each template file
qFile = open("data/questions.txt","w") # Truncate the file if it already exists
cFile = open("data/contexts.txt","w")
aFile = open("data/answers.txt", "w")

# Create data frame from data file
df = pd.read_csv("data/data.csv")

# Loop for each row in our data
for i in range(0, 245):
    # Get the different column values we need
    season = df.loc[i, "season"]
    coach = df.loc[i, "coach"]
    winner = df.loc[i, "winner"]
    # Randomize what order
    sentence = random.randint(1, 3)
    # Write to each file
    if sentence == 1:
        qFile.writelines(["<s> what year was the game ? </s>\n", 
                    "<s> in what year was the game played ? </s>\n",
                    "<s> tell me the year the game was played . </s>\n",
                    "<s> who was the coach ? </s>\n",
                    "<s> tell me who the coach ? </s>\n",
                    "<s> what was the name of the coach? </s>\n",
                    "<s> which team won ? </s>\n",
                    "<s> who won the game ? </s>\n",
                    "<s> what was the result of the game ? </s>\n"])
        for _ in range(0, 9):
            cFile.write("<s> the game occurred in " + str(season) + " . " + str(coach) + " was the coach . " + str(winner) + " won the game . </s>\n")
        for _ in range(0, 3):
            aFile.write("<s> the game occurred in " + str(season) + " . </s>\n")
        for _ in range(0, 3):
            aFile.write("<s> " + str(coach) + " was the coach . </s>\n")
        for _ in range(0, 3):
            aFile.write("<s> " + str(winner) + " won the game . </s>\n")
    elif sentence == 2:
        qFile.writelines(["<s> what year was the game ? </s>\n", 
                    "<s> in what year was the game played ? </s>\n",
                    "<s> tell me the year the game was played . </s>\n",
                    "<s> which team won ? </s>\n",
                    "<s> who won the game ? </s>\n",
                    "<s> what was the result of the game ? </s>\n",
                    "<s> who was the coach ? </s>\n",
                    "<s> tell me who the coach ? </s>\n",
                    "<s> what was the name of the coach? </s>\n"
                    ])
        for _ in range(0, 9):
            cFile.write("<s> the game occurred in " + str(season) + " . " + str(winner) + " won the game . " + str(coach) + " was the coach . </s>\n")
        for _ in range(0, 3):
            aFile.write("<s> the game occurred in " + str(season) + " . </s>\n")
        for _ in range(0, 3):
            aFile.write("<s> " + str(winner) + " won the game . </s>\n")
        for _ in range(0, 3):
            aFile.write("<s> " + str(coach) + " was the coach . </s>\n")
    elif sentence == 3:
        qFile.writelines(["<s> who was the coach ? </s>\n",
                    "<s> tell me who the coach ? </s>\n",
                    "<s> what was the name of the coach? </s>\n",
                    "<s> which team won ? </s>\n",
                    "<s> who won the game ? </s>\n",
                    "<s> what was the result of the game ? </s>\n",
                    "<s> what year was the game ? </s>\n", 
                    "<s> in what year was the game played ? </s>\n",
                    "<s> tell me the year the game was played . </s>\n"])
        for _ in range(0, 9):
            cFile.write("<s> " + str(coach) + " was the coach . the game occurred in " + str(season) + " . " + str(winner) + " won the game . </s>\n")
        for _ in range(0, 3):
            aFile.write("<s> " + str(coach) + " was the coach . </s>\n")
        for _ in range(0, 3):
            aFile.write("<s> the game occurred in " + str(season) + " . </s>\n")
        for _ in range(0, 3):
            aFile.write("<s> " + str(winner) + " won the game . </s>\n")

# Close files  
qFile.close()
cFile.close()
aFile.close()