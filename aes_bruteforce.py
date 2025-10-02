import argparse
import pyAesCrypt
import multiprocessing
from multiprocessing import Pool
import os
import sys

def try_password(password):
    temp_output = f"temp_{hash(password) % 10000}.zip"
    try:
        # Decrypt using paths (handles opening files internally)
        pyAesCrypt.decryptFile(input_file, temp_output, password, buffer_size)
        
        # Check if the output is valid (ZIP header exists)
        with open(temp_output, 'rb') as f:
            header = f.read(4)
            if header == b'PK\x03\x04':  # ZIP file signature
                # Rename temp to final output
                os.rename(temp_output, output_file)
                return password
        
        # If invalid, clean up temp file
        os.remove(temp_output)
        return None
    except ValueError:
        # Wrong password
        if os.path.exists(temp_output):
            os.remove(temp_output)
        return None
    except Exception:
        # Handle other errors (e.g., file not found)
        if os.path.exists(temp_output):
            os.remove(temp_output)
        return None
    finally:
        # Ensure cleanup
        if os.path.exists(temp_output):
            try:
                os.remove(temp_output)
            except:
                pass

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="AES Crypt ZIP Brute-Force Decryptor")
    parser.add_argument("input_file", help="Path to the encrypted input file (.aes)")
    parser.add_argument("output_file", help="Path to the decrypted output file")
    parser.add_argument("wordlist_file", help="Path to the password wordlist file")
    parser.add_argument("-p", "--processes", type=int, default=4, help="Number of parallel processes (default: 4)")
    args = parser.parse_args()

    # Global config (for worker function access)
    global input_file, output_file, buffer_size
    input_file = args.input_file
    output_file = args.output_file
    buffer_size = 64 * 1024
    num_processes = args.processes

    # Read wordlist
    try:
        with open(args.wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        if not passwords:
            print("Error: Wordlist is empty.")
            sys.exit(1)
        print(f"🔓 Starting AES Crypt brute-force decryption")
        print(f"📁 Input file: {input_file}")
        print(f"📤 Output file: {output_file}")
        print(f"📚 Wordlist: {args.wordlist_file} ({len(passwords):,} passwords)")
        print(f"⚡ Processes: {num_processes}")
        print("-" * 50)
    except FileNotFoundError:
        print(f"❌ Error: Wordlist file '{args.wordlist_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading wordlist: {e}")
        sys.exit(1)

    # Brute-force with early termination
    successful_pw = None
    pool = Pool(num_processes)
    try:
        # Prepare iterable for progress
        try:
            from tqdm import tqdm
            iterable = tqdm(pool.imap_unordered(try_password, passwords), total=len(passwords), desc="Testing passwords", unit="pw")
        except ImportError:
            iterable = pool.imap_unordered(try_password, passwords)
            print("ℹ️  tqdm not installed; no progress bar (pip install tqdm)")

        for result in iterable:
            if result:
                successful_pw = result
                print(f"\n✅ CRACKED! Password: '{successful_pw}'")
                print(f"💾 Decrypted file saved: {output_file}")
                pool.terminate()
                break
    except KeyboardInterrupt:
        print("\n⏹️  Stopped by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error during cracking: {e}")
    finally:
        pool.close()
        pool.join()

    if not successful_pw:
        print("\n❌ Password not found in wordlist.")
    else:
        print("\n🎉 Decryption complete!")
    sys.exit(0 if successful_pw else 1)
