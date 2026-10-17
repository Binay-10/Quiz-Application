"""
Quiz Application – Interactive Python Quiz Engine
=================================================
A modular, interactive command-line quiz application written in Python 3.10+.
Demonstrates dictionary structures, lists, loops, input validation,
score calculation, and formatted scorecard reporting.
"""

from typing import Any

# ============================================================================
# QUESTION BANK
# ============================================================================
# Stored as a list of dictionaries with question text, 4 options, and correct answer.
QUESTION_BANK: list[dict[str, Any]] = [
    {
        "question": "Which keyword is used to create a function in Python?",
        "options": {
            "A": "func",
            "B": "define",
            "C": "def",
            "D": "function",
        },
        "answer": "C",
    },
    {
        "question": "Which of the following built-in collection types in Python is immutable?",
        "options": {
            "A": "List",
            "B": "Dictionary",
            "C": "Set",
            "D": "Tuple",
        },
        "answer": "D",
    },
    {
        "question": "What is the standard file extension for Python source code files?",
        "options": {
            "A": ".python",
            "B": ".py",
            "C": ".pt",
            "D": ".pyt",
        },
        "answer": "B",
    },
    {
        "question": "Which character is used to denote a single-line comment in Python?",
        "options": {
            "A": "//",
            "B": "/*",
            "C": "#",
            "D": "--",
        },
        "answer": "C",
    },
    {
        "question": "Which built-in function returns the total number of items in an iterable?",
        "options": {
            "A": "count()",
            "B": "size()",
            "C": "length()",
            "D": "len()",
        },
        "answer": "D",
    },
    {
        "question": "Which list method adds a single element to the very end of a list?",
        "options": {
            "A": "append()",
            "B": "add()",
            "C": "insert()",
            "D": "extend()",
        },
        "answer": "A",
    },
    {
        "question": "Which keyword is paired with 'try' to handle errors and exceptions in Python?",
        "options": {
            "A": "catch",
            "B": "except",
            "C": "handle",
            "D": "rescue",
        },
        "answer": "B",
    },
    {
        "question": "What is the evaluated output of the expression bool(0) in Python?",
        "options": {
            "A": "True",
            "B": "False",
            "C": "None",
            "D": "ZeroDivisionError",
        },
        "answer": "B",
    },
    {
        "question": "Which mathematical operator represents exponentiation (power) in Python?",
        "options": {
            "A": "^",
            "B": "**",
            "C": "//",
            "D": "pow",
        },
        "answer": "B",
    },
    {
        "question": "Which data type stores an unordered collection of unique elements?",
        "options": {
            "A": "List",
            "B": "Tuple",
            "C": "Set",
            "D": "Dictionary",
        },
        "answer": "C",
    },
]

PASSING_PERCENTAGE: float = 70.0


# ============================================================================
# MODULAR FUNCTIONS
# ============================================================================

def display_welcome(total_questions: int, passing_grade: float = PASSING_PERCENTAGE) -> None:
    """
    Display a clean, professional console welcome banner and quiz metadata.
    """
    print("\n" + "=" * 60)
    print("                 PYTHON KNOWLEDGE QUIZ")
    print("=" * 60)
    print(f"Total Questions: {total_questions} | Passing Grade: {passing_grade:.0f}%")
    print("Instructions   : Enter A, B, C, or D for each question.")
    print("                 Enter Q at any prompt to quit the quiz early.")
    print("=" * 60 + "\n")


def display_question(index: int, total: int, question_data: dict[str, Any]) -> None:
    """
    Format and display a single question along with its four numbered options.
    """
    print(f"Question {index} of {total}:")
    print(question_data["question"])
    print()
    for opt_key, opt_text in question_data["options"].items():
        print(f"{opt_key}) {opt_text}")
    print()


def get_valid_answer(prompt: str = "Your Answer (A/B/C/D or Q to Quit): ") -> str:
    """
    Prompt the user for input and validate against allowed options (A, B, C, D, Q).
    Handles empty strings, leading/trailing whitespace, and case insensitivity.
    Re-prompts continuously until a valid choice is supplied.
    """
    valid_choices = {"A", "B", "C", "D", "Q"}
    while True:
        try:
            raw_input = input(prompt)
        except (KeyboardInterrupt, EOFError):
            print("\n-> Input interrupted. Exiting quiz session.")
            return "Q"

        cleaned = raw_input.strip().upper()
        if cleaned in valid_choices:
            return cleaned

        print(f"   [!] Invalid input '{raw_input.strip()}'. Please enter A, B, C, D, or Q.\n")


