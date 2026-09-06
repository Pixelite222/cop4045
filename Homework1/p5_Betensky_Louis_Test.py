import unittest
from p5_Betensky_Louis import caesar_cipher, caesar_decipher, letter_frequency


class TestCaesarCipher(unittest.TestCase):

    def test_caesar_cipher(self):
        self.assertEqual(caesar_cipher("Hello", 3), "Khoor")
        self.assertEqual(caesar_cipher("Hello, World!", 3), "Khoor, Zruog!")
        self.assertEqual(caesar_cipher("ABC XYZ", 2), "CDE ZAB")

    def test_caesar_decipher(self):
        self.assertEqual(caesar_decipher("Khoor", 3), "Hello")
        self.assertEqual(caesar_decipher("Khoor, Zruog!", 3), "Hello, World!")
        self.assertEqual(caesar_decipher("CDE ZAB", 2), "ABC XYZ")

    def test_letter_frequency(self):
        self.assertEqual(
            letter_frequency("Hello"),
            {"h": 1, "e": 1, "l": 2, "o": 1}
        )

        self.assertEqual(
            letter_frequency("Hello, World!"),
            {"h": 1, "e": 1, "l": 3, "o": 2, "w": 1, "r": 1, "d": 1}
        )

        self.assertEqual(
            letter_frequency("AaBbCc! 123"),
            {"a": 2, "b": 2, "c": 2}
        )


if __name__ == "__main__":
    unittest.main()