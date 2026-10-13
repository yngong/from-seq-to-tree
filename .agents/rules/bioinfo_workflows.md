# Bioinformatics & Phylogenetic Analysis Rules for Google Antigravity

When assisting students and researchers in this repository, follow these domain-specific best practices:

## 1. Sequence Quality and Sanitization
- Always verify that input FASTA files contain valid nucleotide characters (`A`, `C`, `G`, `T`, `N`, and IUPAC ambiguity codes).
- Standardize header identifiers: avoid spaces, pipes (`|`), commas, or special punctuation that break downstream tools (such as IQ-TREE, RAxML, or FastTree).
- Keep a mapping file (`.map`) if renaming long headers to short IDs to preserve traceability.

## 2. Alignment Principles (MAFFT / MUSCLE)
- For coding sequences (e.g., Influenza Hemagglutinin HA or Neuraminidase NA), check for frame shifts or premature stop codons.
- Use `--auto` for general alignment in MAFFT, or `--maxiterate 1000 --localpair` (L-INS-i) for small, highly accurate alignments (< 200 sequences).
- Document gap frequencies and distinguish true biological indels from terminal sequencing truncations.

## 3. Tree Inference Principles (IQ-TREE)
- Model selection: Default to `GTR+G4` or use ModelFinder (`-m MFP`) to evaluate the optimal substitution model using Bayesian Information Criterion (BIC).
- Support values: Recommend Ultrafast Bootstrap (`-B 1000` or `-B 10000`) combined with SH-like approximate likelihood ratio test (`-alrt 1000`) for rigorous branch support.
- Rooting: Always identify an appropriate biological outgroup (e.g., historical reference strain `A/California/07/2009` for Influenza H1N1pdm09) before interpreting clade divergence or molecular clocks. Midpoint rooting is acceptable only when no outgroup exists.

## 4. Student Guidance & Explanations
- When generating scripts or running analyses, explain the biological meaning of key parameters (e.g., transition/transversion ratio, gamma distribution shape parameter $\alpha$, ultrafast bootstrap percentages).
- Present tree outputs in an interactive, visual manner (e.g. self-contained HTML/SVG artifacts) so students can explore clades, branch lengths, and metadata without needing specialized desktop software.
