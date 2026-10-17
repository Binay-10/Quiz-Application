# Quiz Application – Interactive Python Quiz Engine

An interactive, modular command-line quiz application developed in **Python 3.10+** utilizing only the Python standard library. Designed as a clean, intermediate-level project demonstrating best practices in modular design, data structures, robust input validation, and defensive score calculation.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Python Concepts Demonstrated](#python-concepts-demonstrated)
- [Project Architecture & File Structure](#project-architecture--file-structure)
- [Prerequisites](#prerequisites)
- [Installation & Execution Guide](#installation--execution-guide)
  - [Option A: Running from VS Code](#option-a-running-from-vs-code)
  - [Option B: Running from Terminal / PowerShell](#option-b-running-from-terminal--powershell)
- [Testing & Quality Assurance](#testing--quality-assurance)
- [Sample Console Run](#sample-console-run)
- [GitHub Repository Setup](#github-repository-setup)
- [License](#license)

---

## 🎯 Overview

The **Quiz Application** challenges users on foundational to intermediate Python programming topics through a 10-question multiple-choice quiz engine. The application provides instant feedback, handles whitespace and letter case variations seamlessly, supports an early exit option without data loss, and computes comprehensive scorecards with a strict **70.0%** passing criteria.

---

## ✨ Key Features

- **10-Question Curated Bank**: Stored as a list of dictionaries with 4 distinct options (A, B, C, D) and verified answers covering Python functions, immutability, file extensions, comments, iterables, list methods, exception handling, truthiness, exponentiation, and sets.
- **Case-Insensitive Input**: Accepts lowercase (`a`, `b`, `c`, `d`, `q`) and uppercase (`A`, `B`, `C`, `D`, `Q`) answers seamlessly.
- **Robust Input Validation**: Rejects invalid characters, empty entries, and numbers without penalizing the user or counting them as question attempts.
- **Immediate Feedback Loop**: Instantly informs the user if their choice was correct. If incorrect, displays the exact correct option and text.
- **Early Exit Mechanism (`Q`)**: Users can exit at any point during the quiz; the scorecard dynamically adjusts its denominator to evaluate attempted questions fairly.
- **Zero-Division Immunity**: Gracefully handles zero-attempt exits (e.g., quitting on Question 1) without crashing or throwing `ZeroDivisionError`.
- **Comprehensive Scorecard**:
  - Total Questions in Question Bank
  - Questions Attempted
  - Correct Answers
  - Incorrect Answers
  - Unanswered Questions
  - Final Score Percentage (2 decimal precision)
  - Status: `PASSED (Certificate Eligible)` (>= 70.0%) or `FAILED (Needs Improvement)` (< 70.0%)
  - Tailored motivational feedback based on performance.
- **Zero External Dependencies**: Runs entirely on the Python Standard Library.

---

## 🧠 Python Concepts Demonstrated

| Concept | Implementation Details |
| :--- | :--- |
| **Nested Data Structures** | `list[dict[str, Any]]` structure to model the question bank and option maps. |
| **Modular Functional Design** | Decoupled responsibilities into dedicated functions (`display_welcome`, `display_question`, `get_valid_answer`, `calculate_score`, `display_results`, `run_quiz`). |
| **Input Sanitization** | `raw_input.strip().upper()` with membership testing against allowed sets `{"A", "B", "C", "D", "Q"}`. |
| **Defensive Programming** | Prevention of `ZeroDivisionError` using conditional denominators and safe defaults. |
| **Type Annotations** | Static typing hints (`list`, `dict`, `int`, `float`, `str`, `bool`) for clarity and maintainability. |
| **Clean Console UX** | Formatted ASCII borders, structured alignment, and visual dividers. |

---

## 📁 Project Architecture & File Structure

```text
Quiz-Application/
│
├── quiz_application.py      # Core quiz engine & executable entry point
├── test_quiz_application.py # Comprehensive unit test suite (unittest)
├── sample_run.txt           # Console output transcripts from realistic runs
├── README.md                # Project documentation and user guide
└── .gitignore               # Git ignore rules for Python artifacts
```

### Modular Function Breakdown in `quiz_application.py`

- `display_welcome(total_questions: int, passing_grade: float)`: Displays title banner, total question count, and passing threshold.
- `display_question(index: int, total: int, question_data: dict)`: Renders formatted question text and multiple-choice options.
- `get_valid_answer(prompt: str) -> str`: Loop that reprompts on empty/invalid inputs until valid answer is provided.
- `calculate_score(correct_count, attempted_count, total_questions, quit_early, passing_threshold) -> dict`: Computes statistics, calculates percentages, and determines pass/fail status.
- `display_results(results: dict)`: Prints formatted final scorecard and performance feedback.
- `run_quiz(questions: list[dict] | None)`: Coordinates the overall quiz execution flow.

---

## ⚙️ Prerequisites

- **Python 3.10+** (Python 3.10, 3.11, 3.12, 3.13+)
- Any code editor or terminal (e.g., **VS Code**, Windows Terminal, PowerShell, macOS Terminal, Linux Bash)

---

## 🚀 Installation & Execution Guide

### Option A: Running from VS Code

1. Launch **VS Code**.
2. Open the project folder:
   - Go to `File` > `Open Folder...`
   - Select `Quiz-Application`.
3. Open `quiz_application.py`.
4. Run the application:
   - Click the **Play button** (▶) in the top-right corner of the editor, OR
   - Press <kbd>Ctrl</kbd> + <kbd>F5</kbd> (Run Without Debugging).
5. Interact directly with the quiz inside the integrated VS Code Terminal.

### Option B: Running from Terminal / PowerShell

1. Open your terminal or PowerShell and navigate to the project root:
   ```bash
   cd path/to/Quiz-Application
   ```
2. Verify your Python version:
   ```bash
   python --version
   ```
3. Run the application:
   ```bash
   python quiz_application.py
   ```

---

## 🧪 Testing & Quality Assurance

A dedicated automated test suite is provided in `test_quiz_application.py` verifying:
- 10-question structural integrity (keys, options A-D, answers).
- Lowercase input conversions and whitespace trimming.
- Continuous reprompting on invalid inputs.
- 100% correct score calculation (`PASSED`).
- Boundary score testing at exact 70.0% threshold (`PASSED`).
- Below threshold scores at 60.0% (`FAILED`).
- Early exit calculations where denominator adjusts to attempted questions.
- Zero-attempt exit safety (`ZeroDivisionError` prevention).
- End-to-end simulated interactive session with mocked inputs.

To execute the test suite:
```bash
python -m unittest test_quiz_application.py -v
```

### Test Suite Output:
```text
test_calculate_score_all_correct ... ok
test_calculate_score_below_70_percent_fail ... ok
test_calculate_score_early_quit ... ok
test_calculate_score_exact_70_percent_pass ... ok
test_calculate_score_zero_attempts ... ok
test_get_valid_answer_case_and_whitespace ... ok
test_get_valid_answer_rejects_invalid_inputs ... ok
test_question_bank_structure ... ok
test_run_quiz_full_session_simulation ... ok
test_run_quiz_immediate_quit ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.006s

OK
```

---

## 🖥️ Sample Console Run

```text
============================================================
                 PYTHON KNOWLEDGE QUIZ
============================================================
Total Questions: 10 | Passing Grade: 70%
Instructions   : Enter A, B, C, or D for each question.
                 Enter Q at any prompt to quit the quiz early.
============================================================

Question 1 of 10:
Which keyword is used to create a function in Python?

A) func
B) define
C) def
D) function

Your Answer (A/B/C/D or Q to Quit): c
-> Correct!

...

============================================================
                      [FINAL RESULTS]
============================================================
Quiz Status          : Completed (All Questions Answered)
Total Questions      : 10
Questions Attempted  : 10
Correct Answers      : 8
Incorrect Answers    : 2
Unanswered Questions : 0
Final Score          : 80.00%
Result               : PASSED (Certificate Eligible)
------------------------------------------------------------
Feedback: Congratulations! You demonstrated strong Python proficiency and passed the quiz!
============================================================
```
*(For complete transcripts of early exit, error recovery, and zero-attempt runs, refer to [`sample_run.txt`](sample_run.txt)).*

---

## 🐙 GitHub Repository Setup

To upload this project to a public GitHub repository named **`Quiz-Application`**:

1. Initialize git in the project root:
   ```bash
   git init
   ```
2. Stage and commit all project files:
   ```bash
   git add .
   git commit -m "Initial commit: complete Python quiz engine with tests and docs"
   ```
3. Create a new public repository on GitHub named `Quiz-Application`.
4. Link the remote repository and push:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/Quiz-Application.git
   git push -u origin main
   ```

---

## 📄 License
This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
