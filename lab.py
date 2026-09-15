iimport pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('earthquake_1995-2023.csv')
plt.figure(figsize=(8, 5))
alert_order = ['green', 'yellow', 'orange', 'red']
# sns.boxplot(data=df[df['alert'] != 'unknown'], x='alert', y='magnitude', order=alert_order)
# plt.xlabel('Alert level')
# plt.ylabel('Magnitude')
# plt.tight_layout()
# plt.show()

sns.violinplot(
    data=df[df['alert'] != 'unknown'],
    x='alert',
    y='magnitude',
    order=alert_order,
    palette=alert_order,
)
plt.xlabel('Alert level')
plt.ylabel('Magnitude')
plt.tight_layout()
plt.show()
