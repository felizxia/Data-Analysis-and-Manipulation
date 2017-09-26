import sqlite3
import csv
engine=open("vehicles.csv","rU")
list=[]
# find index
for line in engine:
    lines=line.strip().split(',')
    for i in ['year', 'make', 'model', 'VClass', 'cylinders', 'displ', 'trany','city08', 'highway08', 'comb08']:
       list.append((i,lines.index(i)))
    break
m=0
dblist=[]
for lines in csv.reader(engine):

    year=lines[63]
    make=lines[46]
    model=lines[47]
    Vclass=lines[62]
    displ=lines[23]
    trany=lines[57]
    city08=lines[4]
    highway08=lines[34]
    comb08=lines[15]
    cylinders = lines[22]
    if displ != 0 and cylinders!= "" and displ!= "NA" and cylinders!="NA":
        dblist.append((year, make, model, Vclass, cylinders, displ, trany, city08, highway08, comb08))


con=sqlite3.connect(r'vehicles.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS Engine")
cur.execute("CREATE TABLE IF NOT EXISTS Engine(year INTEGER, make TEXT, model TEXT, Vclass TEXT, cylinders INTEGER, displ FLOAT, trany TEXT, city08 INTEGER, highway08 INTEGER, comb08 INTEGER)")
for value in dblist:
    cur.execute("INSERT INTO Engine VALUES(?,?,?,?,?,?,?,?,?,?)", value)
    con.commit()