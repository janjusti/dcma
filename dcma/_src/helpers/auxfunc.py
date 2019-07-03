from pathlib import Path
from Bio.SeqIO import FastaIO
from anytree import AnyNode, LevelOrderGroupIter
import string
import logging

class AuxFuncPack:
    # package of custom functions

    def fasta_to_list(self, fasta_fn):
        ### convert .fasta file into a list
        filepath = Path.cwd() / fasta_fn
        # original list format: [(name, seq)]
        fasta_list = list(FastaIO.SimpleFastaParser(open(filepath)))
        # converting to list of lists (instead of list of tuples)
        fasta_list = list(map(list, fasta_list))
        # replace underscores for spaces
        for fasta_idx in range(0, len(fasta_list)):
            fasta_list[fasta_idx][0] = fasta_list[fasta_idx][0].replace('_', ' ')                
        # check if all sequences have the same size
        sizes_list = []
        for fasta_idx in range(0, len(fasta_list)):
            sizes_list.append(len(fasta_list[fasta_idx][1]))
        if not all(x == sizes_list[0] for x in sizes_list):
            logging.getLogger().info(f'WARNING: .fasta file has inconsistency: {fasta_fn}')
        # check if all sequences have well-defined codons
        # (!) what if it has gaps?
        # for fasta_idx in range(0, len(fasta_list)):
        #     if (sizes_list[fasta_idx] % 3 != 0):
        #         logging.getLogger().info(
        #             f'WARNING: incorrect number of nucleotides in {fasta_list[fasta_idx][0]}'
        #         )

        return fasta_list
    
    def add_alert_on_df(self, df_alert, seq_name, col_num, alert_type_str):
        df_alert = df_alert.append(
            {
                'SeqName': seq_name,
                'ColNum': col_num+1,
                'AlertType': alert_type_str
            }
        , ignore_index=True)

        return df_alert

    def deep_searcher(self, fasta_folder, fasta_list, col_num, df_alert, searchable_keyphrase):
        # create local root
        loc_root = AnyNode(name='LocRoot', codon='LocRootCodon')
        # create nodes from column number
        for row in range(0, len(fasta_list)):
            AnyNode(
                name=fasta_list[row][0],
                codon=fasta_list[row][1][col_num:col_num+3],
                parent=loc_root
            )
        # run through nodes
        for node in loc_root.children:
            # check if codon is possibly searchable
            codon_unknown_chars = set(node.codon).difference(set(['A', 'C', 'T', 'G']))
            if len(codon_unknown_chars) != 0:
                isCodonWithSpecialChar = (any([x in codon_unknown_chars for x in ['-', '?']]))
                if searchable_keyphrase in node.name and not isCodonWithSpecialChar:
                    # non-gap searchable codon
                    fasta_dict = dict(fasta_list)
                    # check previous number of gaps from sequence
                    num_gaps = fasta_dict[node.name][:col_num].count('-')
                    # shift column number to the correct one
                    shifted_col_num = col_num-num_gaps
                    # get fasta_list of this node's original sequence
                    deeper_fn = node.name.replace((' ' + searchable_keyphrase),'') + '.fasta'
                    deeper_path = str(fasta_folder) + '/' + deeper_fn
                    deeper_list = self.fasta_to_list(deeper_path)
                    # go deeper
                    deeper_result = self.deep_searcher(
                        fasta_folder, deeper_list, shifted_col_num, df_alert, searchable_keyphrase
                    )
                    deeper_result[0].parent = node
                    df_alert = deeper_result[1]
                else:
                    # non-searchable codon, increment on df_alert
                    df_alert = self.add_alert_on_df(
                        df_alert, 
                        node.name,
                        col_num, 
                        'Pure ' + node.codon
                    )        

        return loc_root, df_alert

    def get_codons_perc_dict(self, root, codons_list):
        ### convert list of codons to dict (codon -> its perc)
        # get list of codons levels
        codons_levels = [[node.codon for node in children] for children in LevelOrderGroupIter(
            root,
            filter_=lambda n: n.codon != 'LocRootCodon'
        )]
        # clear any empty lists (parent roots)
        codons_levels = [x for x in codons_levels if x]
        codons_dict = {}
        for target_codon in codons_list:
            total_perc = 0
            deepness_perc = 1
            for level in codons_levels:
                codon_perc_on_lvl = (level.count(target_codon)/len(level))
                total_perc = total_perc + (codon_perc_on_lvl)*deepness_perc
                num_of_deepables = sum([len(set(codon).difference(set(['A', 'C', 'T', 'G']))) for codon in level])
                deepables_perc_on_lvl = (num_of_deepables/len(level))
                deepness_perc = deepness_perc * deepables_perc_on_lvl
            codons_dict[target_codon] = round(100*total_perc,3)

        return codons_dict

    def get_mutations_perc_dict(self, codons_dict, df_codons):
        ### detect mutation types between codons
        # case 1: silent mutation (Sil) -> no amino change between diff codons
        # case 2: missense mutation (Mis) -> amino change between diff codons
        # case 3: nonsense mutation (Non) -> stop codons between diff codons
        muts_dict = {}
        print(df_codons)
        print(codons_dict)

        return muts_dict

    def get_aminos_from_codons(self, codons_dict, df_aminos):
        ### translate codons into aminos        
        aminos_dict = {}
        for codon_name, codon_perc in codons_dict.items():
            codon_amino = df_aminos.loc[df_aminos['Codon'] == codon_name, 'Amino'].iat[0]
            aminos_dict[codon_amino] = aminos_dict.get(codon_amino, 0) + codon_perc

        return aminos_dict

    def get_polarities_perc_dict(self, aminos_dict, df_pols):
        ### get dict of polarities within aminos list
        # get list of tuples (pol_type -> perc)
        list_percs = []
        for curr_pol in range(0, df_pols.shape[0]):
            pol_amino_list = list(df_pols.Amino.at[curr_pol])
            for curr_amino in list(aminos_dict.items()):
                if curr_amino[0] in pol_amino_list:
                    list_percs.append((df_pols.Type.at[curr_pol], curr_amino[1]))
        # convert into unified dict
        pols_dict = {}
        for key, value in list_percs:
            pols_dict[key] = round(pols_dict.get(key, 0) + value, 2)

        return pols_dict

    def get_mut_score(self, muts_dict, pols_dict, df_codons, df_pols):
        ### calculate mutation score
        # (!) still todo
        mut_score = 0

        return mut_score