#%%
import pandas as pd

# Specify the file path relative to the root directory of the workspace
file_path = "test_data/test_results.csv"

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

#%%
for col in df.columns:
    print(col)
# %%
keepcols = [
participant.id_in_session
participant.code
participant.label
participant.time_started_utc
participant.ses_treat
participant.fb_treat
participant.total_points
session.code
session.label
session.is_demo
# these will be revisited later
app_initial_survey.1.player.id_in_group
app_initial_survey.1.player.role
app_initial_survey.1.player.payoff
app_initial_survey.1.player.income
app_initial_survey.1.player.understood_game
app_initial_survey.1.group.id_in_subsession
app_initial_survey.1.subsession.round_number
# ------------------------------
app_smartcity_pgg.1.player.payoff
app_smartcity_pgg.1.player.endowment # only keep for first round
app_smartcity_pgg.1.player.s1_contribution
app_smartcity_pgg.1.group.id_in_subsession # group id
app_smartcity_pgg.1.group.total_spend
app_smartcity_pgg.1.group.individual_share

app_smartcity_pgg.2.player.payoff
app_smartcity_pgg.2.player.s2_contribution
app_smartcity_pgg.2.group.id_in_subsession
app_smartcity_pgg.2.group.total_spend
app_smartcity_pgg.2.group.individual_share

app_smartcity_pgg.3.player.payoff
app_smartcity_pgg.3.player.s3_contribution
app_smartcity_pgg.3.group.id_in_subsession
app_smartcity_pgg.3.group.total_spend
app_smartcity_pgg.3.group.individual_share

app_smartcity_pgg.4.player.payoff
app_smartcity_pgg.4.player.s4_contribution
app_smartcity_pgg.4.group.id_in_subsession
app_smartcity_pgg.4.group.total_spend
app_smartcity_pgg.4.group.individual_share

app_smartcity_pgg.5.player.payoff
app_smartcity_pgg.5.player.s5_contribution
app_smartcity_pgg.5.group.id_in_subsession
app_smartcity_pgg.5.group.total_spend
app_smartcity_pgg.5.group.individual_share

app_smartcity_pgg.6.player.payoff
app_smartcity_pgg.6.player.s6_contribution
app_smartcity_pgg.6.group.id_in_subsession
app_smartcity_pgg.6.group.total_spend
app_smartcity_pgg.6.group.individual_share

app_smartcity_pgg.7.player.payoff
app_smartcity_pgg.7.player.s7_contribution
app_smartcity_pgg.7.group.id_in_subsession
app_smartcity_pgg.7.group.total_spend
app_smartcity_pgg.7.group.individual_share

app_smartcity_pgg.8.player.id_in_group
app_smartcity_pgg.8.player.role
app_smartcity_pgg.8.player.payoff
app_smartcity_pgg.8.player.endowment
app_smartcity_pgg.8.player.s1_contribution
app_smartcity_pgg.8.player.s2_contribution
app_smartcity_pgg.8.player.s3_contribution
app_smartcity_pgg.8.player.s4_contribution
app_smartcity_pgg.8.player.s5_contribution
app_smartcity_pgg.8.player.s6_contribution
app_smartcity_pgg.8.player.s7_contribution
app_smartcity_pgg.8.group.id_in_subsession
app_smartcity_pgg.8.group.total_spend
app_smartcity_pgg.8.group.individual_share
app_smartcity_pgg.8.subsession.round_number
app_smartcity_pgg.9.player.id_in_group
app_smartcity_pgg.9.player.role
app_smartcity_pgg.9.player.payoff
app_smartcity_pgg.9.player.endowment
app_smartcity_pgg.9.player.s1_contribution
app_smartcity_pgg.9.player.s2_contribution
app_smartcity_pgg.9.player.s3_contribution
app_smartcity_pgg.9.player.s4_contribution
app_smartcity_pgg.9.player.s5_contribution
app_smartcity_pgg.9.player.s6_contribution
app_smartcity_pgg.9.player.s7_contribution
app_smartcity_pgg.9.group.id_in_subsession
app_smartcity_pgg.9.group.total_spend
app_smartcity_pgg.9.group.individual_share
app_smartcity_pgg.9.subsession.round_number
app_smartcity_pgg.10.player.id_in_group
app_smartcity_pgg.10.player.role
app_smartcity_pgg.10.player.payoff
app_smartcity_pgg.10.player.endowment
app_smartcity_pgg.10.player.s1_contribution
app_smartcity_pgg.10.player.s2_contribution
app_smartcity_pgg.10.player.s3_contribution
app_smartcity_pgg.10.player.s4_contribution
app_smartcity_pgg.10.player.s5_contribution
app_smartcity_pgg.10.player.s6_contribution
app_smartcity_pgg.10.player.s7_contribution
app_smartcity_pgg.10.group.id_in_subsession
app_smartcity_pgg.10.group.total_spend
app_smartcity_pgg.10.group.individual_share
app_smartcity_pgg.10.subsession.round_number
app_post_survey.1.player.id_in_group
app_post_survey.1.player.role
app_post_survey.1.player.payoff
app_post_survey.1.player.country
app_post_survey.1.player.education_level
app_post_survey.1.player.mothers_education_level
app_post_survey.1.player.fathers_education_level
app_post_survey.1.player.occupation
app_post_survey.1.player.household_composition
app_post_survey.1.player.number_of_books
app_post_survey.1.player.cultural_activities_frequency
app_post_survey.1.group.id_in_subsession
app_post_survey.1.subsession.round_number
