from data_reader import read_Nstr_from_Csv
import numpy as np
import datetime
import pandas
from pandas import DataFrame
from config import CONFIG


def filter_employment(x):
    if x == '':
        return x
    remove_list = ['the ', ' corp.', ' corporation', ' company', ' inc.', ' llc', ' llp', ' international']
    for word in remove_list:
        x = x.replace(word,'')
    punctuation = ['.', '?', '!', '...', ',', ':', ';', '-', '[', ']', '{', '}', '(', ')', '\'', '"']
    for ch in punctuation:
        x = x.replace(ch,'')
    mapping_list = {'army': ['us army', 'united states army',
                             'us air force', 'united states air force',
                             'us navy', 'united states navy',
                             'us marines',  'united states marines',
                             'us military',  'united states military', 'us military army',
                             'us coast guard', 'united states coast guard',
                             'united states marine corps', 'department of homeland security',
                             'us army corps of engineers', 'military',
                             'dept of homeland security', 'navy',
                             'air force', 'us government, dept of homeland securi',
                             'usaf','department of defense', 'us forest service'],
                    'postal':['united states postal service', 'us postal service',
                              'u s postal service', 'u s postal service',
                              'uspostal service', 'usps', 'usps','federal government or postal service', 'post office'],
                    'self': ['self', 'self employed', 'self-employed', 'independant contractor',
                             'becoming independent', 'selfemployed'],
                    'bank': ['jpmorgan chase', 'bank of america', 'jp morgan chase',
                             'us bank','citibank','wells fargo bank', 'wells fargo',
                             'citigroup', 'goldman sachs', 'morgan stanley','citi'],
                    'software': ['ibm', 'texas instruments', 'ta instruments', 'at&t', 'att', 'at&t government solutions', 'microsoft', 'google', 'oracle'],
                    'ups': ['united parcel service', 'ups'],
                    'police': ['nypd','new york city police department','lvmpd','prince georges county pd'],
                    'government':['us government', 'u.s. government', 'united states government', 'irs']
                    }
    replacement_list = {
        'army':['army','homeland security','law enforcement','national guard','customs','border protection', 'coast guard'],
        'law':['law firm','attorney','law office', 'law group','lawyer','law center','psa law'],
        'store': ['store','home depot','walmart', 'wal-mart', 'wal mart', 'target'],
        'hospital': ['hospital', 'medical center', 'med ctr', 'health center',
                     'health systems', 'cancer cent', 'cancer center','kaiser permanente',
                     'clinic', 'medical', 'med center','health','pharmacy'],
        'university': ['university','institute','research','institue','laboratories', 'labs', 'lab.','laboratory', 'ecolab', 'uc '],
        'police': ['police', 'patrol', 'sheriff', 'fire dep', 'cal fire',
                   'central jackson county fire', 'fire and rescue dept'],
        'school': ['school','elementary'],
        'verizon': ['verizon'],
        'transportation': ['railway', 'railroad', 'airline','airway', 'transportation'],
        'insurance': ['insurance'],
        'college': ['college'],
        'government': ['federation of','administration', 'smithsonian institution', 'deparment of', 'dept of', 'dep of',
                       'city of', 'state of', 'government','federal employee',
                       'government', 'federal govt', 'federal bureau', 'department',
                       'health dept', 'deptof ed', 'dept veteran affairs', 'dept transportation',
                       'national geospatial intelligence agency', 'evergreen shipping agency usa',
                       'noaa federal agency','fed govt-environmental protection agency',
                       'us environmental protection agency','federal emergency management agency','town of','county of',
                       'board of','commonwealth of', 'county'],
        'bank': ['credit', 'bank', 'investment', 'bloomberg'],
        'casino': ['casino'],
        'software': ['oracle', 'intel', 'microsoft', 'google', 'apple', 'hewlett'],
        'postal':['postal', 'post office'],
        'construction': ['construction','building'],
        'siemens': ['siemens'],
        'hotel': ['hotel','resort','marriott', 'park inn',
                  'holiday inn', 'nassau inn',
                  'hampton inn', 'piccadilly inn'],
        'prison': ['prison', 'correction'],
        'boeing': ['boeing'],
        'ups': ['ups', 'fedex', 'american express'],
        'energy': ['oil co', 'oil fied', 'oil and gas','workman oil',
                   'oil service','stone oil','oilwell','gas','electric','energy'],
        'pepsi': ['pepsi','cola'],
        'mcdonalds': ['burger king', 'mcdonalds'],
        'costco':['costco'],
        'lockheed':['lockheed'],
        'pricewaterhousecoopers':['pricewaterhousecoopers'],
        'bestbuy': ['bestbuy','best buy'],
        'financial': ['financial']
    }
    for key in mapping_list.keys():
        if x in mapping_list[key]:
            x = key
            return x

    if 'collegesource' not in x:
        for key in replacement_list.keys():
            for element in replacement_list[key]:
                if element in x:
                    x = key
                    return x
    return x

