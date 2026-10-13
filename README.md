# From Sequence to Tree: Phylogenetic Analysis Workflow
> **Integrated with Google Antigravity for AI-Assisted Bioinformatics Education**

[![Workflow](https://img.shields.io/badge/Workflow-MAFFT%20%7C%20IQ--TREE%20%7C%20HTML5-blue.svg)](#workflow)
[![Model](https://img.shields.io/badge/Phylogenetics-Maximum%20Likelihood-green.svg)](#phylogenetics)
[![AI Agent](https://img.shields.io/badge/AI%20Assistant-Google%20Antigravity-purple.svg)](PROMPT_BOOK.md)

This repository provides an end-to-end curriculum and computational pipeline for taking raw genetic sequences to publication-ready phylogenetic trees. It features both a traditional automated scripting pipeline and a complete **Google Antigravity** agentic workflow for teaching modern AI-paired bioinformatics.

---

## 📚 Quick Navigation

- 📖 **[Student Tutorial (H1N1 Case Study)](TUTORIAL_ANTIGRAVITY_H1N1.md)**: Full pedagogical guide using Influenza A (H1N1pdm09) from 2009 root to 2025 isolates.
- 💬 **[Antigravity Prompt Book](PROMPT_BOOK.md)**: Exact prompt engineering recipes, stage-by-stage instructions, and autonomous agent challenges.
- 🌳 **[Interactive Tree Viewer](outputs/h1n1_interactive_tree.html)**: Interactive, web-based phylogenetic tree with metadata tooltips, clades, and search filter.
- 🧬 **[Curated H1N1 Dataset](data/h1n1/)**: Unaligned sequences, gold-standard alignment, metadata, and tree files.
- 🤖 **[Antigravity Configuration](.agents/)**: Agent rules and skills embedded in the workspace.

---

## 🌟 Key Features

1. **Influenza A (H1N1) Case Study**:
   - 30 curated representative strains spanning 16 years of viral evolution (2009 pandemic root `A/California/07/2009`, WHO vaccine strains `A/Victoria/2570/2019` and `A/Victoria/4897/2022`, global clade references, and 2023–2025 clinical isolates).
   - Demonstrates antigenic drift, clade divergence (clade 5a.2 vs 5a.2a), and vaccine match evaluation.

2. **Google Antigravity Integration**:
   - Built-in `.agents/rules/bioinfo_workflows.md` and `.agents/skills/phylogenetic-analysis/` to give Antigravity domain expertise in bioinformatics.
   - Teaches students how to formulate structured biological prompts, debug pipeline failures, and inspect alignment artifacts.

3. **Modern Interactive Visualizations**:
   - Generates standalone, dark-mode SVG/HTML5 interactive trees with search filters, branch length toggling, and metadata inspector.

4. **Self-Contained & Reproducible**:
   - Runs in seconds via MAFFT and IQ-TREE with ultrafast bootstrap support.

---

## 🚀 Quick Start

### Option A: Using Google Antigravity (AI Agent Mode)

1. Open this repository inside the **Google Antigravity IDE**.
2. Open the sidebar chat and prompt Antigravity:
   ```text
   /plan
   Please take the Influenza H1N1 HA dataset at data/h1n1/h1n1_ha_unaligned.fasta and metadata at data/h1n1/h1n1_ha_metadata.tsv, align it with MAFFT, construct a Maximum Likelihood tree with IQ-TREE, and generate an interactive HTML tree report.
   ```
3. Follow the full prompt recipes in **[PROMPT_BOOK.md](PROMPT_BOOK.md)**.

### Option B: Automated CLI Pipeline

**Step 0: Retrieve Reference Sequences from NCBI Public Database**
```bash
# Query NCBI Nucleotide for H1N1 reference and vaccine strains
python3 scripts/fetch_ncbi_sequences.py \
    -a CY121680.1 OQ719015.1 OQ718989.1 \
    -o data/h1n1/ncbi_fetched_references.fasta
```

**Step 1: Run the End-to-End Pipeline**
```bash
python3 scripts/run_pipeline.py \
    --input data/h1n1/h1n1_ha_unaligned.fasta \
    --meta data/h1n1/h1n1_ha_metadata.tsv \
    --outdir outputs \
    --threads 4
```

Inspect alignment quality and parsimony-informative sites:
```bash
python3 scripts/compare_alignment_qc.py data/h1n1/h1n1_ha_aligned.fasta
```

Generate or customize the interactive tree viewer:
```bash
python3 scripts/render_tree_interactive.py \
    data/h1n1/h1n1_ha_tree.treefile \
    data/h1n1/h1n1_ha_metadata.tsv \
    outputs/h1n1_interactive_tree.html
```

---

## 📁 Repository Structure

```
from-seq-to-tree/
├── README.md                                 # Overview and quick-start guide
├── TUTORIAL_ANTIGRAVITY_H1N1.md              # In-depth educational tutorial for students
├── PROMPT_BOOK.md                            # Antigravity prompt engineering cookbook
├── .agents/                                  # Antigravity workspace configurations
│   ├── rules/
│   │   └── bioinfo_workflows.md             # Antigravity bioinformatics rules
│   └── skills/
│       └── phylogenetic-analysis/
│           └── SKILL.md                      # Antigravity sequence analysis skill
├── data/
│   └── h1n1/
│       ├── h1n1_ha_unaligned.fasta           # 30 curated H1N1 HA sequences
│       ├── h1n1_ha_aligned.fasta             # Gold-standard MAFFT alignment
│       ├── h1n1_ha_metadata.tsv              # Epidemiological and clade metadata
│       └── h1n1_ha_tree.treefile             # Maximum Likelihood tree (IQ-TREE)
├── scripts/
│   ├── fetch_ncbi_sequences.py               # NCBI public database sequence downloader
│   ├── run_pipeline.py                       # Automated end-to-end execution script
│   ├── compare_alignment_qc.py               # Alignment metrics & QC calculator
│   └── render_tree_interactive.py            # Standalone interactive HTML tree builder
└── outputs/
    └── h1n1_interactive_tree.html            # Pre-rendered interactive visualizer
```

---

## 🔬 Background: Classic VIDA Workflow

For users utilizing legacy VIDA modules:
```bash
# 1. Rename headers and record mapping
python -m vida.rename_fasta_header -i BVBRC_genome_sequence.fasta -o renamed.fas -m renamed.map

# 2. Alignment
mafft renamed.fas > aligned.fsa

# 3. Tree construction
iqtree -s aligned.fsa -B 1000 -alrt 1000 -redo

# 4. Restore original names
python -m vida.restore_fasta_header -i aligned.fsa.contree -o aligned_restored.fsa.contree -m renamed_modified.map
```

> 🌐 **Searching the NCBI Public Database**:
> Go directly to the **[NCBI Nucleotide database](https://www.ncbi.nlm.nih.gov/nucleotide/)** or **[NCBI Virus portal](https://www.ncbi.nlm.nih.gov/labs/virus/)** to search for reference genomes and target genes (e.g., searching by organism `Influenza A virus`, host `Homo sapiens`, and segment `HA`). Use these accession numbers to retrieve reference coordinates or root outgroups.

---

## 📜 License & Citation

Distributed for academic and educational research. When using this workflow or tutorial for courses, please credit the repository maintainer and reference the underlying tools:
- **MAFFT**: Katoh et al. *Nucleic Acids Res.* 30(14): 3059–3066.
- **IQ-TREE**: Minh et al. *Mol. Biol. Evol.* 37(5): 1530–1534.
