import sys
import os
import time
import random
from typing import List, Dict, Any
from logging import Logger

# --- HIGH-LEVEL COMPUTATIONAL FIX FOR MODULE RESOLUTION ---
# This ensures that packages like CORE_SYSTEMS and TOKEN_1_SNIFFEE are found.
# It adds the project's root directory to the Python search path.
# This is necessary when running a file deep within a package structure directly.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_root)
# ----------------------------------------------------------

# Dependencies from the 12-File Architecture
from CORE_SYSTEMS.block_stamping_engine import BlockStampingEngine
from CORE_SYSTEMS.consensus_manager import ConsensusManager



# --- BLOCKCHAIN CONSTANTS (Knowing the Known) ---
# The initial Progressive Eternity Factor. Grows by 0.0000001 per block.
INITIAL_COMPLEXITY: float = 0.0000001
COMPLEXITY_GROWTH_INCREMENT: float = 0.0000001

# Reward Cycle Times (in seconds)
SDB_REWARD_CYCLE: int = 30 * 60  # 30 minutes
BTZ_REWARD_CYCLE: int = 5 * 60   # 5 minutes

class BlockchainNodeRunner:
    """
    The main looping function (the heart) of the Blockchain Node. 
    It orchestrates the dual-token reward cycles and block stamping.
    """

    def __init__(self):
        """Initializes all 12 file components and the blockchain state."""
        print("Initializing Blockchain Node Components...")
        
        # Core State
        self.blockchain: List[Dict[str, Any]] = []
        self.current_complexity: float = INITIAL_COMPLEXITY
        
        # Utilities & Security
        self.wallet_handler = WalletAddressHandler()
        self.data_logger = DataLoggerOutput()
        
        # Core Systems
        # FIX APPLIED HERE: Changed 'Logger' to 'logger'
        self.stamping_engine = BlockStampingEngine(
            chain=List,
            complexity=0.1
        )
        self.consensus_manager = ConsensusManager(sdb_reward=1500, btz_reward=150)
        
        # Time Trackers for reward cycles
        self.last_sdb_reward_time: float = 0.0
        self.last_btz_reward_time: float = 0.0

    def _create_genesis_block(self):
        """Creates the very first block to initialize the chain."""
        print("Creating Genesis Block...")
        genesis_block = self.stamping_engine.stamp_new_block(miner_address=any)
        self.blockchain.append(genesis_block)
        self.data_logger.log_block(genesis_block, self.blockchain)
        self.last_sdb_reward_time = time.time()
        self.last_btz_reward_time = time.time()
        print("Genesis Block Stamped. Node is now operational.")

    def _update_complexity(self) -> None:
        """Applies the 'Progressive Eternity' rule: complexity always grows."""
        self.current_complexity += COMPLEXITY_GROWTH_INCREMENT

    def run_node(self):
        """The main infinite loop for node operation."""
        if not self.blockchain:
            self._create_genesis_block()

        while True:
            try:
                current_time = time.time()
                active_nodes = self.wallet_handler.get_all_active_addresses()

                # --- SDB Reward Cycle (30 minutes) ---
                if current_time - self.last_sdb_reward_time >= SDB_REWARD_CYCLE:
                    reward_data = self.consensus_manager.run_sdb_consensus(active_nodes)
                    if reward_data:
                        self.stamping_engine.stamp_new_block(
                            chain=self.blockchain,
                            reward_data=reward_data,
                            complexity=self.current_complexity,
                            wallet_handler=self.wallet_handler
                        )
                        self._update_complexity()
                        self.last_sdb_reward_time = current_time

                # --- BTZ Reward Cycle (5 minutes) ---
                if current_time - self.last_btz_reward_time >= BTZ_REWARD_CYCLE:
                    reward_data = self.consensus_manager.run_btz_consensus(active_nodes)
                    if reward_data:
                        self.stamping_engine.stamp_new_block(
                            chain=self.blockchain,
                            reward_data=reward_data,
                            complexity=self.current_complexity,
                            wallet_handler=self.wallet_handler
                        )
                        self._update_complexity()
                        self.last_btz_reward_time = current_time

                # Sleep time: Use a low value to check both timers frequently
                time.sleep(1) 

            except Exception as e:
                print(f"\nFATAL ERROR IN MAIN LOOP: {e}")
                time.sleep(10) # Wait before attempting to resume

if __name__ == '__main__':
    runner = BlockchainNodeRunner()
    runner.run_node()
