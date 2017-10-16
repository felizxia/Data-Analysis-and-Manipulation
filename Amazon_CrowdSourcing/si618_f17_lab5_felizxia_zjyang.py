# crawl all comments (comments & nested comments) that have been written under any post from 09/20/2017 to 09/26/2017

import re
from facepy import GraphAPI
import csv
import numpy as np
from random import choice

user_token='EAACEdEose0cBAEdOM6Y667ZAqmVUuozAqfwnhhPohGgDKRZC1lCHr1ZA9eANantHO2bDVEJMAPf4jNvwl8Dqp5YKbxbglVKKB0dNZB1pXy007NDZAG22bxdZBQn4WrRfrT1XatSzZC4ptZAWxQtUJnUsOZCf0kQR4muIeSPafSm7ds2j9lkPpM0iSna0JTuy0TfNGQ6VaVkeMbwZDZD'
pro= GraphAPI(user_token)
user=pro.get('wsj/posts?fields=id,comments,message','since=2017-09-20&until=2017-09-26')

# step1
## extract and filter emoji and empty lines

emoji=re.compile(u'[\w!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ ]+')

raw_number=open('si618_f17_lab5_total_number_of_comments_felizxia_zjyang.txt','w')
### original is to test emoji clean effect
#original=open('test.txt','w')
m_l=[]
for i in user:
    data= i['data']
    for item in data:
        post_id=item['id']
        try:
            user_i=item['comments']['data']
            message=item['message']
            for w in user_i:
                u_comments= w['message']
                match = emoji.findall(u_comments)
                u_com = ''.join(match).strip()
                c_id=w['id']
                if u_com :
                    # original.write(str(u_com))
                    # original.write('\n')
                    m_l.append(("wsj",post_id, c_id,u_com))
        except KeyError:
            pass

## count row numbers
raw_number.write(str(len(m_l)))


# step2: sample file

sample_f=[choice(m_l) for _ in range(100)]

# step3: write sampled file

with open ('si618_f17_lab5_random_sample_100_comments_felizxia_zjyang.csv','w') as sample:

    writer= csv.writer(sample, dialect='excel')
    writer.writerow(['pagename', 'post_id', 'comment_id','comment'])
    writer.writerows(sample_f)



