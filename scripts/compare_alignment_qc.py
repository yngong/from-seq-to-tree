#!/usr/bin/env python3
"""
Sequence Alignment QC and Statistics Inspector.
Calculates alignment length, pairwise divergence, GC content, and parsimony-informative sites.
"""

import sys
import os
from Bio import AlignIO
from Bio.SeqUtils import gc_fraction

def analyze_alignment(alignment_path):
    if not os.path.exists(alignment_path):
        print(f"File not found: {alignment_path}")
        sys.exit(1)

    alignment = AlignIO.read(alignment_path, "fasta")
    num_seqs = len(alignment)
    align_len = alignment.get_alignment_length()

    print("\n" + "="*50)
    print("  ALIGNMENT QUALITY CONTROL REPORT")
    print("="*50)
    print(f"File:                      {os.path.basename(alignment_path)}")
    print(f"Number of Taxa:            {num_seqs}")
    print(f"Alignment Length:          {align_len} bp")

    # Count constant, singleton, informative sites
    informative_sites = 0
    constant_sites = 0
    variable_sites = 0

    for col_idx in range(align_len):
        column = alignment[:, col_idx].upper()
        # Filter out gaps and ambiguous
        bases = [b for b in column if b in "ACGT"]
        unique_bases = set(bases)
        if len(unique_bases) <= 1:
            constant_sites += 1
        else:
            variable_sites += 1
            # Check if parsimony informative (at least 2 states occurring >= 2 times)
            counts = {b: bases.count(b) for b in unique_bases}
            qualifying = [b for b, cnt in counts.items() if cnt >= 2]
            if len(qualifying) >= 2:
                informative_sites += 1

    print(f"Constant Sites:            {constant_sites} ({constant_sites/align_len*100:.1f}%)")
    print(f"Variable Sites:            {variable_sites} ({variable_sites/align_len*100:.1f}%)")
    print(f"Parsimony-Informative:     {informative_sites} ({informative_sites/align_len*100:.1f}%)")
    print("-" * 50)
    print(f"{'Taxon':<45} {'GC%':<8} {'Gaps%'}")
    print("-" * 50)

    for record in alignment:
        gc = gc_fraction(record.seq) * 100
        gaps = (record.seq.count("-") / align_len) * 100
        print(f"{record.id[:43]:<45} {gc:5.1f}%  {gaps:5.1f}%")
    print("="*50 + "\n")

if __name__ == "__main__":
    aln = sys.argv[1] if len(sys.argv) > 1 else "data/h1n1/h1n1_ha_aligned.fasta"
    analyze_alignment(aln)
