import pandas as pd
df = pd.read_csv('data/processed/tyre_analysis.csv')
df = df[df['compound'].isin(['SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET'])]
df.to_csv('data/processed/tyre_analysis.csv', index=False)
print(df['compound'].unique())