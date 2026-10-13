#!/usr/bin/env python3
"""
End-to-End Phylogenetic Analysis Pipeline for Google Antigravity.
Executes Sequence QC -> MAFFT Alignment -> IQ-TREE Maximum Likelihood -> Rooting -> HTML Visualization.
"""

import os
import sys
import argparse
import subprocess
from Bio import SeqIO

def run_command(cmd, desc):
    print(f"\n[PIPELINE] >>> {desc}...")
    print(f"[CMD] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] Failed during: {desc}")
        print(res.stderr)
        sys.exit(1)
    print(f"[SUCCESS] {desc} completed successfully.")
    return res.stdout

def qc_fasta(fasta_path):
    print(f"\n[PIPELINE] >>> Step 1: Performing Quality Control on {fasta_path}...")
    seqs = list(SeqIO.parse(fasta_path, "fasta"))
    if not seqs:
        raise ValueError(f"No sequences found in {fasta_path}")
    
    lengths = [len(s.seq) for s in seqs]
    avg_len = sum(lengths) / len(lengths)
    
    print(f"  - Total Taxa: {len(seqs)}")
    print(f"  - Min Length: {min(lengths)} bp")
    print(f"  - Max Length: {max(lengths)} bp")
    print(f"  - Mean Length: {avg_len:.1f} bp")
    
    # Check ambiguities
    ambiguous = {}
    for s in seqs:
        n_count = s.seq.upper().count('N')
        if n_count > 0:
            ambiguous[s.id] = (n_count, n_count / len(s.seq) * 100)
            
    if ambiguous:
        print(f"  - Notice: {len(ambiguous)} sequences contain 'N' bases (acceptable within threshold):")
        for k, v in list(ambiguous.items())[:3]:
            print(f"    * {k}: {v[0]} Ns ({v[1]:.2f}%)")
    else:
        print("  - Zero 'N' ambiguities detected. Sequence quality is pristine.")
    return len(seqs)

def main():
    parser = argparse.ArgumentParser(description="Antigravity Sequence-to-Tree Workflow")
    parser.add_argument("-i", "--input", default="data/h1n1/h1n1_ha_unaligned.fasta", help="Input unaligned FASTA")
    parser.add_argument("-m", "--meta", default="data/h1n1/h1n1_ha_metadata.tsv", help="Metadata TSV")
    parser.add_argument("-o", "--outdir", default="outputs", help="Output directory")
    parser.add_argument("-t", "--threads", default="4", help="CPU threads to use")
    parser.add_argument("--model", default="GTR+G", help="IQ-TREE nucleotide substitution model (or MFP)")
    parser.add_argument("--bootstrap", default="1000", help="Ultrafast bootstrap replicates")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(args.input))[0]
    
    aligned_fasta = os.path.join(args.outdir, f"{base_name}_aligned.fasta")
    tree_prefix = os.path.join(args.outdir, f"{base_name}_iqtree")
    final_html = os.path.join(args.outdir, "interactive_tree.html")

    # Step 1: QC
    qc_fasta(args.input)

    # Step 2: MAFFT Alignment
    cmd_mafft = f"mafft --auto --thread {args.threads} {args.input} > {aligned_fasta}"
    run_command(cmd_mafft, "Step 2: Multiple Sequence Alignment (MAFFT)")

    # Step 3: IQ-TREE ML Inference
    cmd_iqtree = f"iqtree -s {aligned_fasta} -m {args.model} -B {args.bootstrap} -T {args.threads} --redo -pre {tree_prefix}"
    run_command(cmd_iqtree, "Step 3: Maximum Likelihood Tree Construction (IQ-TREE)")

    # Step 4: Render Interactive Visualization
    script_dir = os.path.dirname(os.path.abspath(__file__))
    render_script = os.path.join(script_dir, "render_tree_interactive.py")
    treefile = f"{tree_prefix}.treefile"
    cmd_render = f"python3 {render_script} {treefile} {args.meta} {final_html}"
    run_command(cmd_render, "Step 4: Interactive HTML Visualizer Generation")

    print("\n" + "="*60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Alignment Output:   {aligned_fasta}")
    print(f"Phylogenetic Tree:  {treefile}")
    print(f"Interactive Viewer: {final_html}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
