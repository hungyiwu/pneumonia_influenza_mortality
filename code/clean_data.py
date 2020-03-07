import os
import pandas as pd

# paths
raw_data_folderpath = '../raw_data'
derived_data_folderpath = '../derived_data'
us_pop_filepath = os.path.join(raw_data_folderpath, 'nst-est2019-alldata.csv#.csv')
tw_pop_filepath = os.path.join(raw_data_folderpath, 'y0s1-00000.xls')
us_pi_filepath = os.path.join(raw_data_folderpath, 'NCHSData19.csv')
tw_pi_filepath = os.path.join(raw_data_folderpath, 'chart.csv')
output_pi_filepath = os.path.join(derived_data_folderpath, 'merged_data.csv')
output_pop_filepath = os.path.join(derived_data_folderpath, 'pop.csv')

# get US population
df_us_pop = pd.read_csv(us_pop_filepath)
us_pop_2018 = df_us_pop.loc[df_us_pop['NAME']=='United States', 'POPESTIMATE2018'].tolist()[0]

# get US P&I mortality
df_pi_us = pd.read_csv(us_pi_filepath)
df_pi_us['US_P&I_death_count'] = df_pi_us['Percent of Deaths Due to Pneumonia and Influenza']\
        * df_pi_us['All Deaths'] / 100
df_pi_us = df_pi_us[['Year', 'Week', 'US_P&I_death_count']]

# get Taiwan population
df_tw_pop = pd.read_excel(tw_pop_filepath, sheet_name='107', usecols='C', skiprows=4, header=None)
tw_pop_2018 = df_tw_pop.iloc[0].tolist()[0]

# get Taiwan P&I mortality
df_pi_tw = pd.read_csv(tw_pi_filepath)
df_pi_tw = df_pi_tw[['死亡年週', '肺炎及流感死亡人數']]
df_pi_tw['Year'] = df_pi_tw['死亡年週'].apply(lambda s: int(str(s)[0:4]))
df_pi_tw['Week'] = df_pi_tw['死亡年週'].apply(lambda s: int(str(s)[4:]))
df_pi_tw['TW_P&I_death_count'] = df_pi_tw['肺炎及流感死亡人數']
df_pi_tw = df_pi_tw[['Year', 'Week', 'TW_P&I_death_count']]

# merge data
df_merge = df_pi_tw.merge(df_pi_us, on=['Year', 'Week'], how='inner')
df_merge = df_merge.applymap(int)

# calculate mortality percentage
df_merge['TW_P&I_death_pct'] = df_merge['TW_P&I_death_count'] / tw_pop_2018 * 100
df_merge['US_P&I_death_pct'] = df_merge['US_P&I_death_count'] / us_pop_2018 * 100

# save data
df_merge.to_csv(output_pi_filepath, index=False)

df_pop = pd.DataFrame([[us_pop_2018, tw_pop_2018]], columns=['us_pop_2018', 'tw_pop_2018'])
df_pop = df_pop.applymap(int)
df_pop.to_csv(output_pop_filepath, index=False)
