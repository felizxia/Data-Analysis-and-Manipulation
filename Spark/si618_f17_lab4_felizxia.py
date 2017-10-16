from pyspark import SparkContext
sc = SparkContext(appName="lecture4")

from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)


nfl_df = sqlContext.read.json("hdfs:///var/si618f17/NFLPlaybyPlay2015.json")


nfl_df.printSchema()


nfl_df.registerTempTable("nfl")
# question1

post= sqlContext.sql('select posteam, sum(YardsGained) as p from nfl group by posteam').cache()
post.registerTempTable("post")
defensive = sqlContext.sql('select DefensiveTeam, sum(YardsGained) as d from nfl group by DefensiveTeam')
defensive.registerTempTable("defensive")
final_score= sqlContext.sql('select post.posteam, post.p - defensive.d as score from post JOIN defensive ON post.posteam= defensive.DefensiveTeam')
final_score.registerTempTable("final_score")

game=sqlContext.sql('select posteam,count(DISTINCT(GameID)) as num from nfl group by posteam')
game.registerTempTable("game")
average=sqlContext.sql('select game.posteam, final_score.score/game.num as average from final_score JOIN game ON final_score.posteam=game.posteam order by average DESC')
average.rdd.map(lambda i: '\t'.join(str(j) for j in i)) \
	.saveAsTextFile('si618_f17_lab4_output_1_felizxia.tsv')

#question2
run=sqlContext.sql('select posteam,count(PlayType) as c1 from nfl where PlayType = "Run" group by posteam')
run.registerTempTable("run")
passes=sqlContext.sql('select posteam,count(PlayType) as c2 from nfl where PlayType = "Pass" group by posteam')
passes.registerTempTable("passes")
rate=sqlContext.sql('select run.posteam, run.c1/passes.c2 as average from run JOIN passes ON run.posteam=passes.posteam order by average')
rate.rdd.map(lambda i: '\t'.join(str(j) for j in i)) \
	.saveAsTextFile('si618_f17_lab4_output_2_felizxia.tsv')

#question3

pt=sqlContext.sql('select PenalizedPlayer, PenalizedTeam, count(PenalizedPlayer) as cpl from nfl group by PenalizedTeam,PenalizedPlayer order by cpl DESC,PenalizedTeam LIMIT 10')
pt.rdd.map(lambda i: '\t'.join(str(j) for j in i)) \
	.saveAsTextFile('si618_f17_lab4_output_3_felizxia.tsv')