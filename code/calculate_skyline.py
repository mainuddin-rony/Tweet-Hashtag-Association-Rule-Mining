import pandas as pd


def extract_sky_line_tweets(file_name):
    data = pd.read_csv(file_name, encoding='utf-8', index_col=False)
    data = data[data['length'] < 6]
    sky_lines = []
    for index, value in data.iterrows():
        present_item = value
        conf_ok = True
        conv_ok = True
        int_ok = True
        for j in range(1, len(data)):
            next_item = data.iloc[(index + j) % len(data)]
            if next_item['conf'] > present_item['conf']:
                conf_ok = False
            else:
                if next_item['conf'] == present_item['conf']:
                    if next_item['conv'] > present_item['conv']:
                        conf_ok = False
                    if next_item['interest'] > present_item['interest']:
                        conf_ok = False
            if next_item['conv'] > present_item['conv']:
                conv_ok = False
            else:
                if next_item['conv'] == present_item['conv']:
                    if next_item['conf'] > present_item['conf']:
                        conv_ok = False
                    if next_item['interest'] > present_item['interest']:
                        conv_ok = False
            if next_item['interest'] > present_item['interest']:
                int_ok = False
            else:
                if next_item['interest'] == present_item['interest']:
                    if next_item['conf'] > present_item['conf']:
                        int_ok = False
                    if next_item['conv'] > present_item['conv']:
                        int_ok = False
            if conf_ok or conv_ok or int_ok:
                continue
            else:
                present_item['is_sky'] = 'no'
                break
        if conf_ok or conv_ok or int_ok:
            present_item['is_sky'] = 'yes'
        else:
            present_item['is_sky'] = 'no'
        sky_lines.append(present_item)
    skyline_data = pd.DataFrame(sky_lines)
    skyline_data = skyline_data[skyline_data['is_sky'] == 'yes']

    skyline_data.to_csv('skyline_hash_tags.csv', encoding='utf-8')
    print "Rules \t Confidence \t Conviction \t Interest"
    for idx, val in skyline_data.iterrows():
        print "%s %1.3f %1.3f %1.3f" % (val['rule'], val['conf'], val['conv'], val['interest'])

