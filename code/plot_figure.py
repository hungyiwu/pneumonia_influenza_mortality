import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.ticker import MaxNLocator

# load data
merged_data_filepath = '../derived_data/merged_data.csv'
output_filepath = '../derived_data/figure.png'

df = pd.read_csv(merged_data_filepath)

# prepare data
df.sort_values(by=['Year', 'Week'], inplace=True)
num_week = df.shape[0]

# plot
fig, axes = plt.subplots(ncols=2, nrows=1, sharex=True, figsize=(8,4))

axes[0].plot(range(num_week), 1e4 * df['US_P&I_death_pct'].values, color='tab:blue')
axes[0].plot(range(num_week), 1e4 * df['TW_P&I_death_pct'].values, color='tab:orange')
axes[0].set_title('Weekly death')
axes[0].set_ylabel('Count per million people')
axes[0].yaxis.set_major_locator(MaxNLocator(integer=True))
axes[0].legend(['United States', 'Taiwan'])

axes[1].plot(range(num_week), np.cumsum(df['US_P&I_death_pct'].values), color='tab:blue')
axes[1].plot(range(num_week), np.cumsum(df['TW_P&I_death_pct'].values), color='tab:orange')
axes[1].set_title('Cumulative death')
axes[1].set_ylabel('% of 2018 population')
axes[1].legend(['United States', 'Taiwan'])

# add time ticks
tick_weeks = np.arange(0, num_week, num_week//4, dtype=int)
tick_labels = []
for t in tick_weeks:
    y = int(df.iloc[t]['Year'])
    w = int(df.iloc[t]['Week'])
    tick_labels.append('{}\nweek {}'.format(y, w))
params = dict(ma='center', ha='center', rotation=45)
axes[0].set_xticks(tick_weeks)
axes[0].set_xticklabels(tick_labels, **params)
axes[1].set_xticklabels(tick_labels, **params)

# add title for the whole figure
fig.suptitle('2018-2019 Pneumonia & Influenza Mortality')
fig.tight_layout(rect=[0, 0, 1, 0.95])

# save figure
plt.savefig(output_filepath)
plt.show()
