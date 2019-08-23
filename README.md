# Deep Codon Mutation Analyser (DCMA)

DCMA analyses each column of codons within .fasta files, from a target file, generating a report with all possible mutations listed.

## Installation
```bash
pip install dcma
```

## Examples

- [Simple Execution](examples/example1-simple.md)
- [Group Execution](examples/example2-group.md)

## Usage
### Command Line

```bash
usage: run-dcma [-h] [--reportName REPORTNAME] [--reportPath REPORTPATH]
                [--searchKP SEARCHKP] [--debug]
                TARGET REPORTTYPE

Analyse mutation on all nucleotide alignment .fasta files from a target.

positional arguments:
  TARGET                Target .fasta file to be analysed.
  REPORTTYPE            Output report file type.

optional arguments:
  -h, --help            show this help message and exit
  --reportName REPORTNAME
                        Output report custom file name.
  --reportPath REPORTPATH
                        Output report custom file path.
  --searchKP SEARCHKP   Custom keyphrase to detect searchable sequences.
  --debug               Turn debug messages on.
```

### Python

```python
import dcma.core as solver

target_path = 'example.fasta'
report_name = 'myrep'
report_type = 'all' # 'xls', 'csv' or 'all'
report_path = 'results-folder' # optional

solver.set_debug_mode(True) # optional

# results[0] -> polarity results dataframe
# results[1] -> alerts dataframe
results = solver.run(target_path)

# option 1: export to the current folder
solver.export(results, report_type, report_name)
# option 2: export to custom folder
solver.export(results, report_type, report_name, report_path)
```