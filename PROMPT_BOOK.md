# Google Antigravity Prompting Cookbook: From Sequences to Tree

A comprehensive guide for students and instructors on how to effectively prompt **Google Antigravity** to execute, troubleshoot, and interpret phylogenetic analyses using Influenza A (H1N1pdm09) as a case study.

---

## 1. Understanding Google Antigravity in Bioinformatics

Google Antigravity is an **AI-first agentic paired programming environment**. Unlike a standard web chatbot that only returns text, Antigravity can:
1. **Directly inspect your workspace files** (FASTA files, alignments, metadata).
2. **Execute shell tools** (`mafft`, `iqtree`, `python3`, `git`).
3. **Diagnose and heal errors** automatically if a script or pipeline fails.
4. **Generate rich visual artifacts** (interactive HTML trees, publication charts, markdown reports).
5. **Formulate step-by-step plans** before running expensive computational tasks.

### Golden Rules of Agent Prompting
- **Be Specific About File Paths**: Tell the agent where your data lives (e.g., `data/h1n1/h1n1_ha_unaligned.fasta`) rather than saying "analyze my sequences".
- **Define Biological Intent**: Specify whether you need a quick Neighbor-Joining tree or a rigorous Maximum Likelihood tree with bootstrap support.
- **Request Verifiable Artifacts**: Ask the agent to produce tangible outputs (e.g., summary tables, HTML visualizers, log files).
- **Use Slash Commands**:
  - `/plan`: Request Antigravity to lay out a multi-phase execution plan before modifying any code or running heavy tree searches.
  - `/goal`: Command Antigravity to run an autonomous end-to-end task without stopping until verification succeeds.

---

## 2. Step-by-Step Prompt Recipes (Stage-by-Stage)

### Stage 0: Finding and Downloading Sequences from the NCBI Public Database

