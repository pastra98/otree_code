#%%
import pandas as pd
import re

#%%
# Specify the file path relative to the root directory of the workspace
file_path = "../results/pretest_20_12_pm.csv"

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

#%%
for col in df.columns:
    print(col)
# %%
# TODO: add initial survey data
keepcols = {
    "participant.id_in_session" : "participant_id_in_session",
    "participant.code" : "participant_code",
    "participant.label" : "participant_label",
    "participant.time_started_utc" : "participant_time_started_utc",
    "participant.ses_treat" : "participant_ses_treat",
    "participant.fb_treat" : "participant_fb_treat",
    "participant.total_points" : "participant_total_points",
    "session.code" : "session_code",
    "session.label" : "session_label",
    "session.is_demo" : "session_is_demo",
    "app_initial_survey.1.player.q1": "understanding_q1",
    "app_initial_survey.1.player.q2": "understanding_q2",
    "app_smartcity_pgg.1.player.payoff" : "pgg_1_payoff",
    "app_smartcity_pgg.1.player.endowment"  : "pgg_1_endowment ",
    "app_smartcity_pgg.1.player.s1_contribution"  : "pgg_1_contribution",
    "app_smartcity_pgg.1.group.id_in_subsession"  : "pgg_1_group_id",
    "app_smartcity_pgg.1.group.total_spend"  : "pgg_1_group_total_spend",
    "app_smartcity_pgg.1.group.individual_share"  : "pgg_1_individual_share",
    "app_smartcity_pgg.2.player.payoff"  : "pgg_2_payoff",
    "app_smartcity_pgg.2.player.s2_contribution"  : "pgg_2_contribution",
    "app_smartcity_pgg.2.group.id_in_subsession"  : "pgg_2_group_id",
    "app_smartcity_pgg.2.group.total_spend"  : "pgg_2_group_total_spend",
    "app_smartcity_pgg.2.group.individual_share"  : "pgg_2_individual_share",
    "app_smartcity_pgg.3.player.payoff"  : "pgg_3_payoff",
    "app_smartcity_pgg.3.player.s3_contribution"  : "pgg_3_contribution",
    "app_smartcity_pgg.3.group.id_in_subsession"  : "pgg_3_group_id",
    "app_smartcity_pgg.3.group.total_spend"  : "pgg_3_group_total_spend",
    "app_smartcity_pgg.3.group.individual_share"  : "pgg_3_individual_share",
    "app_post_survey.1.player.country"  : "post_survey_player_country",
    "app_post_survey.1.player.education_level"  : "post_survey_player_education_level",
    "app_post_survey.1.player.mothers_education_level"  : "post_survey_player_mothers_education_level",
    "app_post_survey.1.player.fathers_education_level"  : "post_survey_player_fathers_education_level",
    "app_post_survey.1.player.occupation"  : "post_survey_player_occupation",
    "app_post_survey.1.player.household_composition"  : "post_survey_player_household_composition",
    "app_post_survey.1.player.number_of_books"  : "post_survey_player_number_of_books",
    "app_post_survey.1.player.income": "post_survey_player_income",
}
#%%
# Select and rename the columns
df = df.loc[:, keepcols.keys()].rename(columns=keepcols)
df
#%%
# export the dataframe to a csv file
df.to_csv("../results/cleaned_pretest_20_12_pm.csv", index=False)

