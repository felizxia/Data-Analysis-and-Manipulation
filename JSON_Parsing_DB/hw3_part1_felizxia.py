import json
import sqlite3

con=sqlite3.connect(r'si-618-hw3.db')
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS movie_genre")
cur.execute("DROP TABLE IF EXISTS movies")
cur.execute("DROP TABLE IF EXISTS movie_actor")
def create_table(number,value):
    if number==1:
        cur.execute("CREATE TABLE IF NOT EXISTS movie_genre(imdb_id text, genre text)")
        cur.execute("INSERT INTO movie_genre VALUES(?,?)",value)
    if number==2:
        cur.execute("CREATE TABLE IF NOT EXISTS movies(imdb_id text, title text, year integer, rating integer)")
        cur.execute("INSERT INTO movies VALUES(?,?,?,?)", value)
    if number==3:
        cur.execute("CREATE TABLE IF NOT EXISTS movie_actor(imdb_id text, actor text)")
        cur.execute("INSERT INTO movie_actor VALUES(?,?)", value)
    con.commit()
    return cur.fetchall()

def multiple(list,var):
    if len(var)>1:
        for i in var:
            list.append((imdb_id,i))
    else:
        for i in var:
            list.append((imdb_id, i))

movie=open("movie_actors_data.txt","rU")
movie_genre=[]
movies=[]
movie_actor=[]
for line in movie:
    x=json.loads(line)
    imdb_id=x["imdb_id"]
    genre=x['genres']
    title=x['title']
    rating=x['rating']
    year=x['year']
    actors=x['actors']
    multiple(movie_genre,genre)
    multiple(movie_actor,actors)
    movies.append((imdb_id,title,year,rating))
for value in movie_genre:
    create_table(1,value)
for value in movies:
    create_table(2,value)
for value in movie_actor:
    create_table(3,value)

## Write an SQL query to find top 10 genres with most movies
# output1=cur.execute("SELECT genre, COUNT(genre) FROM movie_genre GROUP BY genre ORDER BY COUNT(genre) DESC LIMIT 10")
#print "Top 10 genres:" + "\n" +"Genre, Movies"
# for row in output1:
#     print row[0].encode('utf-8')+ ',' + str(row[1])
##find number of movies broken down by year in chronological order
# output2= cur.execute("SELECT year, COUNT(title) FROM movies GROUP BY year ORDER BY year")
# print "Year, Movies"
# for row in output2:
#     print str(row[0])+ ',' + str(row[1])
#Write anSQL query to find all Sci-Fi movies order by decreasing rating, then by decreasing year if ratings are the same
# output3=cur.execute('SELECT title, year, rating FROM movies JOIN movie_genre ON (movie_genre.imdb_id= movies.imdb_id) WHERE movie_genre.genre=="Sci-Fi" ORDER BY rating DESC,year DESC')
# print "Sci-Fi movies:" + "\n" +"Title," + "Year,"+ "Rating,"
# for row in output3:
#     print row[0].encode('utf-8')+ ',' + str(row[1])+ ',' + str(row[2])

#Write an SQL query to find the top 10 actors who played in most movies in and after year 2000. In case of titles, sort the rows by actor name.
# output4= cur.execute('SELECT actor, COUNT(actor) FROM movie_actor JOIN movies ON(movie_actor.imdb_id=movies.imdb_id) WHERE year>=2000  GROUP BY actor ORDER BY COUNT(actor) DESC LIMIT 10')
# print 'In and after year 2000, top 10 actors who played in most movies:' +'\n' + 'Actor, Movies'
# for row in output4:
#     print row[0].encode('utf-8') + ',' + str(row[1])

# output5=cur.execute('SELECT COUNT(*), a.actor ,b.actor, group_concat(distinct a.actor||","|| b.actor) as c1 FROM movie_actor AS a INNER JOIN movie_actor AS b on a.imdb_id=b.imdb_id WHERE a.actor!=b.actor GROUP BY a.actor ,b.actor ORDER BY COUNT(*) DESC')
# unable to filter records that are the same


# write function includes k and genre

def search_movie(k,genre):
    fetch='SELECT actor, COUNT(*) FROM movie_actor JOIN movie_genre ON (movie_actor.imdb_id=movie_genre.imdb_id) WHERE movie_genre.genre == "' + str(genre) + '" GROUP BY movie_genre.genre, actor ORDER BY COUNT(*) desc LIMIT ' +str(k)
    result= cur.execute(fetch)
    print "Top"+str(k) +" actors who played in most "+ str(genre)+" movies: +\n"
    for row in result.fetchall():
        print row[0].encode('utf-8') + ',' + str(row[1])