#### 🌐 Where to Search in NCBI:
Students must explicitly retrieve reference and surveillance sequences from public NCBI databases:
1. **NCBI Virus Portal**: [https://www.ncbi.nlm.nih.gov/labs/virus/](https://www.ncbi.nlm.nih.gov/labs/virus/)
   - Virus: *Influenza A virus (taxid:11320)*
   - Serotype: *H1N1*
   - Segment: *Segment 4 (Hemagglutinin / HA)*
   - Host: *Homo sapiens (human)*
   - Nucleotide Completeness: *Complete CDS (approx. 1,700 bp)*
2. **NCBI Nucleotide / GenBank**: [https://www.ncbi.nlm.nih.gov/nucleotide/](https://www.ncbi.nlm.nih.gov/nucleotide/)
   - **Pandemic 2009 Root Reference**: Accession `CY121680.1` (`A/California/07/2009`)
   - **WHO 2019–2021 Vaccine Reference**: Accession `OQ719015.1` (`A/Victoria/2570/2019`)
   - **WHO 2022–2025 Vaccine Reference**: Accession `OQ718989.1` (`A/Victoria/4897/2022`)

#### 💬 Copy-Paste Prompt for Antigravity:
```text
I need to retrieve reference sequences for Influenza A (H1N1pdm09) from the NCBI public database (GenBank / NCBI Nucleotide).

Please do the following:
1. Search and download the following official reference sequences from NCBI via BioPython Entrez or using scripts/fetch_ncbi_sequences.py:
   - Root Reference: CY121680.1 (A/California/07/2009)
   - 2019 Vaccine Reference: OQ719015.1 (A/Victoria/2570/2019)
   - 2022 Vaccine Reference: OQ718989.1 (A/Victoria/4897/2022)
2. Save the downloaded sequences to data/h1n1/ncbi_fetched_references.fasta.
3. Verify that the downloaded records contain complete Hemagglutinin (HA) coding sequences (~1,700 bp).
```

---

### Stage 1: Dataset Quality Check & Inspection

#### 🎯 Goal:
Inspect raw FASTA files, verify taxa count, check sequence lengths, identify ambiguous bases (`N`), and check header formatting.

#### 💬 Copy-Paste Prompt:
```text
I have a FASTA file containing unaligned Influenza A (H1N1) Hemagglutinin sequences located at data/h1n1/h1n1_ha_unaligned.fasta and a metadata table at data/h1n1/h1n1_ha_metadata.tsv.

Please perform an initial quality control check on this dataset:
1. Parse the FASTA file and report total sequence count, minimum, maximum, and average sequence lengths.
2. Check for ambiguous bases ('N' or other IUPAC codes) and flag any sequences with high ambiguity (>10%).
3. Verify that FASTA headers match the strain identifiers in the metadata file.
4. Summarize your findings in a clear markdown table.
```

---

### Stage 2: Multiple Sequence Alignment (MSA) with MAFFT

#### 🎯 Goal:
Align the nucleotide sequences and evaluate alignment quality and gap distribution.

#### 💬 Copy-Paste Prompt:
```text
Please run a multiple sequence alignment on data/h1n1/h1n1_ha_unaligned.fasta:
1. Use MAFFT with automated parameter selection (--auto) and output the alignment to data/h1n1/h1n1_ha_aligned.fasta.
2. Run scripts/compare_alignment_qc.py to evaluate alignment statistics (total aligned length, percentage of constant sites, variable sites, and parsimony-informative sites).
3. Report whether any terminal trimming is necessary and confirm whether the sequences align without major frameshift anomalies.
```

---

### Stage 3: Maximum Likelihood Tree Reconstruction with IQ-TREE

#### 🎯 Goal:
Construct a rigorous Maximum Likelihood phylogenetic tree with model selection and bootstrap support.

#### 💬 Copy-Paste Prompt:
```text
Please reconstruct a phylogenetic tree from the aligned sequences data/h1n1/h1n1_ha_aligned.fasta using IQ-TREE:
1. Use the General Time Reversible model with Gamma rate heterogeneity (GTR+G) or run ModelFinder (-m MFP).
2. Set 1,000 ultrafast bootstrap replicates (-B 1000) for branch support estimation.
3. Save the output files with prefix outputs/h1n1_ha_tree.
4. Once completed, inspect the .iqtree log and report:
   - Selected nucleotide substitution model and log-likelihood score.
   - Base frequencies (A, C, G, T) and transition/transversion rate ratios.
   - Gamma distribution shape parameter (alpha).
```

---

### Stage 4: Outgroup Rooting & Molecular Clock Dating

#### 🎯 Goal:
Re-root the unrooted tree using the 2009 pandemic reference strain to reconstruct true evolutionary directionality.

#### 💬 Copy-Paste Prompt:
```text
In outputs/h1n1_ha_tree.treefile, we have an unrooted Maximum Likelihood tree. 

Please:
1. Use BioPython or DendroPy to re-root this tree using A/California/07/2009_REF_NextstrainRoot as the biological outgroup.
2. Verify that the recent circulating strains (e.g., 2023-2025 isolates) and vaccine strains (A/Victoria/2570/2019 and A/Victoria/4897/2022) are positioned correctly on the ingroup branches relative to the 2009 root.
3. Save the re-rooted tree as outputs/h1n1_rooted_tree.nwk.
```

---

### Stage 5: Interactive Visualization & Annotation

#### 🎯 Goal:
Build an interactive HTML tree dashboard integrating metadata (sampling date, geographic location, vaccine vs clinical isolate).

#### 💬 Copy-Paste Prompt:
```text
Please generate an interactive, publication-quality HTML tree viewer for outputs/h1n1_ha_tree.treefile and metadata data/h1n1/h1n1_ha_metadata.tsv:
1. Execute scripts/render_tree_interactive.py to generate outputs/h1n1_interactive_tree.html.
2. Ensure the viewer includes:
   - Search/filter bar for strain names.
   - Toggle between phylogram (real branch lengths) and cladogram.
   - Color coding for clinical isolates (Taiwan 2023-2025), WHO vaccine strains, and reference roots.
   - Interactive tooltips showing strain name, date, country, and accession numbers.
3. Provide me with instructions on how to open and interact with this file.
```

---

### Stage 6: Biological Interpretation & Clade Assignment

#### 🎯 Goal:
Translate phylogenetic topology into biological insights regarding antigenic evolution.

#### 💬 Copy-Paste Prompt:
```text
Based on the generated phylogenetic tree and metadata:
1. Identify which clade the recent 2023-2025 clinical isolates (e.g. Taiwan barcode specimens) cluster with.
2. Are these clinical isolates more closely related to the 2019 vaccine strain (A/Victoria/2570/2019) or the 2022-2024 updated vaccine strain (A/Victoria/4897/2022)?
3. Explain the evolutionary significance of this clustering in the context of seasonal influenza vaccine selection and antigenic drift.
```

---

## 3. The "Autonomous End-to-End" Challenge Prompt

For advanced students who want Antigravity to perform the entire pipeline autonomously using planning mode:

#### 💬 Master Prompt:
```text
/plan
You are an expert bioinformatician and evolutionary virologist.

We want to conduct an autonomous, end-to-end phylogenetic analysis for Influenza A (H1N1pdm09) from public databases to an annotated evolutionary tree:
1. Search and retrieve the official reference sequences from the NCBI public database (GenBank / NCBI Nucleotide):
   - Pandemic Root: CY121680.1 (A/California/07/2009)
   - 2019 Vaccine Reference: OQ719015.1 (A/Victoria/2570/2019)
   - 2022 Vaccine Reference: OQ718989.1 (A/Victoria/4897/2022)
2. Integrate these NCBI references with the local clinical isolate dataset at data/h1n1/h1n1_ha_unaligned.fasta and metadata at data/h1n1/h1n1_ha_metadata.tsv.
3. Conduct sequence QC, verify lengths, and align using MAFFT (--auto).
4. Inspect the alignment for constant and parsimony-informative sites using scripts/compare_alignment_qc.py.
5. Construct a Maximum Likelihood phylogenetic tree with IQ-TREE (GTR+G, 1000 ultrafast bootstraps).
6. Re-root the tree on the NCBI 2009 pandemic reference strain (A/California/07/2009).
7. Generate an interactive HTML tree visualization with metadata linking via scripts/render_tree_interactive.py.
8. Produce a concise markdown summary report analyzing the tree topology, bootstrap support, and the evolutionary drift between recent clinical isolates and WHO vaccine strains.

Please present your execution plan first, and proceed step by step.
```

---

## 4. Troubleshooting & Self-Healing Prompts

| Problem Encountered | Ineffective Prompt | Recommended Antigravity Prompt |
| :--- | :--- | :--- |
| **Tool missing in PATH** | "IQ-TREE didn't run, fix it." | `"IQ-TREE returned command not found. Check if iqtree or fasttree is installed in the active conda environment or system PATH (/home/yngong/miniconda3/bin/iqtree), and adjust your execution script accordingly."` |
| **Header name parsing error** | "There is a syntax error in the Newick tree." | `"The tree building tool threw an error due to invalid characters in the FASTA header. Please sanitize the FASTA headers, maintain an ID mapping table, re-run the tree reconstruction, and restore the human-readable names afterward."` |
| **High gap proportion** | "Why is the alignment strange?" | `"Taxon A/California/07/2009 has ~63% gaps in the alignment. Inspect whether this is due to partial gene coverage (e.g., HA1 coding region vs full-length HA precursor) or alignment mispairing, and explain its impact on tree inference."` |
| **Low bootstrap branch support** | "The tree has low numbers." | `"Several internal branches have bootstrap support < 70. Identify which nodes these are, explain why closely related seasonal influenza strains often exhibit low phylogenetic resolution, and suggest whether whole-genome concatenation would improve node support."` |

---

## 5. Summary Checklist for Students

- [ ] Data checked with `scripts/compare_alignment_qc.py`.
- [ ] Alignment saved in `outputs/` or `data/h1n1/`.
- [ ] ML tree constructed with ultrafast bootstrap $\ge 1000$.
- [ ] Rooted on `A/California/07/2009` outgroup.
- [ ] Interactive HTML report generated and inspected.
- [ ] Evolutionary conclusions documented.
