import pandas as pd

tyre_images = {
    'SOFT': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/tyre%20labels/Soft.png',
    'MEDIUM': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/tyre%20labels/Medium.png',
    'HARD': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/tyre%20labels/Hard.png',
    'INTERMEDIATE': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/tyre%20labels/Intermediate.png',
    'WET': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/tyre%20labels/Wet.png'
}

df = pd.read_csv('data/processed/tyre_usage.csv')
df['image_url'] = df['compound'].map(tyre_images)
df['pct_stints'] = df['pct_stints'] / 100
df.to_csv('data/processed/tyre_usage_with_images.csv', index=False)
print(df['compound'].unique())
print(f"Total rows: {len(df)}")