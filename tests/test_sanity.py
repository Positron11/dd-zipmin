import unittest

from dd.ddmin import minimize as ddmin
from dd.zipmin import minimize as zipmin


VARIANTS = {
	"ddmin": ddmin,
	"zipmin": zipmin
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
		self._tt_basic_minimization(
			target="aaaaabaaaa", 
			oracle=lambda s: "b" in s, 
			expected="b"
		)


	def test_reduces_to_required_substring(self):
		self._tt_basic_minimization(
			target="zzzabczzz", 
			oracle=lambda s: "abc" in s, 
			expected="abc"
		)


	def test_always_true_minimizes_to_empty(self):
		self._tt_basic_minimization(
			target="abcdef", 
			oracle=lambda s: True, 
			expected=""
		)


	def test_always_false_keeps_original(self):
		self._tt_basic_minimization(
			target="abcdef", 
			oracle=lambda s: False, 
			expected="abcdef"
		)


	def test_unicode_handling(self):
		self._tt_basic_minimization(
			target="αβγdéfβγ", 
			oracle=lambda s: "dé" in s, 
			expected="dé"
		)


	def test_large_noise_minimizes_to_pattern(self):
		self._tt_basic_minimization(
			target=("x" * 300) + "needle" + ("x" * 400), 
			oracle=lambda s: "needle" in s, 
			expected="needle"
		)


	def test_odd_length_partitions(self):
		self._tt_basic_minimization(
			target=("a" * 17) + "Z" + ("a" * 13), 
			oracle=lambda s: "Z" in s, 
			expected="Z"
		)


	def test_two_required_occurrences(self):
		self._tt_basic_minimization(
			target="bbbbbaaaabbbb", 
			oracle=lambda s: s.count("a") >= 2, 
			expected="aa"
		)


	def test_newline_sequence_required(self):
		self._tt_basic_minimization(
			target="line1\nline2\n\nline4\n", 
			oracle=lambda s: "\n\n" in s, 
			expected="\n\n"
		)


	def test_requires_prefix_and_suffix(self):
		self._tt_basic_minimization(
			target="Axxx--middle--yyyZ", 
			oracle=lambda s: s.startswith("A") and s.endswith("Z"), 
			expected="AZ")

	# ---

	def test_non_contiguous_requirements_minimal(self):
		target = "zzazbzczz"

		def oracle(s: str) -> bool:
			return ("a" in s) and ("c" in s) and (s.find("a") < s.find("c"))

		for name, callback in VARIANTS.items():
			with self.subTest(variant=name):
				result = callback(target, oracle)
				
				self.assertTrue(oracle(result))

				# minimality check: removing any single char should break the property
				self.assertTrue(result)

				for i in range(len(result)):
					self.assertFalse(oracle(result[:i] + result[i + 1 :]))


if __name__ == "__main__":
	unittest.main()
