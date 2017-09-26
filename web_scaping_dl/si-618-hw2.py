import urllib2
from bs4 import BeautifulSoup
import re
import json
import omdb

# first check if website is unicode or not.
#turn unicode into string
def str_f(s):
    return s.encode('utf-8')
#
# def strip(m):
#     return m.replace(".","")
# # html=urllib2.urlopen('http://www.imdb.com/search/title?at=0&sort=num_votes&count=100').read()
# # html=urllib2.urlopen('step.htm').read()
# web= BeautifulSoup(open("/Users/rita/Desktop/step1.html"),'html.parser')
# title= web.find_all('h3','lister-item-header')
# l=[]
#
# for i in title:
#     rank= strip(i.contents[1].string)
#     name= i.contents[3].string
#     id=i.contents[3].get('href')
#     match=re.search(r'\/(tt.*?)\/.*',id)
#     if match:
#         l.append((match.group(1),rank,name))
#
#
# with open("step2.txt","w") as f:
#     for element in l:
#         f.write("\t".join([str_f(i) for i in element]))
#         f.write('\n')
#

# movie=open('step2.txt','rU')
# step3file=open('step3.txt','w')
# i=0
# for line in movie:
#     id= line.strip().split('\t')[0]
#     request="http://www.omdbapi.com/?i="+str(id)+"&apikey=e92de2aa"
#     next=urllib2.urlopen(request).read()
#     step3file.write(next)
#     step3file.write('\n')
#     i+=1
#     print i
# step3file.close()
import pydot
import itertools
fetch=open('step3.txt','rU')
# step4file=open('step4.txt','w')
# step4file.write("Title"+'\t'+"Actors"+'\n')
graph = pydot.Dot(graph_type='graph', charset='utf-8')
actor_list=[]
for line in fetch:
    line=json.loads(line)
    title=line['Title']
    actor=line['Actors']
    # step4file.write(str_f(title) + '\t' + str_f(actor))
    for x in actor.split(','):
        actor_list.append(x.strip())

print actor_list
# step4file.close()
for i in list(itertools.combinations(actor_list, 2)):
    edge = pydot.Edge(i)
    graph.add_edge(edge)
graph.write('actors_graph_output.dot.')


