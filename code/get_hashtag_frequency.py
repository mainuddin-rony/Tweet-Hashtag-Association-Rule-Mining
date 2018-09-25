import pandas as pd


def get_top_hash_tags(file_path, top_n):
    data = pd.read_csv(file_path, encoding='utf-8')
    data = data.drop(['Unnamed: 0'], axis=1)
    without_duplicates = data.drop_duplicates(subset=['id'], keep=False)
    hash_data = without_duplicates['hashtags'].str.lower()
    hash_frq = hash_data.str.split(expand=True).stack().value_counts()
    new_hash = hash_frq[~hash_frq.index.isin(['#'])]
    if top_n == 50:
        all_data = pd.DataFrame({'tags': new_hash.index, 'count': new_hash.values})
        all_data.to_csv('all_hashtags_distibution.csv', index=False)
    new_hash = new_hash[0:top_n]
    top_25_data = pd.DataFrame({'tags': new_hash.index, 'count': new_hash.values})
    top_25_data.to_csv('top_' + str(top_n) + '_hashtags.csv',index=False)
