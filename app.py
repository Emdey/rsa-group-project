import streamlit as st
import random
import math
import time


# ==============================================================================
# PART 1: CORE RSA FUNCTIONS (Team Member 1) - Mathematical logic
# ==============================================================================

def gcd(a, b):
    """Computes the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def modInverse(a, m):
    """Computes the modular multiplicative inverse of a modulo m."""
    m0, x0, x1 = m, 0, 1
    if m == 1: return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += m0
    return x1

def miller_rabin_test(n, k=5):
    """Performs the Miller-Rabin primality test."""
    if n <= 3: return n > 1
    if n % 2 == 0: return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def generate_prime(n):
    """Generates a random n-bit prime number."""
    while True:
        # Generate a random n-bit number, ensuring it's not 1 and is odd
        p = random.getrandbits(n)
        if p > 1 and p % 2 != 0 and miller_rabin_test(p):
            return p

def generate_keypair(p, q):
    """Generates the RSA public and private key pair."""
    n = p * q
    phi = (p - 1) * (q - 1)
    # Standard choice for the public exponent e
    e = 65537 
    # Calculate the private exponent d
    d = modInverse(e, phi)
    
    # Public key (e, n), Private key (d, n)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    """Encrypts plaintext message using the public key."""
    e, n = pk
    # Convert each character to its ASCII value and encrypt it
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext

def decrypt(pk, ciphertext):
    """Decrypts ciphertext using the private key."""
    d, n = pk
    # Decrypt each integer and convert back to a character
    decrypted_chars = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(decrypted_chars)


# --- 2. STREAMLIT CONFIGURATION ---
st.set_page_config(page_title="Secure RSA Vault", page_icon="🛡️", layout="wide")
st.title("🛡️ RSA Vault: Cryptography")
st.markdown("---")
