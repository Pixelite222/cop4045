def caesar_cipher(text, shift):
    encrypted = ""

    for char in text:
        if char.isalpha():
            if char.isupper():
                encrypted += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            encrypted += char

    return encrypted


def caesar_decipher(ciphertext, shift):
    decrypted = ""

    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                decrypted += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            decrypted += char

    return decrypted


def letter_frequency(text):
    frequency = {}

    for char in text.lower():
        if char.isalpha():
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1

    return frequency


def main():
    message = ""

    while True:
        print("\n--- Caesar Cipher Menu ---")
        print("1. Enter a message")
        print("2. Encrypt message")
        print("3. Decrypt message")
        print("4. Count letters")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            message = input("Enter your message: ")
            print("Message saved.")

        elif choice == "2":
            if message == "":
                print("Please enter a message first.")
            else:
                shift = int(input("Enter the shift value: "))
                message = caesar_cipher(message, shift)
                print("Encrypted message:", message)

        elif choice == "3":
            if message == "":
                print("Please enter a message first.")
            else:
                shift = int(input("Enter the shift value: "))
                message = caesar_decipher(message, shift)
                print("Decrypted message:", message)

        elif choice == "4":
            if message == "":
                print("Please enter a message first.")
            else:
                frequency = letter_frequency(message)

                print("Letter frequency:")
                for letter in sorted(frequency):
                    print(letter + ":", frequency[letter])

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select an option from 1-5.")


if __name__ == "__main__":
    main()