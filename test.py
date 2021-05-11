from live_predictor import make_prediction

def test(test_type):
    questions = ["Who won the game ?", "Who was the coach ?", "What year was the game ?"]
    answers = ["notre dame won the game", "bob davie was the coach", "the game occured in 2000"]

    count = 0
    for question, answer in zip(questions, answers):
        response = make_prediction(question, 50, test_type)
        if response == answer:
            count += 1
        print(response)

    return count/len(questions)

if __name__ == "__main__":
    print(test("deduction"))
