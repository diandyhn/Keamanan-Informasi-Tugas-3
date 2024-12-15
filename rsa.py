import random
from sympy import isprime

class RSA:
    def __init__(self, key_size=1024):
        self.p = self.generate_prime(key_size // 2)
        self.q = self.generate_prime(key_size // 2)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.find_coprime(self.phi)
        self.d = self.mod_inverse(self.e, self.phi)

    def generate_prime(self, bits):
        while True:
            # Generate a prime number with specified bit length
            num = random.getrandbits(bits)
            # Ensure the number is odd and prime
            if num % 2 != 0 and isprime(num):
                return num

    def find_coprime(self, phi):
        for e in range(3, phi, 2):
            if self.gcd(e, phi) == 1:
                return e
        return None

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def mod_inverse(self, a, m):
        def egcd(a, b):
            if a == 0:
                return (b, 0, 1)
            else:
                g, y, x = egcd(b % a, a)
                return (g, x - (b // a) * y, y)

        g, x, _ = egcd(a, m)
        if g != 1:
            raise Exception('Modular inverse does not exist')
        else:
            return x % m

    def encrypt(self, message, public_key=None):
        # If no public key provided, use own public key
        if public_key is None:
            public_key = (self.e, self.n)
        
        # Convert message to integer
        if isinstance(message, str):
            message = int.from_bytes(message.encode(), 'big')
        
        # Encrypt using provided public key
        return pow(message, public_key[0], public_key[1])

    def decrypt(self, ciphertext, private_key=None):
        # If no private key provided, use own private key
        if private_key is None:
            private_key = (self.d, self.n)
        
        # Decrypt using provided private key
        plaintext = pow(ciphertext, private_key[0], private_key[1])
        
        # Convert back to bytes/string
        try:
            return plaintext.to_bytes((plaintext.bit_length() + 7) // 8, 'big').decode()
        except:
            return str(plaintext)

    def get_public_key(self):
        return (self.e, self.n)

    def get_private_key(self):
        return (self.d, self.n)