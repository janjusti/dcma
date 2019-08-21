# Example 1 - Simple Execution

Open terminal and create a new folder.

```bash
mkdir dcma-examples
```

Get inside `dcma-examples` and download `ExSimple` module.

```bash
cd dcma-examples
wget https://github.com/janjusti/dcma/raw/master/example/ExSimple.py
```

Open Python3 from terminal.

```bash
python3
Python 3.6.7 (default, Oct 22 2018, 11:32:17) 
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

Import all functions from `ExSimple` module.

```python
>>> from ExSimple import *
```

This example will use four different genes of HPV 16 (E6), extracted from [GenBank](https://www.ncbi.nlm.nih.gov/genbank/) and identified as [KC662553.1](https://www.ncbi.nlm.nih.gov/nuccore/KC662553.1), [KC662552.1](https://www.ncbi.nlm.nih.gov/nuccore/KC662552.1), [KM058604.1](https://www.ncbi.nlm.nih.gov/nuccore/KM058604.1) and [KM058603.1](https://www.ncbi.nlm.nih.gov/nuccore/KM058603.1).

Generate .fasta file from ID list.

```python
>>> id_list = ['KC662553.1', 'KC662552.1', 'KM058604.1', 'KM058603.1']
>>> generate_fasta_from_ids(id_list, 'simple-unaligned.fasta')
KC662553.1 successfully fetched.
KC662552.1 successfully fetched.
KM058604.1 successfully fetched.
KM058603.1 successfully fetched.
simple-unaligned.fasta sucessfully created.
```

Align all sequences with any Multiple Sequence Alignment (MSA) software. In this case, [MUSCLE](https://www.drive5.com/muscle/) is used.

```python
>>> align_via_muscle('simple-unaligned.fasta', 'simple.fasta')
Alignment simple-unaligned.fasta -> simple.fasta done.
```

Finally, analysis results are obtained from dcma's solver.

```python
>>> results = solver.run('simple.fasta')
>>> solver.export(results, 'csv', 'simple')
```

---

## simple-muts.csv

| ColNum | PossibleCodons               | PossibleMuts     | PossiblePols               | GenScore |
|--------|------------------------------|------------------|----------------------------|----------|
| 94     | "{'GAT': 0.75, 'CAT': 0.25}" | {'Mis': 0.06176} | "{'Pp': 0.25, 'Pn': 0.75}" | 12.30298 |
| 268    | "{'GTG': 0.25, 'TTG': 0.75}" | {'Mis': 0.06176} | {'Np': 1.0}                | 12.22848 |
| 16     | "{'ACG': 0.25, 'ACT': 0.25}" | {'Sil': 0.16667} | {'Nc': 0.5}                | 0.0165   |

#### `ColNum`

First position of mutated codon, starting from 1. For example, `ColNum` 16 would be related to every codon in positions 16-17-18 in `simple.fasta`.

#### `PossibleCodons`

Percentage values dictionary showing the proportion of each codon on `ColNum`. Gaps and unidentified codons are also considered, as seen in `ColNum` 16, where half of analysed codons are not real codons.

#### `PossibleMuts`

Percentage values dictionary showing mutation scores for each mutation type.

* `Sil` (Silent)

Best-case scenario (close to 0): only one different codon between all codons, generating the same amino acid.

Worst-case scenario (1): all possible codons for the same amino, in equal proportions.

* `Mis` (Missense)

Best-case scenario (close to 0): only one different amino acid being generated through a single different codon, between all codons.

Worst-case scenario (1): all possible amino acids being generated, in equal proportions.

* `Non` (Nonsense)

Best-case scenario (close to 0): only one stop codon between all codons.

Worst-case scenario (1): half of codons are stop codons.

#### `PossiblePols`

Percentage values dictionary showing the proportion of polarity from each amino acid generated from all codons listed on `PossibleCodons`. Score values are used to calculate `PolScore`.

| Type | Name               | Score |
|------|--------------------|-------|
| Pp   | Positive Polar     | 1     |
| Pn   | Negative Polar     | 1     |
| Nc   | Neutral Polar      | 0     |
| Np   | Neutral Non\-polar | 0     |

#### `GenScore`

General score is based on two scores: mutation and polarity score.

```math
GenScore = 0.99*MutScore + 0.01*PolScore
```

* `MutScore`

Mutation score is calculated based on each percentage from mutation type occurrence (`PossibleMuts`).

```math
MutScore = SilPerc*0.1 + MisPerc*200 + NonPerc*200
```

* `PolScore`

Polarity score is calculated using score's sum of all existent polarities on `PossiblePols` (`SumScores`), length of `PossiblePols` size (`PolListSize`) and smallest percentage value between all existent polarities (`MinPolsPerc`).

```math
PolScore = SumScores*3 + PolListSize*0.6 + MinPolsPerc
```

---

## simple-alerts.csv

All unidentified codons and gaps are listed in this file.

| SeqName                                                                              | ColNum | AlertType   |
|--------------------------------------------------------------------------------------|--------|-------------|
| "KC662552\.1 Human papillomavirus type 16 isolate B3620 E6 \(E6\) gene, partial cds" | 1      | Pure \-\-\- |
| "KC662553\.1 Human papillomavirus type 16 isolate B2995 E6 \(E6\) gene, partial cds" | 1      | Pure \-\-\- |
| "KC662552\.1 Human papillomavirus type 16 isolate B3620 E6 \(E6\) gene, partial cds" | 4      | Pure \-\-\- |
| "KC662553\.1 Human papillomavirus type 16 isolate B2995 E6 \(E6\) gene, partial cds" | 4      | Pure \-\-\- |
| \.\.\.                                                                               | \.\.\. | \.\.\.      |
| "KC662552\.1 Human papillomavirus type 16 isolate B3620 E6 \(E6\) gene, partial cds" | 472    | Pure \-\-\- |
| "KC662553\.1 Human papillomavirus type 16 isolate B2995 E6 \(E6\) gene, partial cds" | 472    | Pure \-\-\- |
| "KC662552\.1 Human papillomavirus type 16 isolate B3620 E6 \(E6\) gene, partial cds" | 475    | Pure \-\-\- |
| "KC662553\.1 Human papillomavirus type 16 isolate B2995 E6 \(E6\) gene, partial cds" | 475    | Pure \-\-\- |