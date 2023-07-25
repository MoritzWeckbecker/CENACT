import pandas as pd
import os
import numpy as np

list_of_datasets = [
    'ace_vaxinpad',
    'acp_anticp',
    'acp_iacp',
    'acp_mlacp',
    'afp_amppred',
    'afp_antifp',
    'aip_aippred',
    'aip_antiinflam',
    'amp_antibp',
    'amp_antibp2',
    'amp_csamp',
    'amp_fernandes',
    'amp_gonzales',
    'amp_iamp2l',
    'amp_modlamp',
    'atb_antitbp',
    'atb_iantitb',
    'avp_amppred',
    'avp_avppred',
    'bce_ibce',
    'cpp_cellppd',
    'cpp_cellppdmod',
    'cpp_cppredfl',
    'cpp_kelmcpp',
    'cpp_mixed',
    'cpp_mlcpp',
    'cpp_mlcppue',
    'cpp_sanders',
    'hem_hemopi'
]

# add imbalances for new datasets
imbalance_dict = {
    'ace_vaxinpad':0.4404069767,
    'acp_anticp':0.5,
    'acp_iacp':0.4011627907,
    'acp_mlacp':0.3196581197,
    'afp_amppred':0.5,
    'afp_antifp':0.5003429355,
    'aip_aippred':0.4003813155,
    'aip_antiinflam':0.4063088512,
    'amp_antibp':0.5005807201,
    'amp_antibp2':0.5012543904,
    'amp_csamp':0.5,
    'amp_fernandes':0.4978354978,
    'amp_gonzales':0.2093023256,
    'amp_iamp2l':0.2676613886,
    'amp_modlamp':0.4749903063,
    'atb_antitbp':0.5,
    'atb_iantitb':0.5,
    'avp_amppred':0.5,
    'avp_avppred':0.5721107927,
    'bce_ibce':0.4408260524,
    'cpp_cellppd':0.5,
    'cpp_cellppdmod':0.5006839945,
    'cpp_cppredfl':0.5,
    'cpp_kelmcpp':0.5024925224,
    'cpp_mixed':0.7578125,
    'cpp_mlcpp':0.3878087231,
    'cpp_mlcppue':0.5,
    'cpp_sanders':0.7655172414,
    'hem_hemopi':0.472826087
}

# add bio_field for new datasets
bio_field_dict = {
    'ace_vaxinpad':'ace',
    'acp_anticp':'acp',
    'acp_iacp':'acp',
    'acp_mlacp':'acp',
    'afp_amppred':'afp',
    'afp_antifp':'afp',
    'aip_aippred':'aip',
    'aip_antiinflam':'aip',
    'amp_antibp':'amp',
    'amp_antibp2':'amp',
    'amp_csamp':'amp',
    'amp_fernandes':'amp',
    'amp_gonzales':'amp',
    'amp_iamp2l':'amp',
    'amp_modlamp':'amp',
    'atb_antitbp':'atb',
    'atb_iantitb':'atb',
    'avp_amppred':'avp',
    'avp_avppred':'avp',
    'bce_ibce':'bce',
    'cpp_cellppd':'cpp',
    'cpp_cellppdmod':'cpp',
    'cpp_cppredfl':'cpp',
    'cpp_kelmcpp':'cpp',
    'cpp_mixed':'cpp',
    'cpp_mlcpp':'cpp',
    'cpp_mlcppue':'cpp',
    'cpp_sanders':'cpp',
    'hem_hemopi':'hem'
}

def max_median(df):
    max_medians = []
    for i in range(len(df)):
        row = df.iloc[i,:]
        max_median = np.max([np.median([row[i*5:i*5+4]]) for i in range(10)])
        max_medians.append(max_median)
    return max_medians

def prepare_dataframe(file, encoding):
    path = os.path.join('.', 'csv', file)
    df = pd.read_csv(path, index_col=0)
    df['F1'] = max_median(df)
    df = pd.DataFrame(df['F1'])
    df['Dataset'] = df.index
    df['is_imbalanced'] = df['Dataset'].map(imbalance_dict)
    df['bio_field'] = df['Dataset'].map(bio_field_dict)
    df['Encoding'] = encoding
    df['type'] = "sequence based"
    df = df.reset_index(drop=True)
    return(df)

def best_encoding(df):
    df['Encoding_max'] = None
    for dataset in list_of_datasets:
        df_sub = df[df['Dataset'] == dataset]
        largest_value = df_sub['F1'].max()
        largest_encoding = df_sub.loc[df_sub['F1'] == largest_value, 'Encoding'].values[0]
        df.loc[df['Dataset'] == dataset, 'Encoding_max'] = largest_encoding
    return df


df_hyd = prepare_dataframe('cv_f1_score_level_2_with_hydrogen.csv', 'cenact_hyd')
df_nohyd = prepare_dataframe('cv_f1_score_level_2_without_hydrogen.csv', 'cenact_nohyd')
df_dd = prepare_dataframe('cv_f1_score_level_2_data_driven.csv', 'cenact_dd')

df_comb = pd.concat([df_hyd, df_nohyd, df_dd]).reset_index(drop=True)
df_comb = best_encoding(df_comb)
df_comb = df_comb[['Dataset', 'Encoding', 'Encoding_max', 'F1', 'type', 'is_imbalanced', 'bio_field']]
df_comb.to_csv('./CENACT_f1_score_overview.csv', index=False)

json_data = df_comb.to_json(orient = 'records')

# Save the JSON string as a file
with open('../Data/Visualization_data/data/multiple_datasets/vis/mds_1_Overview/hm_cenact_data.json', 'w') as file:
    file.write(json_data)