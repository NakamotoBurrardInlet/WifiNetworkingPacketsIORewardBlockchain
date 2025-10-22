import random
import time
import hashlib
from typing import List, Dict, Any, Optional

# Dependencies from other structural files
from TOKEN_1_SNIFFEE.wifi_analyzer import ConceptualWifiAnalyzer # For data structure
from TOKEN_2_BTZCY.ping_nmap_verifier import PingNmapVerifier # For integrity check

class BTZRewardLogic:
    """
    Manages the Proof-of-Traffic-Volume (PoTV) consensus for the BTZCY-SYSTEM token.
    
    This logic determines the highest I/O node and initiates the 'Human Ethical Choice' 
    (5-minute acceptance) required to finalize the 150 BTZ reward block stamp.
    """

    BTZ_REWARD_AMOUNT: int = 150
    BTZ_CYCLE_TIME_SECONDS: int = 5 * 60  # 5 minutes

    def __init__(self):
        """Initializes the logic with required utility and verification components."""
        self.analyzer = ConceptualWifiAnalyzer()
        self.verifier = PingNmapVerifier()
        self.last_reward_time = time.time() # Tracks the last block stamp time

    def _determine_highest_traffic_winner(self, verified_traffic_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Selects the node with the highest I/O O/I packet count (PoTV winner).
        The data must have already passed the PING/NMAP verification layer.
        """
        if not verified_traffic_data:
            return None

        # 1. Select the raw winner based on the highest total packet count
        sorted_nodes = sorted(
            verified_traffic_data, 
            key=lambda x: x['io_traffic_details'].get('total_packet_count', 0), 
            reverse=True
        )
        
        # 2. Logistical check: Ensure the winner is verified
        winner = sorted_nodes[0]
        if not winner['is_verified']:
             # Theoretically, this shouldn't happen if input is pre-verified, 
             # but acts as a safety check.
            print(f"WARNING: Highest traffic node {winner['address']} failed final verification.")
            return None 

        return winner

    def _create_ethical_choice_challenge(self, winner_address: str, packet_count: int) -> Dict[str, Any]:
        """
        Generates the payload for the 'Human Ethical Choice' challenge.
        The node owner must explicitly accept the reward within the 5-minute window.
        """
        
        challenge_id = hashlib.sha256(f"{winner_address}-{packet_count}-{time.time()}".encode()).hexdigest()
        
        # The node must accept the reward before this timestamp (5 minutes from generation)
        expiry_timestamp = int(time.time()) + self.BTZ_CYCLE_TIME_SECONDS
        
        return {
            "challenge_id": challenge_id,
            "expiry_timestamp": expiry_timestamp,
            "reward_status": "PENDING_ACCEPTANCE", 
            # Simulated proof hash representing indexed ethical data (e.g., node consent status)
            "ethical_proof_hash": f"ETHICAL_CONSENT_0x{random.getrandbits(128):X}", 
        }
        
    def run_btz_consensus(self, all_active_nodes: List[str]) -> Optional[Dict[str, Any]]:
        """
        The main function to run the 5-minute BTZ reward cycle, rewarding the 
        highest I/O node that passes integrity checks and accepts the challenge.
        
        Returns:
            A dictionary containing the winning data for block stamping, or None.
        """
        
        # 1. Time Gate: Ensure the 5-minute cycle has elapsed
        if time.time() - self.last_reward_time < self.BTZ_CYCLE_TIME_SECONDS:
             return None
        
        if not all_active_nodes:
            return None

        print(f"--- BTZ PoTV Consensus Active. Time Check Passed. ---")

        # 2. Aggregate and Verify Data
        # Get raw traffic data structure from the analyzer (File 6)
        raw_traffic_data = self.analyzer.aggregate_all_node_traffic(all_active_nodes)
        
        # Merge traffic data with verification reports (File 8)
        verified_reports = self.verifier.bulk_verify_nodes(all_active_nodes)
        
        # Combine the two datasets for a final list of eligible nodes
        eligible_nodes = []
        for traffic in raw_traffic_data:
            report = next((r for r in verified_reports if r['address'] == traffic['node_address']), None)
            if report and report['is_verified']:
                # Stamp the verification results onto the traffic data
                traffic_stamp = traffic.copy()
                traffic_stamp['is_verified'] = report['is_verified']
                traffic_stamp['verification_hash_proof'] = report['verification_hash_proof']
                traffic_stamp['io_traffic_details'] = traffic['io_traffic_details']
                traffic_stamp['address'] = traffic['node_address']
                eligible_nodes.append(traffic_stamp)


        # 3. Determine the PoTV Winner
        winner_data = self._determine_highest_traffic_node(eligible_nodes)
        
        if not winner_data:
            print("BTZ Consensus: No verified, high-traffic winner found this cycle.")
            return None

        # 4. Initiate the Human Ethical Choice Challenge
        winner_address = winner_data["address"]
        packet_count = winner_data["io_traffic_details"]["total_packet_count"]
        
        challenge_payload = self._create_ethical_choice_challenge(winner_address, packet_count)
        
        # 5. Assume acceptance (since the acceptance function is outside this core logic)
        # In a real system, the main_node_runner would wait for a 'YES' transaction.
        # For seamless block stamping, we stamp the *challenge* block here:
        
        # Update timer
        self.last_reward_time = time.time()
        
        return {
            "winner_address": winner_address,
            "reward_amount": self.BTZ_REWARD_AMOUNT,
            "binary_transit_no": packet_count,
            "seedframe": challenge_payload['challenge_id'], # Use challenge ID as the seed for traceability
            "reward_type": "BTZCY-SYSTEM",
            "proof_data": winner_data,
            "ethical_challenge": challenge_payload # Log the challenge details
        }