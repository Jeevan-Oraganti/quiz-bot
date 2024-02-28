
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    answers = session.get("answers", [])
    
    answers.append({"question_id": current_question_id, "answer": answer})
    
    session["answers"] = answers
    session.save()
    
    return True, ""



def get_next_question(current_question_id):
    current_index = next((index for index, q in enumerate(PYTHON_QUESTION_LIST) if q["id"] == current_question_id), -1)
    
    if current_index < len(PYTHON_QUESTION_LIST) - 1:
        next_question = PYTHON_QUESTION_LIST[current_index + 1]["question"]
        next_question_id = PYTHON_QUESTION_LIST[current_index + 1]["id"]
        return next_question, next_question_id
    else:
        return None, None



def generate_final_response(session):
    correct_answers = [q["correct_answer"] for q in PYTHON_QUESTION_LIST]
    
    user_answers = session.get("answers", [])
    
    score = sum(1 for ans in user_answers if ans["answer"] == correct_answers[ans["question_id"]])
    
    return f"Quiz completed! Your score is {score}/{len(correct_answers)}."

