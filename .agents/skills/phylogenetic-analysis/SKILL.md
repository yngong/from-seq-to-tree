---
name: phylogenetic-analysis
description: End-to-end evolutionary and phylogenetic sequence analysis workflow from FASTA to multiple sequence alignment, maximum-likelihood tree reconstruction, outgroup rooting, and interactive visualization.
---

# Phylogenetic Analysis Skill (From Sequences to Tree)

This skill provides step-by-step procedures, tool invocations, and troubleshooting recipes for phylogenetic analysis on viral and bacterial genomic sequences.

## Pipeline Architecture

1. **Input Inspection**: Read FASTA sequences, examine sequence lengths, check GC%, and identify excessive ambiguity codes (`N`).
2. **Multiple Sequence Alignment (MSA)**: Align sequences using MAFFT or MUSCLE.
3. **Alignment QC & Trimming**: Measure parsimony-informative sites and inspect conserved blocks.
4. **Phylogenetic Reconstruction**: Build maximum-likelihood trees using IQ-TREE with ultrafast bootstrap.
5. **Rooting & Divergence Assessment**: Re-root trees on designated outgroups (e.g. `A/California/07/2009` for H1N1pdm09).
6. **Interactive Visualization**: Export trees to Newick, NEXUS, and self-contained interactive HTML dashboards.

---

## Standard Commands

### 1. Multiple Sequence Alignment (MAFFT)
```bash
# Auto mode (fast & robust)
mafft --auto input.fasta > aligned.fasta

# High-accuracy mode for small datasets (< 200 sequences)
mafft --maxiterate 1000 --localpair input.fasta > aligned.fasta
```

### 2. Alignment Inspection
```bash
python3 scripts/compare_alignment_qc.py aligned.fasta
```

### 3. Maximum-Likelihood Tree Building (IQ-TREE)
```bash
# Fast GTR+G model with 1000 ultrafast bootstraps
iqtree -s aligned.fasta -m GTR+G -B 1000 -T AUTO --redo -pre tree_out

# Automatic Model Selection with ModelFinder + SH-aLRT + UFBoot
iqtree -s aligned.fasta -m MFP -alrt 1000 -B 1000 -T AUTO --redo -pre tree_out
```

### 4. Interactive Visualization
```bash
python3 scripts/render_tree_interactive.py tree_out.treefile metadata.tsv outputs/interactive_tree.html
```

---

## Common Gotchas & Troubleshooting

- **Duplicate Sequence Headers**: Downstream phylogenetic tools (IQ-TREE, RAxML) fail if headers are non-unique. Ensure unique strain names.
- **Illegal Header Characters**: Avoid spaces, colons, or parentheses in FASTA headers when passing to tree building programs.
- **Unrooted vs Rooted Trees**: Raw IQ-TREE outputs are unrooted. Always root with a known historical outgroup before measuring molecular clock rates or interpreting lineage succession.