# %%
################################################################################
####################        THAR BE DRAGONS                 ####################
################################################################################
# could this be done in a better way? YES
longstring=""""
"app_smartcity_pgg.1.player.payoff" : "app_smartcity_pgg.1.player.payoff",
"app_smartcity_pgg.1.player.endowment " : "app_smartcity_pgg.1.player.endowment ",
"app_smartcity_pgg.1.player.s1_contribution" : "app_smartcity_pgg.1.player.s1_contribution",
"app_smartcity_pgg.1.group.id_in_subsession" : "app_smartcity_pgg.1.group.id_in_subsession",
"app_smartcity_pgg.1.group.total_spend" : "app_smartcity_pgg.1.group.total_spend",
"app_smartcity_pgg.1.group.individual_share" : "app_smartcity_pgg.1.group.individual_share",

"app_smartcity_pgg.2.player.payoff" : "app_smartcity_pgg.2.player.payoff",
"app_smartcity_pgg.2.player.s2_contribution" : "app_smartcity_pgg.2.player.s2_contribution",
"app_smartcity_pgg.2.group.id_in_subsession" : "app_smartcity_pgg.2.group.id_in_subsession",
"app_smartcity_pgg.2.group.total_spend" : "app_smartcity_pgg.2.group.total_spend",
"app_smartcity_pgg.2.group.individual_share" : "app_smartcity_pgg.2.group.individual_share",

"app_smartcity_pgg.3.player.payoff" : "app_smartcity_pgg.3.player.payoff",
"app_smartcity_pgg.3.player.s3_contribution" : "app_smartcity_pgg.3.player.s3_contribution",
"app_smartcity_pgg.3.group.id_in_subsession" : "app_smartcity_pgg.3.group.id_in_subsession",
"app_smartcity_pgg.3.group.total_spend" : "app_smartcity_pgg.3.group.total_spend",
"app_smartcity_pgg.3.group.individual_share" : "app_smartcity_pgg.3.group.individual_share",

"app_smartcity_pgg.4.player.payoff" : "app_smartcity_pgg.4.player.payoff",
"app_smartcity_pgg.4.player.s4_contribution" : "app_smartcity_pgg.4.player.s4_contribution",
"app_smartcity_pgg.4.group.id_in_subsession" : "app_smartcity_pgg.4.group.id_in_subsession",
"app_smartcity_pgg.4.group.total_spend" : "app_smartcity_pgg.4.group.total_spend",
"app_smartcity_pgg.4.group.individual_share" : "app_smartcity_pgg.4.group.individual_share",

"app_smartcity_pgg.5.player.payoff" : "app_smartcity_pgg.5.player.payoff",
"app_smartcity_pgg.5.player.s5_contribution" : "app_smartcity_pgg.5.player.s5_contribution",
"app_smartcity_pgg.5.group.id_in_subsession" : "app_smartcity_pgg.5.group.id_in_subsession",
"app_smartcity_pgg.5.group.total_spend" : "app_smartcity_pgg.5.group.total_spend",
"app_smartcity_pgg.5.group.individual_share" : "app_smartcity_pgg.5.group.individual_share",

"app_smartcity_pgg.6.player.payoff" : "app_smartcity_pgg.6.player.payoff",
"app_smartcity_pgg.6.player.s6_contribution" : "app_smartcity_pgg.6.player.s6_contribution",
"app_smartcity_pgg.6.group.id_in_subsession" : "app_smartcity_pgg.6.group.id_in_subsession",
"app_smartcity_pgg.6.group.total_spend" : "app_smartcity_pgg.6.group.total_spend",
"app_smartcity_pgg.6.group.individual_share" : "app_smartcity_pgg.6.group.individual_share",

"app_smartcity_pgg.7.player.payoff" : "app_smartcity_pgg.7.player.payoff",
"app_smartcity_pgg.7.player.s7_contribution" : "app_smartcity_pgg.7.player.s7_contribution",
"app_smartcity_pgg.7.group.id_in_subsession" : "app_smartcity_pgg.7.group.id_in_subsession",
"app_smartcity_pgg.7.group.total_spend" : "app_smartcity_pgg.7.group.total_spend",
"app_smartcity_pgg.7.group.individual_share" : "app_smartcity_pgg.7.group.individual_share",

"app_post_survey.1.player.country" : "app_post_survey.1.player.country",
"app_post_survey.1.player.education_level" : "app_post_survey.1.player.education_level",
"app_post_survey.1.player.mothers_education_level" : "app_post_survey.1.player.mothers_education_level",
"app_post_survey.1.player.fathers_education_level" : "app_post_survey.1.player.fathers_education_level",
"app_post_survey.1.player.occupation" : "app_post_survey.1.player.occupation",
"app_post_survey.1.player.household_composition" : "app_post_survey.1.player.household_composition",
"app_post_survey.1.player.number_of_books" : "app_post_survey.1.player.number_of_books",
"app_post_survey.1.player.cultural_activities_frequency" : "app_post_survey.1.player.cultural_activities_frequency",
"""
output_lines = []
for line in longstring.strip().split("\n"):
    if ":" in line:
        # Split line at the colon
        left, right = line.split(":", 1)

        right = right.replace("app_post_survey.1.", "post_survey_")
        right = right.replace("app_smartcity_", "")
        right = right.replace(".player.", "_")
        right = re.sub(r's\d_', '', right)
        right = right.replace(".", "_")
        right = right.replace("_in_subsession", "")
        right = right.replace("group_individual_share", "individual_share")

        modified_line = f"{left} :{right}"
        output_lines.append(modified_line)
    else:
        output_lines.append(line)

output_string = "\n".join(output_lines)

print(output_string)

# %%
# data explained

# participant_total_points -> points at the end of the game
# pgg_1_payoff -> endowment - contribution + individual share
# pgg_1_endowment 
# pgg_1_contribution
# pgg_1_group_id -> in each feedback treatment, there are groups of 4 (2 lowses, 2 highses). the groups are randomly shuffeled each round if there are more than one group per treatment
# pgg_1_group_total_spend -> includes the spending of participant
# pgg_1_individual_share -> pot/4*1,5

