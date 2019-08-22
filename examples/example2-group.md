# Example 2 - Group Execution

Open terminal and create a new folder.

```bash
mkdir dcma-examples
```

Get inside `dcma-examples` and download `ExGroup` module.

```bash
cd dcma-examples
wget https://github.com/janjusti/dcma/raw/master/example/ExGroup.py
```

Open Python3 from terminal.

```bash
python3
Python 3.6.7 (default, Oct 22 2018, 11:32:17) 
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

Import all functions from `ExGroup` module.

```python
>>> from ExGroup import *
```

This example will use four different genes of HPV 16 (E6), extracted from [GenBank](https://www.ncbi.nlm.nih.gov/genbank/) and identified arbitrarily as Group A ([KC662553.1](https://www.ncbi.nlm.nih.gov/nuccore/KC662553.1) and [KC662552.1](https://www.ncbi.nlm.nih.gov/nuccore/KC662552.1)) and Group B ([KM058604.1](https://www.ncbi.nlm.nih.gov/nuccore/KM058604.1) and [KM058603.1](https://www.ncbi.nlm.nih.gov/nuccore/KM058603.1)).

Generate .fasta files from ID list for each group.

```python
>>> groupA_ids = ['KC662553.1', 'KC662552.1']
>>> groupB_ids = ['KM058604.1', 'KM058603.1']
>>> generate_fasta_from_ids(groupA_ids, 'groupA-unaligned.fasta')
KC662553.1 successfully fetched.
KC662552.1 successfully fetched.
groupA-unaligned.fasta sucessfully created.
>>> generate_fasta_from_ids(groupB_ids, 'groupB-unaligned.fasta')
KM058604.1 successfully fetched.
KM058603.1 successfully fetched.
groupB-unaligned.fasta sucessfully created.
```

Align all sequences with any Multiple Sequence Alignment (MSA) software. In this case, [MUSCLE](https://www.drive5.com/muscle/) is used.

```python
>>> align_via_muscle('groupA-unaligned.fasta', 'groupA.fasta')
Alignment groupA-unaligned.fasta > groupA.fasta done.
>>> align_via_muscle('groupB-unaligned.fasta', 'groupB.fasta')
Alignment groupB-unaligned.fasta > groupB.fasta done.
```

Get consensus sequence for each group and generate a new .fasta file with both of them.

```python
>>> seqA = get_consensus_seq('groupA.fasta', 'groupA_any_sentence')
'groupA_any_sentence' consensus sequence generated (original: groupA.fasta)
>>> seqB = get_consensus_seq('groupB.fasta', 'groupB_any_sentence')
'groupB_any_sentence' consensus sequence generated (original: groupB.fasta)
>>> write_fasta('groupAB-cons.fasta', [seqA, seqB])
groupAB-cons.fasta successfully written.
```

Align all consensus sequences from previous step.

```python
>>> align_via_muscle('groupAB-cons.fasta', 'groups-target.fasta')
Alignment groupAB-cons.fasta > groups-target.fasta done.
```

In this example, "any sentence" is being used as *searchable keyphrase*. If there is any unrecognised codon (containing any non-generic symbol [not recognised by IUPAC](https://www.bioinformatics.org/sms2/iupac.html)) in any consensus sequence, DCMA will search for matching codons in original files. 

*e.g.*: an unrecognised codon (XAT, position 94-95-96) is found in `groupB_any_sentence` sequence. DCMA will look into `groupB.fasta` to check which codons XAT could be. 

This feature works for any amount of levels, as long as the sequence's name containing an unrecognised codon has a searchable keyphrase settled. If there is not any other searchable sequence to check, this unrecognised codon will be considered as "pure" in `alerts`.

Finally, analysis results are obtained from dcma's solver.

```python
>>> results = solver.run('groups-target.fasta', searchable_keyphrase='any sentence')
>>> solver.export(results, 'csv', 'groups')
```

## Output ([More details](../docs/report-exp.md))

### `groups-muts.csv`

| ColNum | PossibleCodons               | PossibleMuts     | PossiblePols               | GenScore |
|--------|------------------------------|------------------|----------------------------|----------|
| 94     | "{'GAT': 0.75, 'CAT': 0.25}" | {'Mis': 0.06176} | "{'Pp': 0.25, 'Pn': 0.75}" | 12.30298 |
| 268    | "{'GTG': 0.25, 'TTG': 0.75}" | {'Mis': 0.06176} | {'Np': 1.0}                | 12.22848 |
| 16     | "{'ACG': 0.25, 'ACT': 0.25}" | {'Sil': 0.16667} | {'Nc': 0.5}                | 0.0165   |

### `groups-alerts.csv`

All gaps and unidentified codons are listed in this file.

| SeqName             | ColNum | AlertType   |
|---------------------|--------|-------------|
| groupA any sentence | 1      | Pure \-\-\- |
| groupA any sentence | 4      | Pure \-\-\- |
| groupA any sentence | 7      | Pure \-\-\- |
| groupA any sentence | 10     | Pure \-\-\- |
| \.\.\.              | \.\.\. | \.\.\.      |
| groupA any sentence | 466    | Pure \-\-\- |
| groupA any sentence | 469    | Pure \-\-\- |
| groupA any sentence | 472    | Pure \-\-\- |
| groupA any sentence | 475    | Pure \-\-\- |