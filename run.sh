python -m vida.rename_fasta_header -i BVBRC_genome_sequence.fasta -o renamed.fas -m renamed.map
mafft renamed.fas > aligned.fsa
iqtree -s aligned.fsa -B 1000 -alrt 1000 -redo
# manually modify map file
python -m vida.restore_fasta_header -i aligned.fsa.contree -o aligned_restored.fsa.contree -m renamed_modified.map
