import itertools
import pandas as pd

'''for generating candidate set containing 1 item'''


def generate_candidate_1_set(items, min_twt_count):
    candidate_set = {}
    for index, value in items.iteritems():
        if value >= min_twt_count:
            candidate_set[index] = value
    return candidate_set

'''for generating hashtags per tweet'''


def generate_hash_tags_test_data(tag_series):
    total_tweets = 0
    test_data_set = []
    for index, value in tag_series.iteritems():
        tweet_hash = []
        total_tweets += 1
        for tags in value.split():
            tweet_hash.append(tags)
        test_data_set.append(tweet_hash)
    print "=============Hash Tag List for each Tweet================"
    print "Total %d tweets" % len(test_data_set)
    return test_data_set

"""for generating frequent hash tag set containing 1 tag"""


def generate_frequent_item_set_1(candidate, item_set, support):
    freq_tag_set_1 = []
    test_size = len(item_set)
    for key in candidate:
        if candidate[key] / float(test_size) >= support:
            hash_tags = [key]
            freq_tag_set_1.append(hash_tags)
    print "===================Frequent Hash Tag Set: 1===================="
    print freq_tag_set_1
    print "==========================================================="
    return freq_tag_set_1

"""function to generate subset"""


def generate_subset(S, m):
    return set(itertools.combinations(S, m))

"""to check whether pruning is required"""


def has_infrequent_subset(candidate, hash_tag_set, k):
    hash_list = generate_subset(candidate, k)
    for item in hash_list:
        tags = []
        for l in item:
            tags.append(l)
            tags.sort()
        if tags not in hash_tag_set:
            return True
    return False

"""apply apriori rule to rule out infrequent hash tag set"""


def apply_apriori(hash_tag_set, k):
    length = k
    candidate_set_k = []
    for list1 in hash_tag_set:
        for list2 in hash_tag_set:
            idx = 0
            candidate = []
            if list1 != list2:
                while idx < length - 1:
                    if list1[idx] != list2[idx]:
                        break
                    else:
                        idx += 1
                else:
                    if list1[length - 1] < list2[length - 1]:
                        for item in list1:
                            candidate.append(item)
                        candidate.append(list2[length - 1])
                        if not has_infrequent_subset(candidate, hash_tag_set, k):
                            candidate_set_k.append(candidate)
    return candidate_set_k

"""for generating frequent hash tag set containing more than 1 tag"""


def generate_frequent_item_set_n(freq_tag_set_1, test_data_set, support):
    n = 2  # frequent item set counter
    length = len(test_data_set)
    candidate_set = []
    freq_itemset = []
    for item in freq_tag_set_1:
        candidate_set.append(item)
    while candidate_set:
        item_container = []
        valid_candidates = apply_apriori(candidate_set, n - 1)
        for candidate in valid_candidates:
            count = 0
            each_candidate = set(candidate)
            for per_tweet in test_data_set:
                per_tweet_set = set(per_tweet)
                if each_candidate.issubset(per_tweet_set):
                    count += 1
            if count / float(length) >= support:
                candidate.sort()
                item_container.append(candidate)
        candidate_set = []
        print "=======================Frequent Hash Tag Set: %d============================" % n
        print item_container
        print "============================================================================"
        for l in item_container:
            candidate_set.append(l)
        n += 1
        if item_container:
            freq_itemset.append(item_container)

    return freq_itemset


def extract_tweet_association(file_name, min_twt_count, support, confidence):
    data = pd.read_csv(file_name, encoding='utf-8')
    data = data.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)
    without_duplicates = data.drop_duplicates(subset=['id'], keep=False)
    hash_data = without_duplicates['hashtags'].str.lower()
    hash_frq = hash_data.str.split(expand=True).stack().value_counts()
    filtered_hash = hash_frq[~hash_frq.index.isin(['#'])]
    candidate_1 = generate_candidate_1_set(filtered_hash, min_twt_count)
    test_data_set = generate_hash_tags_test_data(hash_data)
    freq_tag_set_1 = generate_frequent_item_set_1(candidate_1, test_data_set, support)
    freq_set = generate_frequent_item_set_n(freq_tag_set_1, test_data_set, support)
    print "---------------------ASSOCIATION RULES------------------"
    print "RULES \t SUPPORT \t CONFIDENCE \t CONVICTION \t INTEREST \t ITEM_LENGTH"
    print "--------------------------------------------------------"
    num = 1
    rule_list = []
    for f_set in freq_set:
        for item_xy in f_set:
            length = len(item_xy)
            count = 1
            while count < length:
                r = generate_subset(item_xy, count)
                count += 1
                for item in r:
                    count_x = 0
                    count_xy = 0
                    count_y = 0
                    item_x = []
                    item_y = []
                    for i in item:
                        item_x.append(i)
                    for T in test_data_set:
                        if set(item_x).issubset(set(T)):
                            count_x += 1
                        if set(item_xy).issubset(set(T)):
                            count_xy += 1
                    if count_xy / float(count_x) >= confidence:
                        for index in item_xy:
                            if index not in item_x:
                                item_y.append(index)
                        for T in test_data_set:
                            if set(item_y).issubset(set(T)):
                                count_y += 1
                        supp = count_xy / float(len(test_data_set))
                        conf = count_xy / float(count_x)
                        conv = (1 - count_y / float(len(test_data_set))) / (count_xy / float(count_x))
                        interest = (count_xy / float(len(test_data_set))) / (
                        count_x / float(len(test_data_set)) * count_y / float(len(test_data_set)))
                        rule_str = "%s==>%s" % (item_x, item_y)
                        each_rule = {'rule_no': num, 'rule': rule_str, 'supp': supp, 'conf': conf, 'conv': conv, 'interest': interest, 'length': length}
                        rule_list.append(each_rule)
                        rule = "Rule%d %s==>%s %1.3f %1.3f %1.3f %1.3f %d" % (
                        num, item_x, item_y, supp, conf, conv, interest, length)
                        print rule
                        num += 1
    pd.DataFrame(rule_list).to_csv('association_rules.csv', encoding='utf-8', index=False)