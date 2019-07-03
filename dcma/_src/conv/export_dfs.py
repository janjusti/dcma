import logging
from pathlib import Path
from StyleFrame import StyleFrame, Styler, utils

class DfExporter():
    def export_dfs(self, results_df_list, report_type, report_name, report_path):
        ### export alerts and muts df to csv/xls
        folder_path = Path.cwd() / report_path / report_name
        # extract dfs from list
        [df_mut_results, df_alert_results] = results_df_list
        # sorting by mutscores
        df_mut_results = df_mut_results.sort_values(
            by=['MutScore'], ascending=False
        ).reset_index(drop=True)
        # check if any
        df_muts_size = df_mut_results.shape[0]
        df_alert_size = df_alert_results.shape[0]
        if (df_muts_size != 0 or df_alert_size != 0):
            # check user option
            if report_type == 'csv' or report_type == 'all':
                # option 1: export to csv format
                self.df_to_csv(df_mut_results, folder_path, 'muts')
                self.df_to_csv(df_alert_results, folder_path, 'alerts')
            if report_type == 'xls' or report_type == 'all':
                # option 2: export to xls format
                df_list = [df_mut_results, df_alert_results]
                sheetname_list = ['Mutations', 'Alerts']
                self.df_to_xls(df_list, sheetname_list, folder_path)
        else:
            logging.info('WARNING: Nothing to export. Both dfs are empty.')
        if (report_type not in ['csv', 'xls', 'all']):
            logging.info('WARNING: Invalid report type.')

    def df_to_csv(self, df, folder_path, fn_suffix):
        file_path = self.ext_remover(str(folder_path), '.fasta') + '-' + fn_suffix + '.csv'
        if not df.empty: df.to_csv(file_path, index=False)

    def df_to_xls(self, list_dfs, list_sheet_names, folder_path):
        # create list of styleframes based on dfs
        list_sfs = []
        for df in list_dfs:
            list_sfs.append(StyleFrame(df))
        # apply cell patterns if any
        if not list_dfs[0].empty: self.apply_highlights_mut_rows(list_sfs[0], list_dfs[0])
        # export
        file_path = self.ext_remover(str(folder_path), '.fasta') + '-report.xlsx'
        # best_fit factors
        StyleFrame.A_FACTOR = 6
        StyleFrame.P_FACTOR = 1.3
        with StyleFrame.ExcelWriter(file_path) as writer:
            for df_idx in range(0, len(list_sfs)):
                if not list_dfs[df_idx].empty:
                    list_sfs[df_idx].to_excel(
                        writer, 
                        sheet_name=list_sheet_names[df_idx], 
                        index=False,
                        best_fit=list(list_dfs[df_idx].columns.values)
                    )

    def apply_highlights_mut_rows(self, sf, df):
        # create masks based on row mutations
        # (!) still todo
        pass
        # end

    def ext_remover(self, name, ext):
        if name[-(len(ext)):] == ext: 
            name = name[:-(len(ext))]
        return name 