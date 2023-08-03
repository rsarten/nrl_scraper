import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

stats = pd.read_csv('data/summarised/all_stats.csv')
compare = stats[['break_even', 'fantasy_points']].copy()
compare['diff'] = (compare.loc[:,'break_even'] - compare.loc[:,'fantasy_points'])
compare['diff_sqr'] = compare['diff']**2

np.sqrt(compare['diff_sqr'].mean()) # 21.272065964029135
plt.close()
plt.style.use('ggplot')
plt.hist(compare['diff'], bins=30)
plt.savefig('be_err.png')
