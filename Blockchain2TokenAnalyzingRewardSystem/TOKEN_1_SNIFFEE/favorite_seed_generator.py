import time
import random
import hashlib
from typing import Dict, Any, List

class FavoriteSeedGenerator:
    """
    Generates the highly specific 'Favorite Randomized Online Seed Transaction' 
    required for the SDB token's Proof-of-Favorite-Seed (PoFS) consensus.

    This implements a non-linear cryptographic complexity model based on randomized 
    'Favorite' algorithmic choices.
    """

    # Dictionary mapping a conceptual 'Sniffing Preference' (Favorite) to a 
    # computational complexity multiplier. This dictates the difficulty of alignment.
    FAVORITE_ALGORITHM_FACTORS: Dict[str, float] = {
        "HighThroughput_SHA512": 1.5,
        "LowLatency_SHA256": 1.25,
        "DenseTopology_SCRAMBLE": 1.75,
        "RandomizedNoise_XOR": 2.0
    }
    
    # Target bit length for the complex binary computation proof (representing hash difficulty)
    TARGET_SEED_LENGTH: int = 64 # Length in hexadecimal characters (256 bits)

    def __init__(self):
        """Initializes the generator and creates the first immutable seed frame."""
        self._current_seed_frame: Dict[str, Any] = self._generate_new_seed_frame()
        
    def _select_random_favorite(self) -> str:
        """Picks one of the 'Favorite' algorithm types for the current reward cycle."""
        return random.choice(list(self.FAVORITE_ALGORITHM_FACTORS.keys()))

    def _generate_complex_seed(self, favorite_key: str) -> str:
        """
        Creates the non-reversible, high-entropy seed target based on the 
        selected 'Favorite' algorithm and its complexity factor.
        """
        factor = self.FAVORITE_ALGORITHM_FACTORS[favorite_key]
        
        # Input includes time, factor, and a high-entropy random component
        complex_input = f"{favorite_key}-{time.time() * factor}-{random.getrandbits(128)}"
        
        # Use SHA-512 for a strong cryptographic core
        complex_hash = hashlib.sha512(complex_input.encode('utf-8')).hexdigest()
        
        # Truncate the hash to the target length to define the specific puzzle (Seed Transaction)
        return complex_hash[:self.TARGET_SEED_LENGTH]

    def _generate_constellation_lock_key(self, target_seed: str) -> str:
        """
        Generates the 'Constellation Lock Key' as a secondary security measure. 
        This is a non-linear verification signature that ties the seed to the cycle time.
        """
        # Scramble the seed with a time-based hash for uniqueness
        scramble_input = f"{target_seed}-{int(time.time() / 3600)}" # Use hourly block time
        return hashlib.sha256(scramble_input.encode('utf-8')).hexdigest()
        
    def _generate_new_seed_frame(self) -> Dict[str, Any]:
        """Creates a complete new 'Favorite Randomized Online Seed Transaction'."""
        favorite_key = self._select_random_favorite()
        target_seed = self._generate_complex_seed(favorite_key)
        
        return {
            "seed_timestamp": int(time.time()),
            "seed_frame_id": hashlib.sha256(target_seed.encode('utf-8')).hexdigest()[:16],
            "favorite_algorithm": favorite_key,
            "complexity_factor": self.FAVORITE_ALGORITHM_FACTORS[favorite_key],
            "target_seed_transaction": target_seed, # The immutable target hash
            "constellation_lock_signature": self._generate_constellation_lock_key(target_seed)
        }

    def generate_favorite_seed(self) -> str:
        """Retrieves the immutable target seed for the current reward cycle."""
        # This function is called by sdb_reward_logic.py (File 5)
        return self._current_seed_frame["target_seed_transaction"]

    def refresh_seed(self) -> None:
        """
        Generates a completely new seed frame. 
        Should only be called by the Consensus Manager after a successful SDB block stamp.
        """
        self._current_seed_frame = self._generate_new_seed_frame()
        print(f"[{int(time.time())}] New SDB SeedFrame generated. Favorite: {self._current_seed_frame['favorite_algorithm']}")