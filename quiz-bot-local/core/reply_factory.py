
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id)

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


def record_current_answer(answer, current_question_id):
    '''
    Validates and stores the answer for the current question to session.
    '''

    if not answer:
        return False, "Please provide an answer."

    # Here, you can implement additional validation logic if needed.
    # For example, if the current_question_id is out of range or invalid, return an error.
    if current_question_id not in range(len(PYTHON_QUESTION_LIST)):
        return False, "Invalid current_question_id."

    # Assuming the session is a dictionary where you can store user answers.
    # You can customize the session storage as per your requirements (e.g., using a database).
    session = {
    "current_question_id": None,
    "answers": {},
    # Any other session-related data you want to store can be added here.
}

    session["answers"][current_question_id] = answer
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0], 0

    next_question_id = current_question_id + 1
    if next_question_id < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[next_question_id], next_question_id
    else:
        return None, -1

    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    answers = session.get("answers", {})

    total_questions = len(PYTHON_QUESTION_LIST)
    answered_questions = len(answers)

    # Calculate the number of correct answers
    correct_answers = 0
    for question_id, answer in answers.items():
        # Here, you can implement the logic to check if the user's answer is correct.
        # You may compare it with the expected answer or perform any other validation.
        # For example, if the answer is correct:
        # if answer == correct_answers[question_id]:
        #     correct_answers += 1
        pass

    # Calculate the user's score
    score = (correct_answers / total_questions) * 100

    # Create the final result message
    final_response = f"Thank you for answering {answered_questions} out of {total_questions} questions."
    final_response += f" Your score is {score:.2f}%."

    return final_response

    return "dummy result"
