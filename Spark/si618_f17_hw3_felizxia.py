'''
park-submit --master yarn-client --queue si618f17 --num-executors 2 --executor-memory 1g --executor-cores 2 spark_avg_stars_per_category.py
'''
import sys
import json
import pyspark
from operator import add
from pyspark import SparkConf,SparkContext
conf = SparkConf().setAppName("pyspark")
sc = SparkContext(conf=conf)

input_file = sc.textFile("hdfs:///var/si618f17/yelp_academic_dataset_business.json")
output_file = sys.argv[1]
def all_star(data):
                all_list = []
                city= data.get('city',None)
                neighborhood= data.get('neighborhoods',None)
                review_count= data.get('review_count',None)
                stars = data.get('stars', None)
                if neighborhood!=[]:
                        for n in neighborhood:
                                all_list.append((city, n, review_count, stars))
                else:
                        all_list.append((city,"Unknown",review_count,stars))
                return all_list
def filter_score(score, threshold):
        if score>=threshold:
                return 1
        else:
                return 0
data = input_file.map(lambda line: json.loads(line)).flatMap(all_star)
business = data.map(lambda x:((x[0],x[1]),(1,x[2],filter_score(x[3], 4)))) \
.reduceByKey(lambda x,y:(x[0] + y[0], x[1] + y[1], x[2] + y[2]))\
.map(lambda x:[x[0][0],x[0][1],x[1][0],x[1][1],x[1][2]]) \
.sortBy(lambda x: (x[0],-x[2],-x[3],-x[4],x[1])) \
.map(lambda x:x[0]+'\t'+x[1] +'\t'+str(x[2])+'\t'+str(x[3])+'\t'+str(x[4]))

business.saveAsTextFile(output_file)
