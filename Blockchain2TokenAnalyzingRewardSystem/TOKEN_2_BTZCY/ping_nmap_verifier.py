import random
import time
import hashlib
from typing import List, Dict, Any, Union

class PingNmapVerifier:
    """
    Implements a computationally realistic simulation of the verification layer 
    for the Proof-of-Traffic-Volume (PoTV). 
    
    This layer ensures the integrity of the claimed I/O packets by checking for:
    1. Liveness (PING simulation)
    2. Service Integrity (NMAP simulation for required blockchain ports)
    3. Proof-of-Work (Hashing of latency data to verify effort).
    """

    # Constants derived from the 'Progressive Eternity' model
    MINIMUM_VERIFICATION_HASH_DIFFICULTY = "000"  # Requires hash to start with three zeroes conceptually
    MAX_LATENCY_MS = 150 
    DEFAULT_PING_PACKETS = 4 
    CONNECTIVITY_SUCCESS_RATE = 0.9 

    def __init__(self):
        """Initializes the verifier with a conceptual difficulty target."""
        self.difficulty_target = self.MINIMUM_VERIFICATION_HASH_DIFFICULTY

    def _generate_proof_of_verification_work(self, raw_data: str) -> str:
        """
        A micro-PoW mechanism: hashes the network data until the difficulty 
        target is met, simulating the computational cost of real-time analysis.
        This provides a 'non-simulated' computational expense to the verification process.
        """
        nonce = 0
        while True:
            # Combine raw data and nonce
            attempt = f"{raw_data}{nonce}"
            # Use SHA256 for integrity check
            hash_result = hashlib.sha256(attempt.encode('utf-8')).hexdigest()
            
            # Check if the hash meets the difficulty target
            if hash_result.startswith(self.difficulty_target):
                return hash_result
            
            nonce += 1
            if nonce > 10000: # Safety break for simulation
                return f"NonceExceeded-{hash_result[:10]}"

    def _simulated_ping(self, address: str) -> Dict[str, Union[str, float, int]]:
        """
        Simulates PING with a focus on traceable data, generating latency values 
        that become part of the verification PoW hash.
        """
        if random.random() > self.CONNECTIVITY_SUCCESS_RATE:
            return {
                "status": "FAILED",
                "latency_avg_ms": 0.0,
                "packets_lost": self.DEFAULT_PING_PACKETS,
                "raw_latency_data": ""
            }
        
        latency_values = [random.uniform(20.0, self.MAX_LATENCY_MS) 
                          for _ in range(self.DEFAULT_PING_PACKETS)]
        
        # Create traceable raw data string from the simulation result
        raw_latency_data = ",".join([f"{l:.3f}" for l in latency_values])
        
        return {
            "status": "SUCCESS",
            "latency_avg_ms": round(sum(latency_values) / len(latency_values), 3),
            "packets_lost": 0,
            "raw_latency_data": raw_latency_data
        }

    def _simulated_nmap_scan(self, address: str) -> Dict[str, Union[str, int, str]]:
        """
        Simulates NMAP service verification, ensuring the critical service is running.
        """
        is_service_running = random.random() > 0.1 
        
        return {
            "service_status": "RUNNING" if is_service_running else "BLOCKED",
            "verified_ports_hash": hashlib.sha256(f"{address}-{int(is_service_running)}".encode()).hexdigest()[:10],
            "scan_timestamp": int(time.time())
        }

    def verify_node_integrity(self, node_address: str) -> Dict[str, Any]:
        """
        Executes the combined verification check and generates the PoW proof 
        based on the simulated network data.
        """
        ping_report = self._simulated_ping(node_address)
        nmap_report = self._simulated_nmap_scan(node_address)

        is_verified = (ping_report["status"] == "SUCCESS" and 
                       nmap_report["service_status"] == "RUNNING")
        
        # Combine all verification data into a single string for PoW
        proof_input = f"{node_address}-{ping_report['raw_latency_data']}-{nmap_report['verified_ports_hash']}-{is_verified}"
        
        verification_proof = self._generate_proof_of_verification_work(proof_input)

        return {
            "address": node_address,
            "verification_timestamp": int(time.time()),
            "is_verified": is_verified,
            "ping_results": ping_report,
            "nmap_results": nmap_report,
            "verification_hash_proof": verification_proof,
            "difficulty_target": self.difficulty_target
        }

    def bulk_verify_nodes(self, node_list: List[str]) -> List[Dict[str, Any]]:
        """Performs verification on all active nodes."""
        full_reports = [self.verify_node_integrity(address) for address in node_list]
        return full_reports
