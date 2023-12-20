#%%
import pandas as pd
import matplotlib.pyplot as plt

# load
am = pd.read_csv("../results/cleaned_pretest_20_12_am.csv")
pm = pd.read_csv("../results/cleaned_pretest_20_12_pm.csv")

#%%
am.columns

# %%
payoff_cols = [col for col in am.columns if "payoff" in col]
contributions_cols = [col for col in am.columns if "contribution" in col]

# %%
# plot grouped by ses treatment
ses_plots = am.groupby("participant_ses_treat")[contributions_cols].boxplot()
for plot in ses_plots:
    plot.set_xticklabels(["r1", "r2", "r3"])
ses_plots

# %%
# plot grouped by fb treatment
fb_plots = am.groupby("participant_fb_treat")[contributions_cols].boxplot()
for plot in fb_plots:
    plot.set_xticklabels(["r1", "r2", "r3"])

# %%
