import sys
from pathlib import Path
import unittest

from dd.ddmin import ddmin


VARIANTS = {
	"ddmin": ddmin,
}


class TestSanity(unittest.TestCase):
	"""Basic sanity checks for all DD variants."""

	def _tt_basic_minimization(self, target, oracle, expected):
		"""Test template: basic minimization."""

		for name, callback in VARIANTS.items():
			with self.subTest(variant=name):
				self.assertEqual(callback(target, oracle), expected)

	# ---

	def test_reduces_to_single_required_char(self):
		self._tt_basic_minimization("aaaaabaaaa", lambda s: "b" in s, "b")


	def test_reduces_to_required_substring(self):
		self._tt_basic_minimization("zzzabczzz", lambda s: "abc" in s, "abc")


	def test_oracle_always_true_minimizes_to_empty(self):
		self._tt_basic_minimization("abcdef", lambda s: True, "")


	def test_oracle_never_true_keeps_original(self):
		self._tt_basic_minimization("abcdef", lambda s: False, "abcdef")


	def test_unicode_handling(self):
		self._tt_basic_minimization("αβγdéfβγ", lambda s: "dé" in s, "dé")

	# ---

	def test_non_contiguous_requirements(self):
		target = "zzazbzczz"

		def oracle(s: str) -> bool:
			return ("a" in s) and ("c" in s) and (s.find("a") < s.find("c"))

		for name, callback in VARIANTS.items():
			with self.subTest(variant=name):
				result = callback(target, oracle)
				
				self.assertTrue(oracle(result))

				# minimality check: removing any single char should break the property
				self.assertTrue(result)  # result not empty

				for i in range(len(result)):
					self.assertFalse(oracle(result[:i] + result[i + 1 :]))


if __name__ == "__main__":
	unittest.main()
