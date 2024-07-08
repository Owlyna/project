import sqlite3

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()
#Запросы: 
#1. Для каждой страны вывести средний рейтинг фильма, сумму количества отзывов

cursor.execute("""SELECT countries.СтранаВыпуска, AVG(films.Оценка), SUM(films.КоличествоОтзывов)
               FROM countries
               FULL OUTER JOIN films ON countries.idСтраныВыпуска = films.idСтраныВыпуска
               GROUP BY countries.СтранаВыпуска;
               """)

results = cursor.fetchall()

for row in results:
  print(row)

con.commit()
con.close()        

