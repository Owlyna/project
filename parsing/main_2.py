import sqlite3

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()
#Запросы: 

#2. Для каждого фильма вывести разницу между средним количеством отзывов в стране выпуска"

cursor.execute("""SELECT films.НазваниеФильма, (films.КоличествоОтзывов -
                   (SELECT AVG(films.КоличествоОтзывов)
                   FROM films
                   GROUP BY films.idСтраныВыпуска))
                   FROM films
                   """)
results = cursor.fetchall()

for row in results:
  print(row)

con.commit()
con.close()        