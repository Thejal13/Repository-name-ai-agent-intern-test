import json
import sys
from pathlib import Path

from app.agent import SupportAgent


BASE_DIR = Path(__file__).resolve().parent.parent
CASES_FILE = BASE_DIR / "evaluation" / "visible-cases.json"


def check_case(case, answer):
    expect = case["expect"]
    text = answer.lower()

    failures = []

    # Required exact phrases
    for phrase in expect.get("must_include", []):
        if phrase.lower() not in text:
            failures.append(f"missing: {phrase}")

    # Required concepts / phrases
    for concept in expect.get("must_include_concepts", []):
        if concept.lower() not in text:
            failures.append(f"missing concept: {concept}")

    # Forbidden content
    for phrase in expect.get("must_not_include", []):
        if phrase.lower() in text:
            failures.append(f"forbidden: {phrase}")

    # Invented information
    for phrase in expect.get("must_not_invent", []):
        if phrase.lower() in text:
            failures.append(f"invented: {phrase}")

    # Prompt injection protection
    for phrase in expect.get("must_not_follow", []):
        if phrase.lower() in text:
            failures.append(f"followed injection: {phrase}")

    # Privacy
    for phrase in expect.get("must_refuse_to_disclose", []):
        if phrase.lower() in text:
            failures.append(f"privacy leak: {phrase}")

    # Missing information request
    for phrase in expect.get("must_ask_for", []):
        if phrase.lower() not in text:
            failures.append(f"did not ask for: {phrase}")

    return failures


def run_case(case):
    agent = SupportAgent()
    messages = case["messages"]

    answer = ""

    for message in messages:
        answer = agent.answer(message["content"])

    failures = check_case(case, answer)

    return answer, failures


def main():
    with open(CASES_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    cases = data["cases"]

    passed = 0

    print("=" * 70)
    print("Aster & Row — Visible Case Evaluation")
    print("=" * 70)

    for case in cases:
        case_id = case["id"]

        try:
            answer, failures = run_case(case)

            if failures:
                print(f"\n❌ FAIL: {case_id}")
                for failure in failures:
                    print(f"   - {failure}")
                print(f"   Answer: {answer}")
            else:
                print(f"✅ PASS: {case_id}")
                passed += 1

        except Exception as error:
            print(f"\n❌ ERROR: {case_id}")
            print(f"   {error}")

    print("\n" + "=" * 70)
    print(f"RESULT: {passed}/{len(cases)} cases passed")
    print("=" * 70)

    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
