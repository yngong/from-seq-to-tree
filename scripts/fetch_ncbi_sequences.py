#!/usr/bin/env python3
"""
Fetch Influenza Reference Sequences from NCBI Public Databases (GenBank / NCBI Nucleotide).
Uses BioPython Entrez API or direct HTTPS requests to download verified reference sequences.
"""

import sys
import os
import argparse
from Bio import Entrez, SeqIO

# NCBI requires an email address for Entrez API queries
Entrez.email = "student@university.edu"

# Standard NCBI Accession list for Influenza A (H1N1pdm09) reference and vaccine strains
DEFAULT_NCBI_REFS = {
    "CY121680.1": "A/California/07/2009_REF_NextstrainRoot",
    "OQ719015.1": "A/Victoria/2570/2019_Vaccine_Ref",
    "OQ718989.1": "A/Victoria/4897/2022_Vaccine_Ref",
    "CY045951.1": "A/New_York/18/2009_H1N1",
    "MW626462.1": "A/Wisconsin/588/2019_H1N1",
    "OQ719002.1": "A/Sydney/5/2021_H1N1"
}

def fetch_from_ncbi(accession_list, output_fasta):
    print(f"\n[NCBI] >>> Connecting to NCBI Public Database (Entrez Nucleotide)...")
    print(f"[NCBI] >>> Querying Accessions: {', '.join(accession_list)}")
    
    os.makedirs(os.path.dirname(os.path.abspath(output_fasta)), exist_ok=True)
    records = []

    try:
        handle = Entrez.efetch(db="nucleotide", id=accession_list, rettype="fasta", retmode="text")
        parsed_records = list(SeqIO.parse(handle, "fasta"))
        handle.close()
        
        for record in parsed_records:
            # Map accession to standardized strain name if known
            acc_clean = record.id.split(".")[0]
            matched_name = None
            for ref_acc, ref_name in DEFAULT_NCBI_REFS.items():
                if ref_acc.startswith(acc_clean):
                    matched_name = ref_name
                    break
            
            if matched_name:
                record.id = matched_name
                record.description = f"NCBI_Accession:{acc_clean}"
            records.append(record)
            print(f"[NCBI] Downloaded: {record.id} ({len(record.seq)} bp)")

        SeqIO.write(records, output_fasta, "fasta")
        print(f"\n[SUCCESS] Successfully saved {len(records)} sequences from NCBI to {output_fasta}\n")

    except Exception as e:
        print(f"[ERROR] Failed to query NCBI: {e}")
        print("[HINT] Ensure internet connectivity and valid accession numbers.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Search and download Influenza reference sequences from NCBI public database."
    )
    parser.add_argument(
        "-a", "--accessions", 
        nargs="+", 
        default=list(DEFAULT_NCBI_REFS.keys())[:3],
        help="List of NCBI Accession IDs to download (e.g., CY121680.1 OQ719015.1 OQ718989.1)"
    )
    parser.add_argument(
        "-o", "--output", 
        default="data/h1n1/ncbi_fetched_references.fasta", 
        help="Output FASTA file path"
    )
    parser.add_argument(
        "-e", "--email", 
        default="student@university.edu", 
        help="User email for NCBI Entrez API"
    )
    args = parser.parse_args()

    Entrez.email = args.email
    fetch_from_ncbi(args.accessions, args.output)

if __name__ == "__main__":
    main()
