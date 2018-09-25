import pandas as pd


def get_top_tweeters(file_path, top_n):
    data = pd.read_csv(file_path, encoding='utf-8')
    data = data.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)
    without_duplicates = data.drop_duplicates(subset=['id'], keep=False)
    tweeter_frq = without_duplicates['username'].value_counts()[0:top_n]
    top_25_data = pd.DataFrame({'tweeter': tweeter_frq.index, 'count': tweeter_frq.values})
    top_25_data.to_csv('top_' + str(top_n) + '_tweeters.csv',index=False)