def filter_notes(x, all_word):
    comment_present = True
    while comment_present:
        comment_present = False
        removal_position = x.find('borrower added on')
        if removal_position != -1:
            removal_position_2 = x[removal_position:].find('>')
            if removal_position_2 != -1:
                replacement_string = x[removal_position:(removal_position + removal_position_2+1)]
                x = x.replace(replacement_string,' ')
                comment_present = True
    removal_list = ['<br>','<br/>']
    for word in removal_list:
        x = x.replace(word, '')
    punctuation = ['.', '?', '!', '...', ',', ':', ';', '-', '[', ']', '{', '}', '(', ')', '\'', '"', '/', '+', '=', '$', ' due to ', '&', '%', '@']
    digits = ['0','1','2','3','4','5','6','7','8','9']
    for ch in punctuation:
        x = x.replace(ch,' ')
    for ch in digits:
        x = x.replace(ch,'')
    x = x.replace('added on    >', ' ')
    x = x.replace('getting married', 'wedding')
    x = x.replace('get married', 'wedding')
    stop_words = ['none', 'as', 'of', 'at', 'in', 'a', 'we', 'and', 'until', 'through',
                  'thanks', 'thank', '', 'do', 'on', 'their', 'under', 'll', 'why', 'she',
                  'i', 'you', 'am', 'to', 'for', 'is', 're', 'will', 'where', 'including',
                  'm', 'an', 'that', 'so', 'are', 'my', 'me', 'which', 'dont', 'better', 'best', 'most',
                  'have', 'been', 'with', 'this', 'would', 'be','like', 'however', 'next', 'regarding', 'email','name',
                  'loan', 'doesn', 't', 'by','thankyou', 'these', 'going', 'use', 'the','because', 'using', 'while',
                  'last', 'six', 'months', 'hello', 'what', 'hope', 'can', 'wont', 'again', 'november', 'august',
                  'december', 'september', 'october', 'january', 'february','march','april', 'may','june', 'july',
                  'even','just', 'beneath', 'looking', 'were', 'want','into','eight','ve', 'hence', 'hi', 'hello',
                  'to', 'whom', 'myself', 'having', 'then',
                  'from', 'than', 'very', 'much', 'your', 'it', 'only', 'it', 'there',
                  'two', 'all', 'other', 'after', 'how', 'soon', 'one', 'not', 'through', 'believe', 'lot', 'has', 'now',
                  'almost', 'need', 'them', 'but', 'they','could', 'if', 'did', 'was',
                  'any', 'same', 'also', 'some', 'around', 'each', 'about', 'here', 'per', 'more', 'being', 'such', 'd',
                  'our', 'or', 'k', 'those', 'who', 'please', 'three', 'her', 'quote', 'wanted', 'his', 'rather', 'needs',
                  'let', 'us', 'still', 'since', 'ask', 'before', 'purpose', 'don', 'before', 's', 'seeking', 'seek',
                  'looking', 'look', 'she', 'etc', 'give', 'answer', 'already', 'know', 'everything', 'quot',
                  'always', 'ago', 'had', 'less', 'least', 'several', 'see', 'decided', 'once', 'not', 'no','within',
                  'towards', 'field', 'time', 'consideration', 'add', 'get','every', 'used', 'five', 'got', 'date',
                  'without','he','intend', 'allow', 'its', 'needed', 'started', 'starting', 'start', 'too',
                  'approximately', 'doing', 'feel', 'another', 'other', 'when','should', 'though',
                  'recently','go', 'considering', 'able', 'total', 'half', 'completely', 'really', 'fully',
                  'left', 'remaining', 'apr', 'made', 'make', 'making','appreciate', 'possible', 'anything',
                  'up', 'out', 'back','current', 'try', 'trying', 'currently', 'take', 'taking', 'new', 'down',
                  'amount', 'financial', 'off'
                  ]
    map_replacement = {'pay': ['paying', 'payoff', 'pay', 'pays', 'pay off', 'pay down', 'consolidate',
                               'consolidation', 'consolidating', 'refinance', 'refinancing', 'paid','repay'],
                       'rate':['rate','rates'],
                       'purchase':['buy','purchase','purchased'],
                       'school': ['school', 'college', 'student'],
                       'debt': ['debt', 'bill', 'loan', 'credit card'],
                       'job': ['worked', 'working', 'work', 'job', 'position','employment', 'employed'],
                       'year': ['years', 'yrs', 'yearly'],
                       'month': ['month','monthly'],
                       'family': ['wife', 'child', 'children', 'kid', 'kids', 'grandson','parents',
                                  'granddaughter', 'husband'],
                       'lend':['lend', 'lends', 'lending'],
                       'payment': ['payments', 'payment'],
                       'stable': ['stable','steady','solid'],
                       'plan':['plan','planning', 'plans'],
                       'home': ['household','home','house'],
                       'car': ['car', 'truck', 'auto'],
                       'fund': ['fund', 'funds', 'funding', 'funded', 'invest', 'investing', 'investment'],
                       'good': ['good', 'great', 'outstanding','excellent','well']}
    for key in map_replacement.keys():
        for element in map_replacement[key]:
            if element in x:
                x = x.replace(element, key)
    x = x.replace('debts','debt')
    all_words = x.split(' ')
    while ('credit' in all_words) and (('card' in all_words) or ('cards' in all_words)):
        all_words.remove('credit')
        if 'card' in all_words:
            all_words.remove('card')
        else:
            all_words.remove('cards')
        all_words.append('dept')
    while ('credit' in all_words):
        all_words.remove('credit')
    while ('pay' in all_words):
         all_words.remove('pay')
    final_string = ''
    for word in all_words:
        if word not in stop_words:
            if word in ['year', 'month', 'mo', 'day', 'days']:
                word = 'period'
            final_string += ' '
            final_string += word
            all_word.update({word:(all_word.get(word,0)+1)})

    return final_string


