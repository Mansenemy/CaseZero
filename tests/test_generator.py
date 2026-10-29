"""
Unit Tests for Procedural Case Generator.
Validates 200 seeds to guarantee every generated case is mathematically solvable,
has exactly one culprit, one accomplice, and one planted contradiction.
"""

import unittest
from game.generator import generate_procedural_case, validate_case

class TestProceduralGenerator(unittest.TestCase):
    def test_200_seeds_solvability(self):
        """
        Tests 200 independent seeds:
        1. validate_case returns True.
        2. Clue text is <= 20 words for all clues.
        3. Tree, graph, suspects, and logs are complete.
        """
        for seed in range(1, 201):
            case = generate_procedural_case(seed=seed)
            self.assertTrue(
                validate_case(case),
                f"Procedural case with seed {seed} failed solvability validation!"
            )
            self.assertEqual(len(case["suspects"]), 6)
            self.assertGreater(len(case["connections"]), 0)
            self.assertGreater(len(case["security_logs"]), 0)

            # Check clue word count
            for c in case["clues"]:
                words = len(c["desc"].split())
                self.assertLessEqual(words, 20, f"Clue {c['id']} in seed {seed} exceeds 20 words")

if __name__ == "__main__":
    unittest.main()
