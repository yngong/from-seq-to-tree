# VIDA Phylogenetic Analysis Workflow

This repository provides a step-by-step workflow for conducting phylogenetic analysis using **VIDA** tools and external software.

## Workflow

1. **Download sequences**
   - Download sequences with a length greater than 6500, collected after 2020.

2. **Rename FASTA headers**
   ```bash
   python -m vida.rename_fasta_header -i BVBRC_genome_sequence.fasta -o renamed.fas -m renamed.map
   ```

3. **Multiple sequence alignment**
   ```bash
   mafft input_file > output_file
   ```

4. **Quality check**
   - Use any sequence viewer (e.g., BioEdit or Seqotron) and trim as VP1 sequences.

   > **Note**: Go to the NCBI nucleotide database to search for any reference for reexamining the genomic coordinates/position (Python).

5. **Tree construction**
   ```bash
   iqtree -s alignment.fasta -B 1000 -alrt 1000
   ```

6. **Manually modify the map file**
   - Shorten the header length.

7. **Restore original names in the tree file**
   ```bash
   python -m vida.restore_fasta_header -i aligned.fsa.contree -o aligned_restored.fsa.contree -m renamed_modified.map
   ```

8. **Visualization**
   - View your tree file (`aligned_restored.fsa.contree`) in **FigTree**.

## Notes

- Ensure your **Conda environment** is working correctly (e.g., within WSL on Windows).

