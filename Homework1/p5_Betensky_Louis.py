def caesar_cipher(text, shift):
    encrypted = ""

    for i in range(len(text)):
        char = text[i]

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

    for i in range(len(ciphertext)):
        char = ciphertext[i]

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

    for i in range(len(text)):
        char = text[i].lower()

        if char.isalpha():
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1

    return frequency

def main():
    message = ""
    shift = 0

    while True:
        print("\n--- Caesar Cipher Menu ---")
        print("1. Enter message")
        print("2. Enter shift value")
        print("3. View ciphered message")
        print("4. View letter frequency")
        print("5. View deciphered message")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            message = input("Enter your message: ")

        elif choice == "2":
            try:
                shift = int(input("Enter the shift value: "))
            except ValueError:
                print("Invalid shift value. Please enter a number.")

        elif choice == "3":
            if message == "":
                print("Please enter a message first.")
            else:
                print("Ciphered message:", caesar_cipher(message, shift))

        elif choice == "4":
            if message == "":
                print("Please enter a message first.")
            else:
                print("Letter frequency:", letter_frequency(message))

        elif choice == "5":
            if message == "":
                print("Please enter a message first.")
            else:
                ciphered_message = caesar_cipher(message, shift)
                print("Deciphered message:", caesar_decipher(ciphered_message, shift))

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main()