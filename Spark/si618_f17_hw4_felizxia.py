from pyspark import SparkContext
sc = SparkContext(appName="lecture4")

from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
from pyspark.sql import *

busi = sqlContext.read.json("hdfs:///var/si618f17/yelp_academic_dataset_business.json")
review= sqlContext.read.json("hdfs:///var/si618f17/yelp_academic_dataset_review.json")

busi.registerTempTable("busi")
review.registerTempTable("review")

# all reviews business id(+), user id(review), city(busi)
all1=sqlContext.sql('select count(DISTINCT(city)) as cities ,user_id from review JOIN busi ON review.business_id= busi.business_id group by user_id')
all1.registerTempTable("all1")

city_num= sqlContext.sql('select MAX(cities) from all1').first()['_c0']
# use histogram for count city names, make sure 27,28 appears
all_review= all1.rdd.map(lambda x: x[0]).histogram(city_num)[1]
city_count=0
all_city_review=[]
list=[]
for i in all_review:
	city_count+=1
	all_city_review.append((city_count,i))
# create columns
hist= (sc.parallelize(all_city_review)).toDF()
column= [('cities','yelp users')]
cc= sqlContext.createDataFrame(column)
all_review=cc.unionAll(hist)

all_review.rdd.map(lambda i: ','.join(str(j) for j in i)) \
	.saveAsTextFile('si618_f17_hw4_output_allreview_felizxia.csv')

#pos review > star 3
pos_r= sqlContext.sql('select count(DISTINCT(city)) as cities ,user_id from review JOIN busi ON review.business_id= busi.business_id where review.stars>3 group by user_id')
pos_r.registerTempTable('pos_r')
pos_r2=sqlContext.sql('select cities, count(DISTINCT(user_id)) as yelp from pos_r  group by cities')
pos_r3 = cc.unionAll(pos_r2)
pos_r3.rdd.map(lambda i: ','.join(str(j) for j in i)) \
	.saveAsTextFile('si618_f17_hw4_output_goodreview_felizxia.csv')
#neg review star<3
neg_r= sqlContext.sql('select count(DISTINCT(city)) as cities ,user_id from review JOIN busi ON review.business_id= busi.business_id where review.stars<3 group by user_id')
neg_r.registerTempTable('neg')
neg_r2=sqlContext.sql('select cities, count(DISTINCT(user_id)) as yelp from neg group by cities')
neg_r3 = cc.unionAll(neg_r2)
neg_r3.rdd.map(lambda i: ','.join(str(j) for j in i)) \
	.saveAsTextFile('si618_f17_hw4_output_badreview_felizxia.csv')