def calculate_score(
    correct_count: int,
    attempted_count: int,
    total_questions: int,
    quit_early: bool,
    passing_threshold: float = PASSING_PERCENTAGE,
) -> dict[str, Any]:
    """
    Calculate the score statistics, percentage, and pass/fail status.

    Percentage calculation:
    - Uses attempted questions as the denominator if the user ended early.
    - Uses all quiz questions if completed normally.
    - Handles zero attempted questions gracefully without division-by-zero.
    """
    incorrect_count = attempted_count - correct_count
    unanswered_count = max(0, total_questions - attempted_count)

    # Denominator depends on whether quiz ended early or completed
    denominator = attempted_count if quit_early else total_questions

    if denominator > 0:
        score_percentage = (correct_count / denominator) * 100.0
    else:
        score_percentage = 0.0

    # Must have attempted at least one question and met/exceeded threshold
    is_passed = (score_percentage >= passing_threshold) and (attempted_count > 0)

    return {
        "total_questions": total_questions,
        "attempted_count": attempted_count,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "unanswered_count": unanswered_count,
        "score_percentage": score_percentage,
        "passing_threshold": passing_threshold,
        "is_passed": is_passed,
        "quit_early": quit_early,
    }


def display_results(results: dict[str, Any]) -> None:
    """
    Print the final scorecard summary, pass/fail status, and feedback messages.
    """
    print("\n" + "=" * 60)
    print("                      [FINAL RESULTS]")
    print("=" * 60)

    if results["quit_early"]:
        if results["attempted_count"] == 0:
            print("Quiz Status          : Ended Early by User (No questions attempted)")
        else:
            print(f"Quiz Status          : Ended Early by User ({results['attempted_count']} attempted)")
    else:
        print("Quiz Status          : Completed (All Questions Answered)")

    print(f"Total Questions      : {results['total_questions']}")
    print(f"Questions Attempted  : {results['attempted_count']}")
    print(f"Correct Answers      : {results['correct_count']}")
    print(f"Incorrect Answers    : {results['incorrect_count']}")
    print(f"Unanswered Questions : {results['unanswered_count']}")
    print(f"Final Score          : {results['score_percentage']:.2f}%")

    if results["attempted_count"] == 0:
        status_text = "INCOMPLETE (No Questions Answered)"
    elif results["is_passed"]:
        status_text = "PASSED (Certificate Eligible)"
    else:
        status_text = "FAILED (Needs Improvement)"

    print(f"Result               : {status_text}")
    print("-" * 60)

    # Congratulatory / encouragement feedback
    if results["attempted_count"] == 0:
        print("Feedback: You exited before answering any questions. Run the quiz again whenever you are ready!")
    elif results["is_passed"]:
        if results["score_percentage"] == 100.0:
            print("Feedback: Outstanding achievement! You achieved a perfect score!")
        else:
            print("Feedback: Congratulations! You demonstrated strong Python proficiency and passed the quiz!")
    else:
        print(f"Feedback: Don't be discouraged! Review the core Python topics and give it another shot (Passing threshold: {results['passing_threshold']:.0f}%).")

    print("=" * 60 + "\n")


def run_quiz(questions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """
    Main controller function to run the interactive quiz loop:
    1. Welcomes user
    2. Iterates questions
    3. Validates answers & provides immediate feedback
    4. Tracks score & early quit
    5. Calculates and renders final scorecard
    """
    if questions is None:
        questions = QUESTION_BANK

    total_questions = len(questions)
    display_welcome(total_questions, PASSING_PERCENTAGE)

    correct_count = 0
    attempted_count = 0
    quit_early = False

    for i, q_data in enumerate(questions, start=1):
        display_question(i, total_questions, q_data)
        user_choice = get_valid_answer()

        if user_choice == "Q":
            quit_early = True
            print("\n-> You chose to quit the quiz early. Computing your interim score...")
            break

        attempted_count += 1
        correct_answer = q_data["answer"].upper()
        correct_text = q_data["options"].get(correct_answer, "")

        if user_choice == correct_answer:
            correct_count += 1
            print("-> Correct!\n")
        else:
            print(f"-> Incorrect! The correct answer was: {correct_answer}) {correct_text}\n")

    results = calculate_score(
        correct_count=correct_count,
        attempted_count=attempted_count,
        total_questions=total_questions,
        quit_early=quit_early,
        passing_threshold=PASSING_PERCENTAGE,
    )

    display_results(results)
    return results


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    run_quiz()
