import pandas as pd
import numpy as np

# Function to generate normally distributed random numbers within a range
def normal_random_within_range(mean, std_dev, low, high):
    while True:
        value = np.random.normal(mean, std_dev)
        if low <= value <= high:
            return value

# Settings
treatment_groups = ["control", "competitive", "cooperative"]
ses_types = ["low_ses", "high_ses"]
participants_per_group = 4
rounds = 7

# Create DataFrame
participants = []
for group in treatment_groups:
    for _ in range(participants_per_group):
        participants.append({'treatment_group': group})

df = pd.DataFrame(participants)

# Assign SES types and participant IDs
df['ses_status'] = np.tile(ses_types, len(df) // 2)
df['participant_id'] = np.arange(len(df)) + 1

# Generate round data
for round_num in range(1, rounds + 1):
    for ses in ses_types:
        subset = df['ses_status'] == ses
        contribution_range = (0, 5) if ses == "low_ses" else (0, 8)
        df.loc[subset, f'{round_num}_contribution'] = df.loc[subset, 'ses_status'].apply(
            lambda _: normal_random_within_range(np.mean(contribution_range), 1, *contribution_range))

    df[f'{round_num}_group_total'] = df[f'{round_num}_contribution'].apply(
        lambda _: normal_random_within_range(13, 5, 0, 26))
    df[f'{round_num}_individual_share'] = df[f'{round_num}_group_total'].apply(
        lambda _: normal_random_within_range(4.875, 2, 0, 9.75))

# Save to CSV
filename = 'experimental_data.csv'
df.to_csv(filename, index=False)
print(f"Data saved to {filename}")
