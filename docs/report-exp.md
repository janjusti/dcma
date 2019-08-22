#### `ColNum`

First position of mutated codon, starting from 1. For example, `ColNum` 16 would be related to every codon in positions 16-17-18 in .fasta target file.

#### `PossibleCodons`

Percentage values dictionary showing the proportion of each codon on `ColNum`. Only recognized codons are listed in `PossibleCodons`; gaps and unidentified codons are also considered, but not shown (see `alerts` instead).

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