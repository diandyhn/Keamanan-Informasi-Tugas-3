import des
from time import sleep
import sys

# Konversi dari biner ke teks ASCII
def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

# Konversi dari teks ASCII ke biner
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

# Membagi string biner ke dalam beberapa kelompok 8 bit
def split_into_groups(string, length):
    return [string[i:i + length] for i in range(0, len(string), length)]

# Fungsi enkripsi untuk teks ASCII menjadi biner terenkripsi
def encrypt(message):
    des_instance = des.DES()
    binary_message = text_to_bits(message)
    binary_blocks = split_into_groups(binary_message, 8)

    encrypted_blocks = [des_instance.Encryption(block) for block in binary_blocks]
    final_encrypted_message = "".join(encrypted_blocks)
    return final_encrypted_message

# Fungsi dekripsi untuk biner terenkripsi menjadi teks ASCII
def decrypt(message):
    des_instance = des.DES()
    binary_blocks = split_into_groups(message, 8)

    decrypted_blocks = [des_instance.Decryption(block) for block in binary_blocks]
    decrypted_message = "".join(decrypted_blocks)
    return text_from_bits(decrypted_message)

# Fungsi menampilkan loading bar
def sending():
    print("\nSending ", end="")
    for _ in range(5):
        sleep(0.4)
        print(".", end="")
        sys.stdout.flush()
    print(' SENT')