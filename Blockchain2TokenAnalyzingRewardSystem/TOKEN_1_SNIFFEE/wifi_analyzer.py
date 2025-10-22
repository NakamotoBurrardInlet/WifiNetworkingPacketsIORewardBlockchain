import random
import hashlib
import time
from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class NetworkPacket:
    """
    Represents a single, highly detailed packet capture. 
    This structure is the foundation of the 'mathematic degree' of complexity.
    """
    timestamp: float = field(default_factory=time.time)
    source_mac: str = field(default_factory=lambda: f"00:1A:2B:{random.randint(0, 99):02X}:{random.randint(0, 99):02X}:{random.randint(0, 99):02X}")
    destination_mac: str = field(default_factory=lambda: f"AA:BB:CC:{random.randint(0, 99):02X}:{random.randint(0, 99):02X}:{random.randint(0, 99):02X}")
    protocol: str = field(default_factory=lambda: random.choice(['TCP', 'UDP', 'ICMP', 'ARP']))
    payload_size_bytes: int = field(default_factory=lambda: random.randint(64, 1500))
    # Simulated high-complexity metadata for 'sniffing' detail
    sequence_number: int = field(default_factory=lambda: random.randint(10000, 99999))
    ttl_hops_remaining: int = field(default_factory=lambda: random.randint(1, 64))


@dataclass
class NodeTrafficSnapshot:
    """
    A full structured snapshot of traffic data for a single node, 
    used as input for the dual reward logic (SDB and BTZ).
    """
    node_address: str
    packets_in: List[NetworkPacket]
    packets_out: List[NetworkPacket]
    simulated_latency_ms: float = field(default_factory=lambda: round(random.uniform(5.0, 150.0), 2))
    timestamp: float = field(default_factory=time.time)

    @property
    def total_packet_count(self) -> int:
        """Returns the total I/O O/I packet count (the PoTV measure)."""
        return len(self.packets_in) + len(self.packets_out)

    def generate_data_proof_hash(self) -> str:
        """
        Creates a cryptographic hash proof based on all captured data. 
        This hash is the basis for matching the 'Favorite Randomized Seed' (SDB) 
        and is included in the block stamp (BTZ).
        """
        # Create a deterministically complex string from all core attributes
        data_string = f"{self.node_address}-{self.timestamp}-{self.total_packet_count}"
        
        # Add complexity by mixing in a random packet's payload size and sequence number
        if self.packets_in:
            data_string += f"-{self.packets_in[0].payload_size_bytes}-{self.packets_in[0].sequence_number}"
        
        return hashlib.sha256(data_string.encode()).hexdigest()


class ConceptualWifiAnalyzer:
    """
    High-level abstraction for generating and aggregating structured network data.
    This class ensures the reward logic receives data of the required 'mathematic degree'.
    """

    def _simulate_packet_capture(self, count: int) -> List[NetworkPacket]:
        """
        Simulates the intensive capture of structured packets. 
        The complexity of the data object itself is the proof of work.
        """
        return [NetworkPacket() for _ in range(count)]

    def get_node_traffic_snapshot(self, node_address: str) -> NodeTrafficSnapshot:
        """
        Generates a full traffic snapshot for a single node. 
        The packet count is randomized to simulate fluctuating network load.
        """
        # PoTV focus: Higher packet counts receive higher rewards
        in_count = random.randint(100, 5000)
        out_count = random.randint(100, 5000)
        
        packets_in = self._simulate_packet_capture(in_count)
        packets_out = self._simulate_packet_capture(out_count)

        return NodeTrafficSnapshot(
            node_address=node_address,
            packets_in=packets_in,
            packets_out=packets_out,
            simulated_latency_ms=round(random.uniform(15.0, 120.0), 2)
        )

    def aggregate_all_node_traffic(self, node_addresses: List[str]) -> List[Dict[str, Any]]:
        """
        Aggregates traffic snapshots for all active nodes for the consensus manager.
        """
        aggregated_data = []
        for address in node_addresses:
            snapshot = self.get_node_traffic_snapshot(address)
            
            # Return a simple dictionary suitable for block stamping and comparison
            aggregated_data.append({
                "node_address": address,
                "data_proof_hash": snapshot.generate_data_proof_hash(),
                "io_traffic_details": {
                    "packets_in": len(snapshot.packets_in),
                    "packets_out": len(snapshot.packets_out),
                    "total_packet_count": snapshot.total_packet_count,
                    "simulated_latency_ms": snapshot.simulated_latency_ms
                }
            })
        return aggregated_data
