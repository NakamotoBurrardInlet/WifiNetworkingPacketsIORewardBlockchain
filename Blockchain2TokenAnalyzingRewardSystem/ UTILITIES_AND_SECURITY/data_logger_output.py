import json
import csv
import os
from typing import List, Dict, Any

class DataLoggerOutput:
    """
    Manages the persistent archival of the blockchain to two distinct formats:
    1. A structured CSV ledger for high-speed statistical analysis.
    2. A complete JSON log for deep auditing of nested cryptographic and ethical proofs.
    
    This class handles the complexity of flattening nested dictionary structures for 
    the CSV output while retaining full fidelity in the JSON output.
    """

    JSON_FILEPATH: str = "blockchain_audit_log.json"
    CSV_FILEPATH: str = "blockchain_ledger.csv"
    
    # Core fields that must always be present in the CSV ledger
    CSV_CORE_FIELDNAMES: List[str] = [
        "BLOCK_INDEX", 
        "TIMESTAMP", 
        "TIME", 
        "REWARD_CHAIN",
        "REWARD_AMOUNT",
        "WINNERS_ADDRESSES",
        "COMPLEXITY_LEVEL",
        "PREVIOUS_HASH",
        "HARDCOVER_CRYPTION",
        "CONSTELLATION-SECURITY"
    ]
    
    # Nested fields we want to specifically extract and flatten for the CSV for ease of use
    CSV_FLATTENED_FIELDNAMES: List[str] = [
        "BINARY-TRANSIT-NO",
        "SDB_SEEDFRAME",
        "BTZ_CHALLENGE_ID",
        "BTZ_EXPIRY_TIMESTAMP",
        "BTZ_PACKETS_TOTAL",
        "BTZ_LATENCY_AVG"
    ]

    def __init__(self):
        """Initializes the logger, ensuring the necessary files are available."""
        self.csv_fieldnames = self.CSV_CORE_FIELDNAMES + self.CSV_FLATTENED_FIELDNAMES

    def _flatten_block_data(self, block: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts and flattens complex, nested block data into a single-level 
        dictionary suitable for the CSV ledger.
        """
        flat_data = block.copy()
        
        # --- Handle BTZ (Token 2) Data Flattening ---
        if block["REWARD_CHAIN"] == "BTZCY-SYSTEM":
            # Data is nested under the 'proof_data' and 'ethical_challenge' keys
            proof_data = block.get('PROOF_DATA', {})
            traffic = proof_data.get('traffic_data', {})
            challenge = block.get('ETHICAL_CHALLENGE', {})
            
            flat_data["BTZ_CHALLENGE_ID"] = challenge.get("challenge_id", "")
            flat_data["BTZ_EXPIRY_TIMESTAMP"] = challenge.get("expiry_timestamp", 0)
            flat_data["BTZ_PACKETS_TOTAL"] = traffic.get("total_packet_count", 0)
            flat_data["BTZ_LATENCY_AVG"] = traffic.get("simulated_latency_ms", 0.0)
            
        # --- Handle SDB (Token 1) Data Flattening ---
        elif block["REWARD_CHAIN"] == "@SNIFFEE-DEBUGEE":
            # The SDB seedframe is the block's main seed factor
            flat_data["SDB_SEEDFRAME"] = block.get("SEEDFRAME", "")

        # Remove the complex nested fields from the dictionary before writing the CSV
        for key in ['PROOF_DATA', 'ETHICAL_CHALLENGE', 'SOFT-ENCRYPTER', 'SEEDFRAME']:
            flat_data.pop(key, None)
            
        return flat_data

    def log_block(self, block: Dict[str, Any], full_chain: List[Dict[str, Any]]) -> None:
        """
        Logs the new block to both the JSON log (full fidelity) and the CSV ledger (summary).
        """
        # 1. Log to JSON (Audit Log)
        self._log_to_json(full_chain)
        
        # 2. Log to CSV (Statistical Ledger)
        self._log_to_csv(block)
        
        print(f"[{block['TIME']}] Logged Block {block['BLOCK_INDEX']} to JSON/CSV. Complexity: {block['COMPLEXITY_LEVEL']:.7f}")

    def _log_to_json(self, chain: List[Dict[str, Any]]) -> None:
        """Writes the entire blockchain to the JSON audit log file."""
        try:
            with open(self.JSON_FILEPATH, 'w') as f:
                json.dump(chain, f, indent=4)
        except IOError as e:
            print(f"ERROR: Could not save JSON audit log file: {e}")

    def _log_to_csv(self, block: Dict[str, Any]) -> None:
        """Appends the flattened block data to the CSV ledger."""
        
        # Flatten the data structure to fit the CSV columns
        flat_block = self._flatten_block_data(block)
        
        # Determine if the file exists and whether the header needs to be written
        file_exists = os.path.exists(self.CSV_FILEPATH)
        write_header = not file_exists or os.path.getsize(self.CSV_FILEPATH) == 0

        try:
            with open(self.CSV_FILEPATH, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.csv_fieldnames)
                
                if write_header:
                    writer.writeheader()
                
                # Write the new block data
                writer.writerow(flat_block)

        except IOError as e:
            print(f"ERROR: Could not save CSV ledger file: {e}")
        except ValueError as e:
            # Handle cases where a row might not contain all fieldnames (should not happen with _flatten_block_data)
            print(f"ERROR: CSV writing failed due to missing fields: {e}")

# Note: This file is designed to be imported by block_stamping_engine.py 
# (File 2) for integration into the main block stamping process.


#We have successfully generated the eleventh file, **`UTILITIES_AND_SECURITY/data_logger_output.py`**. This robust file ensures every block is logged with its full complexity and proof data.
