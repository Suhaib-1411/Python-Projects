import base64
import json
import os

class CustomCipher:
    """
    Handles the custom encryption and decryption logic.
    Algorithm: 
    1. Bitwise XOR between the plaintext character and a cyclic key.
    2. Byte-level substitution (shifting by a fixed offset).
    3. Base64 encoding to ensure the output is strictly text-based and safe for file storage.
    """
    def __init__(self, key: str = "ENTERPRISE_SECURE_KEY_2026"):
        self.key = key
        self.shift_offset = 12

    def encrypt(self, plaintext: str) -> str:
        if not plaintext:
            return ""
        
        encrypted_bytes = bytearray()
        key_length = len(self.key)
        
        for i, char in enumerate(plaintext):
            # Step 1: XOR operation
            xor_value = ord(char) ^ ord(self.key[i % key_length])
            # Step 2: Shift substitution
            shifted_value = (xor_value + self.shift_offset) % 256
            encrypted_bytes.append(shifted_value)
            
        # Step 3: Base64 Encoding
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decrypt(self, ciphertext: str) -> str:
        if not ciphertext:
            return ""
            
        try:
            # Step 1: Base64 Decoding
            encrypted_bytes = base64.b64decode(ciphertext.encode('utf-8'))
            decrypted_chars = []
            key_length = len(self.key)
            
            for i, byte in enumerate(encrypted_bytes):
                # Step 2: Reverse shift substitution
                unshifted_value = (byte - self.shift_offset) % 256
                # Step 3: Reverse XOR operation
                original_value = unshifted_value ^ ord(self.key[i % key_length])
                decrypted_chars.append(chr(original_value))
                
            return "".join(decrypted_chars)
        except Exception as e:
            raise ValueError("Decryption failed. The data may be corrupted or not properly formatted.")


class EncryptionCLI:
    """
    Manages the Command Line Interface and file operations.
    """
    def __init__(self):
        self.cipher = CustomCipher()
        self.current_plaintext = ""
        self.current_ciphertext = ""

    def display_menu(self):
        print("\n--- Custom Data Encryption & Decryption Tool ---")
        print("1. Encrypt Data")
        print("2. Decrypt Data")
        print("3. Save Encrypted Data to File")
        print("4. Load and Decrypt Data from File")
        print("5. Exit")
        print("------------------------------------------------")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Select an option (1-5): ").strip()

            if choice == '1':
                self._handle_encrypt()
            elif choice == '2':
                self._handle_decrypt()
            elif choice == '3':
                self._handle_save()
            elif choice == '4':
                self._handle_load()
            elif choice == '5':
                print("Exiting application. Goodbye.")
                break
            else:
                print("Error: Invalid choice. Please select a number between 1 and 5.")

    def _handle_encrypt(self):
        data = input("Enter the plain text to encrypt: ")
        if not data.strip():
            print("Error: Input cannot be empty.")
            return
        
        self.current_plaintext = data
        self.current_ciphertext = self.cipher.encrypt(data)
        print("\n[Success] Data encrypted.")
        print(f"Encrypted output: {self.current_ciphertext}")

    def _handle_decrypt(self):
        data = input("Enter the encrypted text to decrypt: ")
        if not data.strip():
            print("Error: Input cannot be empty.")
            return
            
        try:
            decrypted_text = self.cipher.decrypt(data)
            print("\n[Success] Data decrypted.")
            print(f"Original text: {decrypted_text}")
        except ValueError as ve:
            print(f"Error: {ve}")

    def _handle_save(self):
        if not self.current_ciphertext:
            print("Error: No encrypted data available to save. Please encrypt data first.")
            return

        filename = input("Enter filename to save (e.g., data.json): ").strip()
        if not filename.endswith('.json'):
            filename += '.json'

        # Resolve absolute directory path to ensure file saves next to the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)

        payload = {
            "metadata": "Custom Encrypted Payload",
            "ciphertext": self.current_ciphertext
        }

        try:
            with open(file_path, 'w') as file:
                json.dump(payload, file, indent=4)
            print(f"\n[Success] Encrypted data successfully saved to: {file_path}")
        except IOError as e:
            print(f"Error: Failed to write to file. Details: {e}")

    def _handle_load(self):
        filename = input("Enter filename to load (e.g., data.json): ").strip()
        
        # Resolve absolute directory path to ensure file loads from next to the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"Error: File does not exist at {file_path}")
            return

        try:
            with open(file_path, 'r') as file:
                payload = json.load(file)
            
            if "ciphertext" not in payload:
                print("Error: Invalid file format. No ciphertext found.")
                return

            loaded_ciphertext = payload["ciphertext"]
            decrypted_text = self.cipher.decrypt(loaded_ciphertext)
            
            print("\n[Success] Data loaded and decrypted.")
            print(f"Decrypted text: {decrypted_text}")
            
            # Update application state
            self.current_ciphertext = loaded_ciphertext
            self.current_plaintext = decrypted_text

        except json.JSONDecodeError:
            print("Error: File is not a valid JSON document.")
        except ValueError as ve:
            print(f"Error: {ve}")
        except IOError as e:
            print(f"Error: Failed to read file. Details: {e}")

if __name__ == "__main__":
    app = EncryptionCLI()
    app.run()