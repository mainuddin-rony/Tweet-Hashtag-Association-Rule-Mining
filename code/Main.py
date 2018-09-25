import sys
import pandas as pd
import get_hashtag_frequency as tag_coll
import extract_top_tweeter as tweeter
import tweet_association_mining as mining
import calculate_skyline as sky_cal

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got


def handleTweet(tweets):
    collections = []
    for t in tweets:
        tweet = {'id': t.id, 'username': t.username, 'permalink': t.permalink, 'text': t.text, 'date': t.date,
                 'hashtags': t.hashtags}

        collections.append(tweet)
    return collections


def collect_tweets_by_hash_tag(hash_tag, start_date, end_date):
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(hash_tag).setSince(start_date).setUntil(end_date)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    all_tweets = handleTweet(tweet)
    print("Total collected Tweets: " + str(len(all_tweets)))
    df = pd.DataFrame(all_tweets)
    return df


def main():
    data = collect_tweets_by_hash_tag("#healthy", "2018-02-21", "2018-02-28")
    data.to_csv('tweets_collection.csv', encoding='utf-8')
    tag_coll.get_top_hash_tags('tweets_collection.csv', 25)
    top25 = pd.read_csv('top_25_hashtags.csv', encoding='utf-8')
    list_of_dfs = []
    main_tweet = pd.read_csv('tweets_collection.csv', encoding='utf-8')
    list_of_dfs.append(main_tweet)
    for idx, value in top25[1:25].iterrows():
        tag = value['tags']
        list_of_dfs.append(collect_tweets_by_hash_tag(tag, "2018-02-21", "2018-02-28"))

    all_data = pd.concat(list_of_dfs)
    all_data.to_csv('all_tweets_collection.csv', encoding='utf-8')

    tag_coll.get_top_hash_tags('all_tweets_collection.csv', 50)
    #
    tweeter.get_top_tweeters('all_tweets_collection.csv', 50)
    mining.extract_tweet_association('all_tweets_collection.csv', 500, 0.019, .6)
    sky_cal.extract_sky_line_tweets('association_rules.csv')


if __name__ == '__main__':
    main()
