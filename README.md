# AES Crypt ZIP Brute-Force Decryptor

A Python tool to brute-force decrypt AES-encrypted ZIP files (AES Crypt format, e.g., `.zip.aes`) using a wordlist like `rockyou.txt`. Designed for educational purposes, such as CTF challenges (e.g., HackTheBox "Imagery").

## Features
- **Multiprocessing**: Parallel password testing for speed (configurable CPU cores).
- **Validation**: Checks decrypted output for valid ZIP header (`PK\x03\x04`) to confirm success.
- **Cleanup**: Automatically removes temporary files on failure.
- **Progress Tracking**: Optional `tqdm` bar for long wordlists.
- **Error-Resilient**: Handles common issues like invalid passwords or file I/O errors.

## Requirements
- Python 3.6+ (tested on 3.13).
- `pyAesCrypt`: `pip install pyAesCrypt`.
- Optional: `tqdm` for progress bar: `pip install tqdm`.
- Wordlist: Download `rockyou.txt` (e.g., from Kali: `/usr/share/wordlists/rockyou.txt` or [GitHub](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt)).

## Installation
1. Clone the repo:
   ```
   git clone https://github.com/B4l3rI0n/pyAesDecrypt.git
   cd pyAesDecrypt
   ```
2. Install dependencies:
   ```
   pip install pyAesCrypt tqdm
   ```

## Usage
Run the tool directly with command-line arguments (no need to edit the script):

```
python3 aes_bruteforce.py <input_file> <output_file> <wordlist_file> [-p <processes>]
```

- `<input_file>`: Path to the encrypted `.aes` file.
- `<output_file>`: Path for the decrypted output file (e.g., `target.zip`).
- `<wordlist_file>`: Path to the password wordlist (e.g., `rockyou.txt`).
- `-p <processes>`, `--processes <processes>`: Number of parallel processes (default: 4).

Example:
```
python3 aes_bruteforce.py target.zip.aes target.zip /usr/share/wordlists/rockyou.txt -p 4
```

- It loads the wordlist, tests passwords in parallel, and stops on success.
- Example output (on success):
  ```
  🔓 Starting AES Crypt brute-force decryption
  📁 Input file: target.zip.aes
  📤 Output file: target.zip
  📚 Wordlist: /usr/share/wordlists/rockyou.txt (14,344,391 passwords)
  ⚡ Processes: 4
  --------------------------------------------------
  Testing passwords: 100%|██████████| 14,344,391/14,344,391 [05:23<00:00, 44,344.12pw/s]
  
  ✅ CRACKED! Password: 'bestfriends'
  💾 Decrypted file saved: target.zip
  🎉 Decryption complete!
  ```
  <img width="1899" height="360" alt="image" src="https://github.com/user-attachments/assets/aafca8f4-4411-4a00-a7ff-e1fd2c2eabdf" />

- Example output (if not found):
  ```
  ...
  ❌ Password not found in wordlist.
  ```

## Example: Quick Known-Password Decrypt
For testing with a known password (no brute-force):
```python
import pyAesCrypt

input_file = "target.zip.aes"
output_file = "target.zip"
password = "your_known_password"
buffer_size = 64 * 1024

pyAesCrypt.decryptFile(input_file, output_file, password, buffer_size)
print(f"Decrypted: {output_file}")
```

## Limitations
- Only for AES Crypt v2 (ZIP/TAR archives).
- Brute-force is dictionary-only; not for strong/random passwords.
- No GPU acceleration (CPU-bound).

## Credits
- Inspired by CTF challenges like HTB "Imagery".
