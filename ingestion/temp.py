import pandas as pd

tyre_images = {
    'SOFT': 'https://tyre-assets.pirelli.com/staticfolder/Tyre/resources/img/red-parentesi.png',
    'MEDIUM': 'https://tyre-assets.pirelli.com/staticfolder/Tyre/resources/img/yellow-parentesi.png', 
    'HARD': 'https://tyre-assets.pirelli.com/staticfolder/Tyre/resources/img/white-parentesi.png',
    'INTERMEDIATE': 'https://upload.wikimedia.org/wikipedia/commons/a/a3/F1_tire_Pirelli_PZero_Green_2019.png',
    'WET': 'https://tyre-assets.pirelli.com/images/global/968/233/cinturato-blue-wet-4505508953865.png'
}

df = pd.read_csv('data/processed/tyre_usage.csv')
df['image_url'] = df['compound'].map(tyre_images)
df['pct_stints'] = df['pct_stints'] / 100  # divide por 100
df.to_csv('data/processed/tyre_usage_with_images.csv', index=False)
print(df.head())