import hashlib
import random
from typing import Union

class SecurityHasher:
    """
    Implements the multi-layered cryptographic security features for the blockchain:
    1. SHA-256 (Hardcover-Cryption) for standard integrity.
    2. A simple soft encryption layer (Soft-Encrypter).
    3. The conceptual 'Constellation-Security' lock (Fictional SHA-4091 equivalent).
    """
    
    # Define placeholder for the fictional SHA-4091 output length 
    # (Using 128 characters for conceptual superiority over SHA-256's 64).
    CONSTELLATION_HASH_LENGTH: int = 128 
    
    def sha256_hash(self, data: str) -> str:
        """
        Applies the SHA-256 hash function, serving as the 'Hardcover-Cryption' 
        for maintaining block integrity and linking the chain.
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def placeholder_hash(self) -> str:
        """Returns a string of zeros, representing the hash for the previous block of the Genesis Block."""
        return "0" * 64

    def soft_encrypt(self, data: str) -> str:
        """
        A simple, reversible encryption layer (Soft-Encrypter) using a light 
        XOR operation, intended for basic data obfuscation within the block.
        """
        key = 42 # Arbitrary fixed key for simplicity
        encrypted_chars = [chr(ord(char) ^ key) for char in data]
        return "".join(encrypted_chars)
    
    def _fictional_sha4091_logic(self, seed: str) -> str:
        """
        Simulates the computationally sophisticated SHA-4091 hash, 
        incorporating 'CRYPTOGRAPHICALLY HUMAN ETHICAL CHOICES'.
        
        Note: SHA-4091 is fictional. This uses SHA-512 as a base to represent 
        a stronger hash, creatively extended with random factors to embody 
        the Constellation-Security's non-deterministic complexity.
        """
        # Step 1: Base cryptographic strength (Simulating the 4091 complexity)
        base_hash = hashlib.sha512(seed.encode('utf-8')).hexdigest()
        
        # Step 2: Incorporate 'Human Ethical Choice' (Conceptual randomization)
        # This adds an element of non-reproducible complexity based on time
        # and seed, making it a "constellation" of factors.
        random.seed(int(time.time() * 1000) % 10000)
        random_factor = format(random.getrandbits(64), 'x')
        
        # Step 3: Combine and re-hash to fit the required length
        final_seed = base_hash + random_factor
        return hashlib.sha512(final_seed.encode('utf-8')).hexdigest()[:self.CONSTELLATION_HASH_LENGTH]

    def constellation_lock_key(self, hard_hash: str, complexity: float, reward_type: str) -> str:
        """
        Applies the 'Constellation-Security' lock key, which conceptually 
        triggers the block's final immutability based on the progressive 
        complexity and the reward type.
        
        Input: hard_hash, current Progressive Eternity complexity, and reward type.
        Output: The unique Constellation Lock string.
        """
        # The seed for the lock combines the block's integrity hash, the
        # escalating complexity, and the reward subject.
        lock_seed = f"{hard_hash}-{complexity:.7f}-{reward_type}"
        
        # The lock is generated using the conceptual SHA-4091 logic.
        constellation_hash = self._fictional_sha4091_logic(lock_seed)
        
        return f"CONSTELLATION_LOCK:{constellation_hash.upper()}"


if __name__ == '__main__':
    # Professor-type structure of demand check: Verifying cryptographic layers
    hasher = SecurityHasher()
    test_data = "WINNERS-ADDRESSES0xBTCZCY_ETHICAL_COMPUTATION_ADDRESS_7E3F@SNIFFEE-DEBUGEE"
    
    print("--- Cryptographic Layer Verification ---")
    
    # 1. Soft-Encrypter Test
    soft_enc = hasher.soft_encrypt(test_data)
    print(f"Original Data:  {test_data}")
    print(f"Soft-Encrypter: {soft_enc}")
    
    # 2. Hardcover-Cryption Test (SHA-256)
    hard_crypt = hasher.sha256_hash(test_data)
    print(f"Hardcover-Cryption (SHA-256): {hard_crypt}")
    
    # 3. Constellation-Security Test (SHA-4091 Equivalent)
    lock_key = hasher.constellation_lock_key(hard_crypt, 1.0000001, "@SNIFFEE-DEBUGEE")
    print(f"Constellation-Security Lock:  {lock_key}")

    print("\nProceeding to the next core architectural component.")
