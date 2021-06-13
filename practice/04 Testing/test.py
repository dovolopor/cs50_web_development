from unittest.main import main
from prime import isPrime
import unittest

class PrimeTest(unittest.TestCase):

    def test_1(self):
            """Checking if 1 is prime"""
            self.assertFalse(isPrime(1))

    def test_2(self):
            """Checking if 2 is prime"""
            self.assertTrue(isPrime(2))

    def test_3(self):
            """Checking if 3 is prime"""
            self.assertTrue(isPrime(3))

    def test_7(self):
            """Checking if 7 is prime"""
            self.assertTrue(isPrime(7))

    def test_9(self):
            """Checking if 9 is prime"""
            self.assertFalse(isPrime(9))

    def test_25(self):
            """Checking if 25 is prime"""
            self.assertFalse(isPrime(25))

    def test_89(self):
            """Checking if 89 is prime"""
            self.assertTrue(isPrime(89))

    def test_91(self):
            """Checking if 91 is prime"""
            self.assertFalse(isPrime(91))

if __name__ == "__main__":
    unittest.main()