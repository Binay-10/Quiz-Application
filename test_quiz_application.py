"""
Unit and Integration Test Suite for Quiz Application
===================================================
Verifies all functional criteria and edge cases specified in the project specification:
1. All correct answers (100% score -> PASS)
2. Mixed / incorrect answers (e.g. 50% -> FAIL, 70% -> PASS threshold)
3. Lowercase input handling and whitespace tolerance
4. Invalid option rejection and continuous reprompting
5. Early exit mid-quiz with denominator set to attempted questions
6. Zero-attempt early exit with zero-division safety
7. Exact 70.0% passing threshold boundary testing
"""

import unittest
from unittest.mock import patch
import io
import quiz_application


class TestQuizApplication(unittest.TestCase):

    def setUp(self):
        self.sample_questions = [
            {
                "question": "Sample Question 1",
                "options": {"A": "Opt A", "B": "Opt B", "C": "Opt C", "D": "Opt D"},
                "answer": "A",
            },
            {
                "question": "Sample Question 2",
                "options": {"A": "Opt A", "B": "Opt B", "C": "Opt C", "D": "Opt D"},
                "answer": "B",
            },
            {
                "question": "Sample Question 3",
                "options": {"A": "Opt A", "B": "Opt B", "C": "Opt C", "D": "Opt D"},
                "answer": "C",
            },
            {
                "question": "Sample Question 4",
                "options": {"A": "Opt A", "B": "Opt B", "C": "Opt C", "D": "Opt D"},
                "answer": "D",
            },
        ]

    def test_question_bank_structure(self):
        """Verify the global QUESTION_BANK contains exactly 10 valid questions with 4 options each."""
        self.assertEqual(len(quiz_application.QUESTION_BANK), 10)
        for i, q in enumerate(quiz_application.QUESTION_BANK, start=1):
            self.assertIn("question", q, f"Question {i} missing question text")
            self.assertIn("options", q, f"Question {i} missing options")
            self.assertIn("answer", q, f"Question {i} missing answer")
            options = q["options"]
            self.assertEqual(len(options), 4, f"Question {i} must have exactly 4 options")
            self.assertEqual(list(options.keys()), ["A", "B", "C", "D"])
            self.assertIn(q["answer"], ["A", "B", "C", "D"], f"Question {i} answer must be A, B, C, or D")

    def test_get_valid_answer_case_and_whitespace(self):
        """Test that get_valid_answer accepts lowercase and trims whitespace."""
        with patch("builtins.input", side_effect=["  c  "]):
            answer = quiz_application.get_valid_answer()
            self.assertEqual(answer, "C")

        with patch("builtins.input", side_effect=["b"]):
            answer = quiz_application.get_valid_answer()
            self.assertEqual(answer, "B")

        with patch("builtins.input", side_effect=["q"]):
            answer = quiz_application.get_valid_answer()
            self.assertEqual(answer, "Q")

    def test_get_valid_answer_rejects_invalid_inputs(self):
        """Test that invalid inputs (empty, numbers, out-of-range letters) reprompt until valid."""
        with patch("builtins.input", side_effect=["", "1", "invalid", "E", "A"]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
                answer = quiz_application.get_valid_answer()
                self.assertEqual(answer, "A")
                output = mock_out.getvalue()
                self.assertIn("Invalid input", output)

    def test_calculate_score_all_correct(self):
        """Test score calculation with 10/10 correct answers."""
        res = quiz_application.calculate_score(
            correct_count=10,
            attempted_count=10,
            total_questions=10,
            quit_early=False,
            passing_threshold=70.0,
        )
        self.assertEqual(res["total_questions"], 10)
        self.assertEqual(res["attempted_count"], 10)
        self.assertEqual(res["correct_count"], 10)
        self.assertEqual(res["incorrect_count"], 0)
        self.assertEqual(res["unanswered_count"], 0)
        self.assertAlmostEqual(res["score_percentage"], 100.0)
        self.assertTrue(res["is_passed"])
        self.assertFalse(res["quit_early"])

    def test_calculate_score_exact_70_percent_pass(self):
        """Test boundary condition: exactly 70.0% passes."""
        res = quiz_application.calculate_score(
            correct_count=7,
            attempted_count=10,
            total_questions=10,
            quit_early=False,
            passing_threshold=70.0,
        )
        self.assertAlmostEqual(res["score_percentage"], 70.0)
        self.assertTrue(res["is_passed"])

    def test_calculate_score_below_70_percent_fail(self):
        """Test boundary condition: 69.9% or 6/10 fails."""
        res = quiz_application.calculate_score(
            correct_count=6,
            attempted_count=10,
            total_questions=10,
            quit_early=False,
            passing_threshold=70.0,
        )
        self.assertAlmostEqual(res["score_percentage"], 60.0)
        self.assertFalse(res["is_passed"])

    def test_calculate_score_early_quit(self):
        """
        Test early quit: percentage must use attempted_count as denominator.
        E.g., 3 attempted out of 10, 3 correct -> 100.0% (PASSED).
        """
        res = quiz_application.calculate_score(
            correct_count=3,
            attempted_count=3,
            total_questions=10,
            quit_early=True,
            passing_threshold=70.0,
        )
        self.assertEqual(res["attempted_count"], 3)
        self.assertEqual(res["correct_count"], 3)
        self.assertEqual(res["unanswered_count"], 7)
        self.assertAlmostEqual(res["score_percentage"], 100.0)
        self.assertTrue(res["is_passed"])
        self.assertTrue(res["quit_early"])

    def test_calculate_score_zero_attempts(self):
        """Test zero attempts: must not trigger ZeroDivisionError and should return 0.0% (FAIL)."""
        res = quiz_application.calculate_score(
            correct_count=0,
            attempted_count=0,
            total_questions=10,
            quit_early=True,
            passing_threshold=70.0,
        )
        self.assertEqual(res["attempted_count"], 0)
        self.assertEqual(res["correct_count"], 0)
        self.assertEqual(res["incorrect_count"], 0)
        self.assertEqual(res["unanswered_count"], 10)
        self.assertAlmostEqual(res["score_percentage"], 0.0)
        self.assertFalse(res["is_passed"])

    def test_run_quiz_full_session_simulation(self):
        """Simulate a full 4-question quiz with 3 correct and 1 wrong answer."""
        user_inputs = ["a", "B", "c", "A"]  # Q1=A(correct), Q2=B(correct), Q3=C(correct), Q4=A(wrong, correct is D)
        with patch("builtins.input", side_effect=user_inputs):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
                results = quiz_application.run_quiz(self.sample_questions)
                self.assertEqual(results["attempted_count"], 4)
                self.assertEqual(results["correct_count"], 3)
                self.assertEqual(results["incorrect_count"], 1)
                self.assertAlmostEqual(results["score_percentage"], 75.0)
                self.assertTrue(results["is_passed"])
                output = mock_out.getvalue()
                self.assertIn("-> Correct!", output)
                self.assertIn("-> Incorrect!", output)
                self.assertIn("PASSED", output)

    def test_run_quiz_immediate_quit(self):
        """Simulate immediate quit at Question 1."""
        with patch("builtins.input", side_effect=["q"]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
                results = quiz_application.run_quiz(self.sample_questions)
                self.assertEqual(results["attempted_count"], 0)
                self.assertEqual(results["correct_count"], 0)
                self.assertAlmostEqual(results["score_percentage"], 0.0)
                self.assertFalse(results["is_passed"])
                output = mock_out.getvalue()
                self.assertIn("Ended Early by User", output)


if __name__ == "__main__":
    unittest.main()
