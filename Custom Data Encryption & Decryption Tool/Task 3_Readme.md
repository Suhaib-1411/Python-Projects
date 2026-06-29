# Custom Data Encryption & Decryption Tool

## Overview
This application is a command-line interface (CLI) tool designed to securely encrypt and decrypt text data. It implements a custom cryptographic algorithm that goes beyond standard encoding techniques to simulate real-world data protection workflows. It includes features for data transformation, memory state management, and file I/O operations.

## Features
- Custom multi-layered encryption algorithm.
- Reversible decryption logic.
- JSON-based file storage for encrypted payloads.
- Interactive CLI with robust error handling.
- Modular, object-oriented code structure.

## Algorithm Explanation
The tool relies on a `CustomCipher` class that applies a three-step transformation process to ensure the data is not easily readable:

1. **Cyclic XOR Operation:** The algorithm iterates through the plaintext. Each character's Unicode/ASCII integer representation undergoes a Bitwise XOR operation against a corresponding character in a predefined cyclic key (`ENTERPRISE_SECURE_KEY_2026`).
   
2. **Shift Substitution:** The resulting XOR value is shifted by a constant integer offset (12). A modulo operator (`% 256`) is applied to ensure the resulting integer remains within the bounds of a standard byte array.

3. **Base64 Encoding:** The resulting byte array contains non-printable characters. To ensure the encrypted data can be safely stored, transmitted, and read as standard string data, it is encoded into Base64 format.

*Decryption* is achieved by reversing these steps in exact backward order: Base64 decoding, reverse shift substitution, and a secondary XOR operation to restore the original plaintext character.

## Prerequisites
- Python 3.6 or higher.
- No external libraries are required (the application relies solely on standard library modules: `base64`, `json`, `os`).

## Usage
1. Open a terminal or command prompt.
2. Navigate to the directory containing the script.
3. Execute the script:
   ```bash
   python main.py