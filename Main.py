import random as rnd
import math as mt

def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
       
def generate_prime(min_val, max_val):
    prime = rnd.randint(min_val, max_val)
    while not is_prime(prime):
        prime = rnd.randint(min_val, max_val)
    return prime


def generate_p_q(p, q):
    p, q = generate_prime(1000000, 100000000), generate_prime(1000000, 100000000)
    while p == q:
        q = generate_prime(1000000, 100000000)
    return p, q 

def generate_public_key(phi):
    pub_key =  rnd.randint(3, phi - 1)
    while mt.gcd(pub_key, phi) != 1:
        pub_key = rnd.randint(3, phi - 1)
    return pub_key

def get_n(p, q):
    return p * q

def get_phi(p, q):
    return (p - 1) * (q - 1)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    
    gcd, x, y = extended_gcd(b % a, a)
    return gcd, y - (b // a) * x, x


def mod_inverse(public_key, phi):
    gcd, x, y = extended_gcd(public_key, phi)
    if gcd != 1:
        raise ValueError(f"The modular inverse does not exist for {public_key} (mod {phi})")
    else:
        return x % phi

def encode(message):
    msg_encoded = [ord(c) for c in message]
    return msg_encoded

# (m ^ public_key) mod n = ciphertext
def get_ciphertext(public_key, n, encoded_message):
    
          #(c ^ public_key) % n
    ct = [pow(c, public_key, n) for c in encoded_message]
    return ct

def decode(private_key, n, chipertext):
    message_decoded = [pow(c, private_key, n) for c in chipertext]
    return message_decoded
    
if __name__ == "__main__":
    p , q = generate_p_q(1, 1)
    n = get_n(p, q)
    phi = get_phi(p, q)
    
    public_key = generate_public_key(phi)
    
    private_key = mod_inverse(public_key, phi)
    
    message = "Poruka"
    
    encoded_message = encode(message)
    
    chipertext = get_ciphertext(public_key, n, encoded_message)
    
    decoded_message = decode(private_key, n, chipertext)
    
    message = "".join(chr(c) for c in decoded_message)
    print(f'p: {p},\n q: {q},\n n: {n},\n public key: {public_key},\n private key: {private_key},\n encoded message = {encoded_message},\n chipertext = {chipertext},\n')
    print(f'Decoded message: {decoded_message}')
    print(f'Decrypted message: {message}')
