"""
Scoring and Evaluation Rules for CaseZero.
Calculates verdict score based on DSA deduction accuracy and AP efficiency.
"""

def calculate_verdict(culprit_guess: str, accomplice_guess: str,
                      actual_culprit: str, actual_accomplice: str,
                      contradiction_debunked: bool, remaining_ap: int) -> dict:
    """
    Computes final case score and detective rank:
    - Culprit correct: 500 points
    - Accomplice correct: 250 points
    - Contradiction debunked: 250 points
    - Remaining AP: remaining_ap * 50 points
    - Score >= 1000 earns 'Master Algorithmic Sleuth (O(1) Precision)'
    """
    is_culprit_correct = (culprit_guess == actual_culprit)
    is_accomplice_correct = (
        bool(actual_accomplice) and (accomplice_guess == actual_accomplice)
    )

    score = 0
    if is_culprit_correct:
        score += 500
    if is_accomplice_correct:
        score += 250
    if contradiction_debunked:
        score += 250

    # AP efficiency bonus awarded only if culprit was correctly identified
    ap_bonus = remaining_ap * 50 if is_culprit_correct else 0
    score += ap_bonus

    is_solved = is_culprit_correct

    if score >= 1000:
        rank = "Master Algorithmic Sleuth (O(1) Precision)"
    elif score >= 750:
        rank = "Senior Forensic Analyst"
    elif score >= 500:
        rank = "Junior Detective"
    else:
        rank = "Cadet Investigator"

    return {
        "is_solved": is_solved,
        "is_culprit_correct": is_culprit_correct,
        "is_accomplice_correct": is_accomplice_correct,
        "is_contradiction_debunked": contradiction_debunked,
        "score": score,
        "ap_bonus": ap_bonus,
        "rank": rank,
        "actual_culprit": actual_culprit,
        "actual_accomplice": actual_accomplice
    }
