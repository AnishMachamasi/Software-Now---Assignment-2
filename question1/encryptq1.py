import time
import os
import random
import string


def shift_char(char, shift, direction):
    if not char.isalpha():
        return char

    base = ord('A') if char.isupper() else ord('a')
    offset = ord(char) - base

    if direction == 'forward':
        new_offset = (offset + shift) % 26
    elif direction == 'backward':
        new_offset = (offset - shift) % 26
    else:
        return char

    return chr(base + new_offset)

def encrypt_text(input_file, output_file, n, m, shift_log_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile, open(shift_log_file, 'w') as log_file:
        for line in infile:
            encrypted_line = ''
            for i, char in enumerate(line):
                if char.isalpha():
                    if i % 2 == 0:
                        shift = n
                        direction = 'forward'
                    else:
                        shift = m
                        direction = 'backward'
                    shifted = shift_char(char, shift, direction)
                    log_file.write(f"Encrypting {char}: {char} -> {shifted} ({direction} by {shift})\n")
                    encrypted_line += shifted
                else:
                    encrypted_line += char
            outfile.write(encrypted_line)

def decrypt_text(input_file, output_file, shift_log_file):
    def decrypt_char(char, shift_value, shift_direction):
        base = ord('A') if char.isupper() else ord('a')
        if shift_direction == 'forward':
            return chr((ord(char) - base - shift_value) % 26 + base)
        elif shift_direction == 'backward':
            return chr((ord(char) - base + shift_value) % 26 + base)
        return char

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile, open(shift_log_file, 'r') as log_file:
        shift_log = [line.strip() for line in log_file if '->' in line and '(' in line]

        shift_idx = 0
        for line in infile:
            decrypted_line = ''
            for char in line:
                if char.isalpha() and shift_idx < len(shift_log):
                    log_line = shift_log[shift_idx]
                    try:
                        left, right = log_line.split(' -> ')
                        _, encrypted_char = left.split('Encrypting ')
                        shifted_char, details = right.split(' (')
                        direction_part, shift_val_str = details.rstrip(')').split(' by ')
                        shift_val = int(shift_val_str)
                        direction = direction_part.strip()

                        decrypted_char = decrypt_char(char, shift_val, direction)
                        decrypted_line += decrypted_char
                        shift_idx += 1
                    except Exception as e:
                        print(f"Skipping malformed line in log: {log_line}")
                        decrypted_line += char
                else:
                    decrypted_line += char
            outfile.write(decrypted_line)

def main():
    n = int(input("Enter value for n: "))
    m = int(input("Enter value for m: "))

    input_file = 'raw_text.txt'
    encrypted_file = 'encrypted_text.txt'
    decrypted_file = 'decrypted_text.txt'
    shift_log_file = 'shift_log.txt'

    encrypt_text(input_file, encrypted_file, n, m, shift_log_file)
    decrypt_text(encrypted_file, decrypted_file, shift_log_file)

    with open(input_file, 'r') as f:
        print("\nContents of raw_text.txt:")
        print(f.read())
    with open(encrypted_file, 'r') as f:
        print("\nContents of encrypted_text.txt:")
        print(f.read())
    with open(decrypted_file, 'r') as f:
        print("\nContents of decrypted_text.txt:")
        print(f.read())


    print("\nVerifying decryption...")
    #function that checks the correctness of decrypted text
    time.sleep(3) #to delay 3 seconds to make it funky to user 
    with open(input_file, 'r') as f1, open(decrypted_file, 'r') as f2:
        if f1.read() == f2.read():
            print("\n Decryption is correct!")
        else:
            print("\n Decryption is incorrect!")

if __name__ == '__main__':
    main()
