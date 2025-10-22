import time
import random
from typing import List, Dict, Any, Optional

# Dependencies from other structural files (Knowing the Known)
from TOKEN_1_SNIFFEE.wifi_analyzer import ConceptualWifiAnalyzer # File 6 (Data Structure)
# Note: FavoriteSeedGenerator is part of this token's architecture (File 9)
# Assuming it is available for instantiation here.
from TOKEN_1_SNIFFEE.favorite_seed_generator import FavoriteSeedGenerator 

class SDBRewardLogic:
    """
    Manages the Proof-of-Favorite-Seed (PoFS) consensus for the @SNIFFEE-DEBUGEE token.
    
    This logic determines the winner by matching a node's current cryptographic 
    traffic proof against a non-linearly generated "Favorite Randomized Seed."
    """

    SDB_REWARD_AMOUNT: int = 300
    SDB_CYCLE_TIME_SECONDS: int = 30 * 60  # 30 minutes
    
    # This is the simulated difficulty: how many characters of the hash 
    # must match the target seed. Higher number = higher computational degree.
    MATCH_DIFFICULTY_LENGTH: int = 5 

    def __init__(self):
        """Initializes the integrated components for the PoFS execution layer."""
        self.analyzer = ConceptualWifiAnalyzer()
        self.seed_generator = FavoriteSeedGenerator()
        self.last_reward_time = time.time()

    def _find_seed_match_winner(self, eligible_nodes_data: List[Dict[str, Any]], target_seed: str) -> Optional[Dict[str, Any]]:
        """
        Iterates through node data proofs to find a match against the target seed prefix.
        This represents the core PoFS computational puzzle resolution.
        """
        match_prefix = target_seed[:self.MATCH_DIFFICULTY_LENGTH]
        print(f"Target Seed Match Prefix: {match_prefix}")
        
        for node_data in eligible_nodes_data:
            node_proof = node_data["data_proof_hash"]
            
            # Check for the prefix match
            if node_proof.startswith(match_prefix):
                print(f"SDB Match Found! Node {node_data['node_address']} aligns its hash with the Favorite Seed.")
                return node_data
        
        return None

    def run_sdb_consensus(self, all_active_nodes: List[str]) -> Optional[Dict[str, Any]]:
        """
        The main execution function for the 30-minute SDB reward cycle.
        
        Returns:
            A dictionary containing the winning data for block stamping, or None.
        """
        
        # 1. Time Gate: Ensure the 30-minute cycle has elapsed
        if time.time() - self.last_reward_time < self.SDB_CYCLE_TIME_SECONDS:
             return None
        
        if not all_active_nodes:
            return None

        print(f"\n--- SDB PoFS Consensus Active. Executing 30-min reward cycle. ---")

        # 2. Generate the Non-Linear Target Seed (File 9 Logic)
        target_seed = self.seed_generator.generate_favorite_seed()
        print(f"Generated Favorite Randomized Online Seed: {target_seed}")

        # 3. Aggregate Node Proofs (File 6 Logic)
        eligible_nodes_data = self.analyzer.aggregate_all_node_traffic(all_active_nodes)

        # 4. Find the Winner (The PoFS Puzzle Resolver)
        winner_data = self._find_seed_match_winner(eligible_nodes_data, target_seed)
        
        if not winner_data:
            print("SDB Consensus: No computational alignment found this cycle.")
            return None

        # 5. Update timer and format block data
        self.last_reward_time = time.time()
        
        return {
            "winner_address": winner_data["node_address"],
            "reward_amount": self.SDB_REWARD_AMOUNT,
            "binary_transit_no": winner_data["io_traffic_details"]["total_packet_count"],
            "seedframe": target_seed, # The winning block is stamped with the target seed
            "reward_type": "@SNIFFEE-DEBUGEE",
            "proof_data": winner_data # Log the full winner data for auditing
        }