def word_frequency(x, all_employers):
    all_employers.update({x:(all_employers.get(x,0)+1)})
    return x


def clear_notes_using_dictionary(x,all_words_kept):
    result = set([])
    x_words = x.split(' ')
    for word in x_words:
        if word != '' and (word in all_words_kept):
            result.add(word)
    return result


def clear_employment_using_dictionary(x,all_employments_kept):
    if x in all_employments_kept:
        return x
    else:
        return ''

def purpose_handling_small_buisness(x, keep_business=True):
    sb_code = 'small business'
    if keep_business:
        if sb_code in x:
            x = sb_code
    else:
        if x != sb_code:
            x = x.replace(sb_code,'')
    x = x.strip()
    return x


def date_coversion(x):
    if x == '':
        return x
    datetime_object = datetime.datetime.strptime(x, '%m/%d/%Y')
    now = datetime.datetime.now()
    delta = now - datetime_object
    return str(delta.days)


def make_lower(x):
    return x.lower()


def filter_text_and_categorical_values(data_path,save_path):
    data = read_Nstr_from_Csv(data_path)
    target_column = CONFIG['target_column']

    # convert all text to lower case
    data = data.applymap(make_lower)

    # convert date of opening line to number of days passed since
    data['earliest_cr_line'] = data['earliest_cr_line'].apply(date_coversion)

    # make reassignment of employers for better frequency of data distribution
    data['emp_title'] = data['emp_title'].apply(filter_employment)

    # compute frequencies for each of the employment types
    all_employers = {}
    data['emp_title'].apply(word_frequency, all_employers=all_employers)

    # compute frequency of each of the word in Notes excluding stop words
    all_word_in_notes = {}
    data['Notes'] = data['Notes'].apply(filter_notes, all_word = all_word_in_notes)

    # keep words only exceeding threshold
    keep_words = []
    for key in all_word_in_notes.keys():
        if all_word_in_notes[key] > 400:
            keep_words.append(key)
    data['Notes'] = data['Notes'].apply(clear_notes_using_dictionary, all_words_kept=keep_words)

    # keep employment types only if exceeding threshold
    keep_employers = []
    for key in all_employers.keys():
        if all_employers[key] > 40:
            keep_employers.append(key)

    data['emp_title'] = data['emp_title'].apply(clear_employment_using_dictionary,all_employments_kept=keep_employers)

    keep_states = []
    address_statistics = data['addr_state'].value_counts()
    for addr_key in address_statistics.keys():
        if address_statistics[addr_key] > 100:
            keep_states.append(addr_key)
    data['addr_state'] = data['addr_state'].apply(clear_employment_using_dictionary, all_employments_kept=keep_states)

    keep_zips = []
    address_statistics = data['zip_code'].value_counts()
    for addr_key in address_statistics.keys():
        if address_statistics[addr_key] > 100:
            keep_zips.append(addr_key)

    data['zip_code'] = data['zip_code'].apply(clear_employment_using_dictionary, all_employments_kept=keep_zips)

    data['purpose_cat'] = data['purpose_cat'].apply(purpose_handling_small_buisness, keep_business=False)

    word_data_frame = DataFrame(0, dtype=np.int64, index=np.arange(data.shape[0]), columns=[('word_' + word) for word in keep_words])
    columnn_notes = data['Notes'].values
    for i in range(data.shape[0]):
        if len(columnn_notes[i]) == 0:
            continue
        record_words = columnn_notes[i]
        for word in record_words:
            word_data_frame.at[i, 'word_' + word] = 1

    data = data.drop(columns=CONFIG['remove_columns'])
    data = pandas.concat([data,word_data_frame],axis=1)
    filtered_columns = [name.lower().strip() for name in data.columns]
    data.columns = filtered_columns
    data.to_csv(save_path,index=False,encoding='utf-8')

if __name__ == "__main__":
    data_path = '../data/dataset.csv'
    save_path = '../data/preprocessed_dataset.csv'
    filter_text_and_categorical_values(data_path, save_path)

