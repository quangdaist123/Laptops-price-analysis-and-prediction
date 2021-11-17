import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.factorplots import interaction_plot
import statsmodels.api as sm
from statsmodels.formula.api import ols

import warnings

from Preprocessing.utils.utils_step_1 import correct_dtypes

# In[2]:


warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
pd.options.display.max_rows

# In[3]:
df = pd.read_csv('Dataset/Tidy/3_dataset_feature_added.csv')
df = correct_dtypes(df)
quanti_cols = df.select_dtypes(include='number').columns
quali_df = df.select_dtypes(include='object')
quali_cols = quali_df.columns

# %% TƯƠNG QUAN (ĐA BIẾN)
# %% Interaction plot

for i in range(len(quali_cols) - 1):
    for j in range(i + 1, len(quali_cols)):
        plt.figure(figsize=(7, 7))

        # Tính p-value cho tương tác của 2 biến. p < 0.05 => có ý nghĩa thống kê => có tương tác giữa 2 biến
        model = ols(f'used_price ~ {quali_cols[i]} + {quali_cols[j]} + {quali_cols[i]}:{quali_cols[j]}',
                    data=df).fit()
        aov = sm.stats.anova_lm(model, typ=2)
        p_value = aov['PR(>F)'][f'{quali_cols[i]}:{quali_cols[j]}']

        # Vẽ interaction plot
        interaction_plot(x=quali_df[quali_cols[i]], trace=quali_df[quali_cols[j]], response=df['used_price'])

        # Size của plot

        fig = plt.gcf()
        fig.set_size_inches(9, 7)

        # Size của legend
        plt.legend(fontsize=12)

        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        axes = plt.gca()

        # Size của x y labels
        axes.xaxis.label.set_size(15)
        axes.yaxis.label.set_size(15)

        # Bỏ viền xung quanh
        ax = plt.subplot(111)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Vẽ ticks của trục x
        __ = ax.set_xticklabels(ax.get_xticklabels(), rotation=60)
        labels = [str(int(item / 1e6)) + ' tr' for item in ax.get_yticks()]
        # Custom ticks của trục y
        __ = ax.set_yticklabels(labels)

        ___ = plt.title(f'used_price vs {quali_cols[i]}:{quali_cols[j]}\n(p_value two-way ANOVA: {p_value:.2e})',
                        fontdict={'size': 15})
        plt.tight_layout()
        # plt.show()
        # break
        plt.savefig(f'EDA/plots results/categorical/interactions/{quali_cols[i]} vs {quali_cols[j]}.png',
                    bbox_inches='tight')
        plt.clf()
    # break

#%%
# quali_cols[i] =
for j in range(i + 1, len(quali_cols)):
    plt.figure(figsize=(7, 7))

    # Tính p-value cho tương tác của 2 biến. p < 0.05 => có ý nghĩa thống kê => có tương tác giữa 2 biến
    model = ols(f'used_price ~ {"cpu_speed"} + {quali_cols[j]} + {"cpu_speed"}:{quali_cols[j]}',
                data=df).fit()
    aov = sm.stats.anova_lm(model, typ=2)
    p_value = aov['PR(>F)'][f'{"cpu_speed"}:{quali_cols[j]}']

    # Vẽ interaction plot
    interaction_plot(x=quali_df["cpu_speed"], trace=quali_df[quali_cols[j]], response=df['used_price'])

    # Size của plot

    fig = plt.gcf()
    fig.set_size_inches(9, 7)

    # Size của legend
    plt.legend(fontsize=12)

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    axes = plt.gca()

    # Size của x y labels
    axes.xaxis.label.set_size(15)
    # axes.yaxis.label.set_size(15)

    # Bỏ viền xung quanh
    ax = plt.subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Vẽ ticks của trục x
    __ = ax.set_xticklabels(ax.get_xticklabels(), rotation=60)
    labels = [str(int(item / 1e6)) + ' tr' for item in ax.get_yticks()]
    # Custom ticks của trục y
    __ = ax.set_yticklabels(labels)

    ___ = plt.title(f'used_price vs {"cpu_speed"}:{quali_cols[j]}\n(p_value two-way ANOVA: {p_value:.2e})',
                    fontdict={'size': 15})
    plt.tight_layout()
    plt.show()
    # break
    # plt.savefig(f'EDA/plots results/categorical/interactions/{"cpu_speed"} vs {quali_cols[j]}.png',
    #             bbox_inches='tight')
    plt.clf()
#%%
plt.figure(figsize=(7, 7))
# Tính p-value cho tương tác của 2 biến. p < 0.05 => có ý nghĩa thống kê => có tương tác giữa 2 biến
model = ols(f'used_price ~ {"cpu_speed"} + {quali_cols[j]} + {"cpu_speed"}:{quali_cols[j]}',
            data=df).fit()
aov = sm.stats.anova_lm(model, typ=2)
p_value = aov['PR(>F)'][f'{"cpu_speed"}:{quali_cols[j]}']

# Vẽ interaction plot
interaction_plot(x=quali_df["cpu_speed"], trace=quali_df[quali_cols[j]], response=df['used_price'])

# Size của plot

fig = plt.gcf()
fig.set_size_inches(9, 7)

# Size của legend
plt.legend(fontsize=12)

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
axes = plt.gca()

# Size của x y labels
axes.xaxis.label.set_size(15)
# axes.yaxis.label.set_size(15)

# Bỏ viền xung quanh
ax = plt.subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Vẽ ticks của trục x
__ = ax.set_xticklabels(ax.get_xticklabels(), rotation=60)
labels = [str(int(item / 1e6)) + ' tr' for item in ax.get_yticks()]
# Custom ticks của trục y
__ = ax.set_yticklabels(labels)

___ = plt.title(f'used_price vs {"cpu_speed"}:{quali_cols[j]}\n(p_value two-way ANOVA: {p_value:.2e})',
                fontdict={'size': 15})
plt.tight_layout()
plt.show()
# break
# plt.savefig(f'EDA/plots results/categorical/interactions/{"cpu_speed"} vs {quali_cols[j]}.png',
#             bbox_inches='tight')
plt.clf()