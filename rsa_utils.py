import random
import math

def is_prime(n, k=5):
    """Miller-Rabin primality test."""
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """Generate a random prime number with the specified number of bits."""
    while True:
        # Generate a random odd number of exactly `bits` bits
        p = random.randint(2**(bits-1), 2**bits - 1) | 1
        if is_prime(p):
            return p

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - ((b // a) * y), y)

def mod_inverse(e, phi):
    """Compute the modular inverse d of e modulo phi."""
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise Exception("Modular inverse does not exist")
    else:
        return x % phi

def generate_keypair(bits=8):
    """
    Generates an RSA keypair.
    Defaults to very small bit sizes (8-16 bits) to keep `n` small enough 
    for classic computer simulation of Shor's period finding algorithm.
    """
    p = generate_prime(bits)
    q = generate_prime(bits)
    while p == q:
        q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that 1 < e < phi and e and phi are coprime.
    e = 65537
    # If e >= phi or gcd is not 1, fallback to a smaller prime
    if e >= phi or gcd(e, phi) != 1:
        # Pick random e
        while True:
            e = random.randrange(2, phi)
            if gcd(e, phi) == 1:
                break

    # Calculate d
    d = mod_inverse(e, phi)

    # Public key is (e, n), Private key is (d, n)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    """Encrypt a plaintext integer to a ciphertext integer."""
    e, n = pk
    return pow(plaintext, e, n)

def decrypt(sk, ciphertext):
    """Decrypt a ciphertext integer back to plaintext integer."""
    d, n = sk
    return pow(ciphertext, d, n)

def string_to_ints(message):
    """Convert a string to a list of integers (ASCII values)."""
    return [ord(c) for c in message]

def ints_to_string(ints):
    """Convert a list of integers back to a string."""
    return "".join(chr(i) for i in ints)

if __name__ == "__main__":
    # Test
    print("Generating keypair (8-bit)...")
    public, private = generate_keypair(8)
    print(f"Public Key: {public}")
    print(f"Private Key: {private}")
    
    msg = "SECRET"
    print(f"\nOriginal Message: {msg}")
    
    encoded = string_to_ints(msg)
    print(f"Encoded integers: {encoded}")
    
    encrypted = [encrypt(public, char) for char in encoded]
    print(f"Encrypted message: {encrypted}")
    
    decrypted = [decrypt(private, char) for char in encrypted]
    print(f"Decrypted integers: {decrypted}")
    
    decoded = ints_to_string(decrypted)
    print(f"Decoded Message: {decoded}")
