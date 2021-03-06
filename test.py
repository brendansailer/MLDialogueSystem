from live_predictor import Predictor

def test(test_type, questions, answers, context_line, debug):
    predictor = Predictor(test_type) # This is a class which loads the tokenizes and model ONLY once, which speeds up subsequent predictions

    correct = 0
    for question, answer in zip(questions, answers):
        response = predictor.make_prediction(question, context_line, debug)
        if response == answer:
            correct += 1
            print(response + ' == ' + answer)
        else:
            print(response + ' != ' + answer)

    return str((correct/len(questions)) * 100)

if __name__ == "__main__":
    deduction_questions = ["Who won the game ?", "Who was the coach ?", "What year was the game ?", "what was the spread ?"]
    deduction_answers = ["notre dame won the game", "bob davie was the coach", "the game occurred in 2000", "notre dame won by 2 points"]

    regular_questions = ["Who won the game ?", "Who was the coach ?", "What year was the game ?"]
    regular_answers = ["notre dame won the game", "bob davie was the coach", "the game occurred in 2000"]

    print(test("deduction", deduction_questions, deduction_answers, 50, False) + '%')
    print(test("jumbled",  regular_questions, regular_answers, 50, False) + '%')
    print(test("sentence", regular_questions, regular_answers, 50, False) + '%')
    print(test("simple",   regular_questions, regular_answers, 50, False) + '%')
