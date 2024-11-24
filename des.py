import sys

class DES:
    def __init__(self):
        self.key = "1010101010"  
        self.s0 = [
            [1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 1, 2, 3],
            [2, 3, 0, 1]
        ]
        self.s1 = [
            [0, 2, 1, 3],
            [1, 0, 3, 2],
            [3, 1, 0, 2],
            [2, 3, 1, 0]
        ]
        self.s2 = [
            [2, 1, 0, 3],
            [3, 0, 1, 2],
            [1, 3, 2, 0],
            [0, 2, 3, 1]
        ]
        self.s3 = [
            [3, 0, 1, 2],
            [2, 1, 3, 0],
            [0, 3, 2, 1],
            [1, 2, 0, 3]
        ]
        self.s4 = [
            [0, 3, 2, 1],
            [1, 2, 0, 3],
            [3, 1, 0, 2],
            [2, 0, 3, 1]
        ]
        self.s5 = [
            [1, 2, 3, 0],
            [0, 3, 1, 2],
            [2, 0, 1, 3],
            [3, 1, 2, 0]
        ]
        self.s6 = [
            [3, 1, 2, 0],
            [0, 2, 3, 1],
            [1, 0, 3, 2],
            [2, 3, 0, 1]
        ]
        self.s7 = [
            [2, 3, 0, 1],
            [1, 0, 2, 3],
            [3, 2, 1, 0],
            [0, 1, 3, 2]
        ]

    def getSboxEntry(self, binary, sbox):
        row = binary[0] + binary[3]
        col = binary[1] + binary[2]
        row = int(row, 2)
        col = int(col, 2)
        if sbox == 0:
            binary = bin(self.s0[row][col])[2:]
        elif sbox == 1:
            binary = bin(self.s1[row][col])[2:]
        elif sbox == 2:
            binary = bin(self.s2[row][col])[2:]
        elif sbox == 3:
            binary = bin(self.s3[row][col])[2:]
        elif sbox == 4:
            binary = bin(self.s4[row][col])[2:]
        elif sbox == 5:
            binary = bin(self.s5[row][col])[2:]
        elif sbox == 6:
            binary = bin(self.s6[row][col])[2:]
        elif sbox == 7:
            binary = bin(self.s7[row][col])[2:]
        else:
            raise ValueError("Invalid S-box number")
        return binary.zfill(2)

    def fFunction(self, right, key):
        expansion = right[3] + right[0] + right[1] + right[2] + right[1] + right[2] + right[3] + right[0]
        XOR = bin(int(expansion, 2) ^ int(key, 2))[2:].zfill(8)
        left = XOR[:4]
        right = XOR[4:]
        S0 = self.getSboxEntry(left, 0)
        S1 = self.getSboxEntry(right, 1)
        p4 = S0 + S1
        return p4[1] + p4[3] + p4[2] + p4[0]

    def kValueGenerator(self, key):
        # Generate 16 keys for 16 rounds
        keys = []
        newKey = key[2] + key[4] + key[1] + key[6] + key[3] + key[9] + key[0] + key[8] + key[7] + key[5]
        left, right = newKey[:5], newKey[5:]
        for _ in range(16):
            left = left[1:] + left[0]
            right = right[1:] + right[0]
            combined = left + right
            permuted = combined[5] + combined[2] + combined[6] + combined[3] + combined[7] + combined[4] + combined[9] + combined[8]
            keys.append(permuted)
        return keys

    def initialPermutation(self, key):
        return key[1] + key[5] + key[2] + key[0] + key[3] + key[7] + key[4] + key[6]

    def reversePermutation(self, key):
        return key[3] + key[0] + key[2] + key[4] + key[6] + key[1] + key[7] + key[5]

    def padding(self, string, length):
        return string.zfill(length)

    def Encryption(self, string):
        permString = self.initialPermutation(string)
        left, right = permString[:4], permString[4:]
        keys = self.kValueGenerator(self.key)

        for i in range(16):
            fOutput = self.fFunction(right, keys[i])
            XOR_result = bin(int(left, 2) ^ int(fOutput, 2))[2:].zfill(4)
            left, right = right, XOR_result  # Swap left and right

        output = right + left  # Combine after final swap
        return self.reversePermutation(output)

    def Decryption(self, string):
        permString = self.initialPermutation(string)
        left, right = permString[:4], permString[4:]
        keys = self.kValueGenerator(self.key)

        for i in range(16):
            fOutput = self.fFunction(right, keys[15 - i])  # Use keys in reverse for decryption
            XOR_result = bin(int(left, 2) ^ int(fOutput, 2))[2:].zfill(4)
            left, right = right, XOR_result  # Swap left and right

        output = right + left  # Combine after final swap
        return self.reversePermutation(output)
