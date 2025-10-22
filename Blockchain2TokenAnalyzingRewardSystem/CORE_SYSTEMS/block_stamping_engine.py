import hashlib
import time
import json
import csv
from typing import List, Dict, Any

# --- Module for Cryptography (Used for block integrity and security layers) ---
from    TOKEN_1_SNIFFEE.security_hasher import SecurityHasher

class BlockStampingEngine:
    """
    Manages the creation, cryptographic stamping, and persistence of new blocks.
    It enforces the dual-cryption layers and handles the progressive complexity.
    """
    
    # Define file paths for persistence
    LOG_FILEPATH: str = "blockchain_log.json"
    CSV_FILEPATH: str = "blockchain_ledger.csv"

    def __init__(self, chain: List[Dict[str, Any]], complexity: float):
        """Initializes the engine with the current chain state and difficulty."""
        self.blockchain = chain
        self.current_complexity = complexity
        self.hasher = SecurityHasher()

    def update_complexity(self, new_complexity: float) -> None:
        """Updates the Progressive Eternity complexity factor."""
        self.current_complexity = new_complexity
        
    def _get_last_block(self) -> Dict[str, Any]:
        """Retrieves the last stamped block in the chain."""
        # Ensure the chain is not empty before attempting to access the last block
        if not self.blockchain:
            # Should be handled by main_node_runner creating the Genesis block, 
            # but this provides a safe fallback structure.
            return {
                "HARDCOVER_CRYPTION": self.hasher.placeholder_hash(), # 000...0
                "BLOCK_INDEX": 0
            }
        return self.blockchain[-1]

    def _prepare_block_data(
        self,
        index: int,
        previous_hash: str,
        miner_address: str,
        reward_type: str,
        reward_amount: int,
        binary_transit_no: int,
        seedframe: str
    ) -> Dict[str, Any]:
        """
        Assembles the core block data structure with all required logistical stamps.
        The 'TIME' and 'TIMESTAMP' stamps are separated for human readability and 
        machine precision.
        """
        timestamp_s = time.time()
        
        block = {
            # Core Chain Integrity
            "BLOCK_INDEX": index,
            "TIME": time.ctime(timestamp_s),  # Human readable time stamp
            "TIMESTAMP": timestamp_s,         # Machine precision timestamp
            "PREVIOUS_HASH": previous_hash,
            "COMPLEXITY_LEVEL": self.current_complexity, # Progressive Eternity factor
            
            # Dual-Token Reward Logistics
            "WINNERS_ADDRESSES": miner_address,
            "REWARD_CHAIN": reward_type,
            "REWARD_AMOUNT": reward_amount,
            "SEEDFRAME": seedframe,
            
            # BTZCY-SYSTEM Specific Data
            "BINARY-TRANSIT-NO": binary_transit_no, 
            
            # Cryptographic Layers (Soft and Hard)
            "SOFT-ENCRYPTER": self.hasher.soft_encrypt(str(miner_address) + reward_type),
        }
        return block

    def stamp_new_block(
        self,
        miner_address: str,
        reward_type: str,
        reward_amount: int,
        binary_transit_no: int,
        seedframe: str = "0",
        is_genesis: bool = False
    ) -> Dict[str, Any]:
        """
        Stamps a complete, cryptographically secured new block onto the chain.
        """
        last_block = self._get_last_block()
        index = last_block["BLOCK_INDEX"] + 1
        previous_hash = last_block["HARDCOVER_CRYPTION"]
        
        # 1. Prepare Block Data
        new_block = self._prepare_block_data(
            index,
            previous_hash,
            miner_address,
            reward_type,
            reward_amount,
            binary_transit_no,
            seedframe
        )
        
        # 2. Apply Hardcover-Cryption (SHA-256 for integrity)
        block_content_string = json.dumps(new_block, sort_keys=True)
        hard_hash = self.hasher.sha256_hash(block_content_string)
        new_block["HARDCOVER_CRYPTION"] = hard_hash
        
        # 3. Apply Constellation-Security Lock (Fictional/Conceptual SHA-4091 equivalent)
        # This function conceptually triggers the block's immutability status.
        constellation_lock = self.hasher.constellation_lock_key(
            hard_hash, 
            self.current_complexity, 
            reward_type
        )
        new_block["CONSTELLATION-SECURITY"] = constellation_lock

        print(f"[{new_block['TIME']}] Block {index} Stamped. Reward: {reward_amount} {reward_type}")
        return new_block


    def save_chain(self, chain: List[Dict[str, Any]]) -> None:
        """
        Saves the complete blockchain state to both a JSON file for easy loading 
        and a CSV ledger for infinite infinity stamping and analysis.
        """
        # --- 1. JSON Persistence (Load/Save) ---
        try:
            with open(self.LOG_FILEPATH, 'w') as f:
                json.dump(chain, f, indent=4)
        except IOError as e:
            print(f"ERROR: Could not save JSON log file: {e}")

        # --- 2. CSV Persistence (Analytical Ledger) ---
        if not chain:
            return
            
        fieldnames = list(chain[0].keys())
        
        try:
            # Append to CSV, but write header only if file is new/empty
            file_exists = self.CSV_FILEPATH in [f.name for f in os.scandir('.')]
            write_header = not file_exists or os.path.getsize(self.CSV_FILEPATH) == 0

            with open(self.CSV_FILEPATH, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if write_header:
                    writer.writeheader()
                    # If we write the header, we should write all blocks to ensure
                    # integrity, or just the new block since the last save.
                    # For simplicity, we write the entire chain to ensure sync.
                    writer.writerows(chain)
                else:
                    # Only write the last block (the newest one)
                    writer.writerow(chain[-1])

        except IOError as e:
            print(f"ERROR: Could not save CSV ledger file: {e}")


if __name__ == '__main__':
    # Simple example usage for debugging (requires SecurityHasher to run)
    print("This file should be imported and run via main_node_runner.py.")
    print("Please proceed to generating the next file: security_hasher.py (File 11).")
