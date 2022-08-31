import pandas as pd
import numpy as np
import warnings
from pandas.errors import DtypeWarning

warnings.filterwarnings("ignore", category=DtypeWarning)


class DataLoader():
    def __init__(self, path='data/data.csv'):
        self.df = pd.read_csv(path)
        self.clean_data()

    def clean_data(self):
        self.df.sort_values(by=['pl_name', 'disc_year'], inplace=True)
        self.df.drop_duplicates(subset=['pl_name'], keep='first', inplace=True)
        massJIt = list(zip(self.df['pl_massj'], self.df['pl_msinij']))
        massJ = [x0 if np.isfinite(x0) else x1 for (x0, x1) in massJIt]
        self.df['planetMassJ'] = massJ
        massEIt = list(zip(self.df['pl_masse'], self.df['pl_msinie']))
        massE = [x0 if np.isfinite(x0) else x1 for (x0, x1) in massEIt]
        self.df['planetMassE'] = massE

        drop_cols = ['rowid', 'pl_letter', 'hd_name', 'hip_name', 'tic_id', 'gaia_id', 'sy_pnum', 'sy_mnum',
                     'default_flag',
                     'cb_flag', 'disc_refname', 'disc_pubdate', 'disc_telescope', 'disc_instrument', 'soltype',
                     'pl_controv_flag', 'pl_refname', 'pl_cmasse', 'pl_cmassj', 'pl_bmasse', 'pl_bmassj',
                     'pl_bmassprov',
                     'pl_insol', 'pl_orbincl', 'pl_tranmid', 'pl_tsystemref', 'ttv_flag', 'pl_imppar', 'pl_trandep',
                     'pl_trandur', 'pl_ratror', 'pl_occdep', 'pl_orbtper', 'pl_orblper', 'pl_rvamp', 'pl_projobliq',
                     'pl_trueobliq', 'st_refname', 'st_teff', 'st_met', 'st_metratio', 'st_lum', 'st_logg', 'st_age',
                     'st_dens',
                     'st_vsin', 'st_rotp', 'st_radv', 'sy_refname', 'rastr', 'ra', 'decstr', 'dec', 'glat', 'glon',
                     'elat',
                     'elon', 'sy_pm', 'sy_pmra', 'sy_pmdec', 'sy_plx', 'sy_bmag', 'sy_vmag', 'sy_jmag', 'sy_hmag',
                     'sy_kmag',
                     'sy_umag', 'sy_gmag', 'sy_rmag', 'sy_imag', 'sy_zmag', 'sy_w1mag', 'sy_w2mag', 'sy_w3mag',
                     'sy_w4mag', 'rv_flag', 'pul_flag', 'ptv_flag', 'micro_flag', 'etv_flag', 'ima_flag', 'dkin_flag',
                     'sy_gaiamag', 'sy_icmag', 'sy_tmag', 'sy_kepmag', 'pl_pubdate', 'releasedate', 'pl_nnotes',
                     'st_nphot', 'pl_msinij', 'pl_msinie', 'pl_masse', 'pl_massj', 'st_spectype',
                     'st_nrvc', 'st_nspec', 'pl_nespec', 'pl_ntranspec', 'pl_ratdor', 'rowupdate']

        self.df.drop(columns=drop_cols, inplace=True)
        new_col_names = {'pl_name': 'planetName', 'hostname': 'starName', 'sy_snum': 'numStars',
                         'discoverymethod': 'discoveryMethod', 'disc_year': 'discoveryYear',
                         'disc_locale': 'discoveryLocale',
                         'disc_facility': 'discoveryFacility', 'pl_orbper': 'orbitalPeriod',
                         'pl_orbsmax': 'orbitSemiMaj', 'pl_rade': 'planetRadE', 'pl_radj': 'planetRadJ',
                         'pl_masse': 'planetMassE', 'pl_massj': 'planetMassJ', 'pl_dens': 'planetDens',
                         'pl_orbeccen': 'planetEcce', 'pl_eqt': 'planetEqtT',
                         'st_rad': 'starRadius', 'st_mass': 'starMass', 'sy_dist': 'starDistance'}
        self.df.rename(columns=new_col_names, inplace=True)
        self.df.set_index('planetName', drop=True, inplace=True)
        earth_df = pd.DataFrame.from_dict({"Earth": {'starName': 'Sun', 'numStars': 1, 'discoveryMethod': 'N/A',
                                             'discoveryYear': np.NaN, 'discoveryLocale': 'N/A',
                                             'discoveryFacility': 'N/A', 'orbitalPeriod': 365.25,
                                             'orbitSemiMaj': 1, 'planetRadE': 1, 'planetRadJ': 0.0892,
                                             'planetDens': 5.51, 'planetEcce': 0.017, 'planetEqtT': 255,
                                             'starRadius': 1, 'starMass': 1, 'starDistance': 0, 'planetMassJ': 0.003145,
                                             'planetMassE': 1}}).T
        self.df = pd.concat([self.df, earth_df])
        self.df.sort_index(inplace=True)

    def get_data(self):
        return self.df
