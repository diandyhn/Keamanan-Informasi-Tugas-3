import random
from sympy import isprime

class RSA:
    def __init__(self):
        self.p = self.generate_prime()
        self.q = self.generate_prime()
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.find_coprime(self.phi)
        self.d = self.mod_inverse(self.e, self.phi)

    def generate_prime(self):
        while True:
            num = random.randint(100, 200)  # Random number between 100 and 200
            if isprime(num):
                return num

    def find_coprime(self, phi):
        e = 2
        while e < phi:
            if self.gcd(e, phi) == 1:
                return e
            e += 1
        return None

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def mod_inverse(self, a, m):
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += m0
        return x1

    def encrypt(self, plaintext):
        plaintext = int.from_bytes(plaintext.encode(), 'big')
        ciphertext = pow(plaintext, self.e, self.n)
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = pow(ciphertext, self.d, self.n)
        return plaintext.to_bytes((plaintext.bit_length() + 7) // 8, 'big').decode()

    def get_public_key(self):
        return (self.e, self.n)

    def get_private_key(self):
        return (self.d, self.n)
