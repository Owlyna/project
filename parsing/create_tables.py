#Таблица 1: id фильма, название фильма, год выпуска, id страны выпуска, жанр, режиссер, оценка, количество отзывов
#Таблица 2: id страны выпуска, страна выпуска

import sqlite3

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()
#таблица со странами
cursor.execute('''CREATE TABLE IF NOT EXISTS countries (idСтраныВыпуска INTEGER PRIMARY KEY AUTOINCREMENT, СтранаВыпуска TEXT NOT NULL)''')
cursor.execute('''INSERT INTO countries(СтранаВыпуска)
                SELECT DISTINCT films.СтранаВыпуска
                FROM films
                ''')
#новая таблица с фильмами и внешним ключем по стране выпуска
cursor.execute('''CREATE TABLE IF NOT EXISTS films_new (id INTEGER PRIMARY KEY AUTOINCREMENT, НазваниеФильма TEXT NOT NULL, ГодВыпуска INTEGER NOT NULL, СтранаВыпуска TEXT NOT NULL, Жанр TEXT NOT NULL, Режиссер TEXT NOT NULL, Оценка REAL NOT NULL, КоличествоОтзывов INTEGER NOT NULL, 
               FOREIGN KEY (СтранаВыпуска)
               REFERENCES countries(СтранаВыпуска))
               ''')
cursor.execute('''INSERT INTO films_new (НазваниеФильма, ГодВыпуска, СтранаВыпуска, Жанр, Режиссер, Оценка, КоличествоОтзывов)                
               SELECT films.НазваниеФильма, films.ГодВыпуска, films.СтранаВыпуска, films.Жанр, films.Режиссер, films.Оценка, films.КоличествоОтзывов
               FROM films
               ''')
cursor.execute('''DROP TABLE films''')
cursor.execute('''ALTER TABLE films_new
               RENAME TO films''')



#таблица с фильмами с заполненной колонкой idСтраныВыпуска
cursor.execute('''CREATE TABLE IF NOT EXISTS films_1 (id INTEGER PRIMARY KEY AUTOINCREMENT, НазваниеФильма TEXT NOT NULL, ГодВыпуска INTEGER NOT NULL, СтранаВыпуска TEXT NOT NULL, idСтраныВыпуска INTEGER NOT NULL, Жанр TEXT NOT NULL, Режиссер TEXT NOT NULL, Оценка REAL NOT NULL, КоличествоОтзывов INTEGER NOT NULL,
               FOREIGN KEY (СтранаВыпуска)
               REFERENCES countries(СтранаВыпуска)) ''')
cursor.execute('''INSERT INTO films_1 (НазваниеФильма, ГодВыпуска, СтранаВыпуска, idСтраныВыпуска, Жанр, Режиссер, Оценка, КоличествоОтзывов)                
               SELECT films.НазваниеФильма, films.ГодВыпуска, films.СтранаВыпуска, countries.idСтраныВыпуска, films.Жанр, films.Режиссер, films.Оценка, films.КоличествоОтзывов
               FROM films
               FULL OUTER JOIN countries ON films.СтранаВыпуска = countries.СтранаВыпуска
               ''')
#конечный вариант таблицы с фильмами и с внешним ключем idСтраныВыпуска
cursor.execute('''CREATE TABLE IF NOT EXISTS films_fin (id INTEGER PRIMARY KEY AUTOINCREMENT, НазваниеФильма TEXT NOT NULL, ГодВыпуска INTEGER NOT NULL, idСтраныВыпуска INTEGER NOT NULL, Жанр TEXT NOT NULL, Режиссер TEXT NOT NULL, Оценка REAL NOT NULL, КоличествоОтзывов INTEGER NOT NULL, 
               FOREIGN KEY (idСтраныВыпуска)
               REFERENCES countries(idСтраныВыпуска))
               ''')
cursor.execute('''INSERT INTO films_fin (НазваниеФильма, ГодВыпуска, idСтраныВыпуска, Жанр, Режиссер, Оценка, КоличествоОтзывов)                
               SELECT films_1.НазваниеФильма, films_1.ГодВыпуска, films_1.idСтраныВыпуска, films_1.Жанр, films_1.Режиссер, films_1.Оценка, films_1.КоличествоОтзывов
               FROM films_1
               ''')
cursor.execute('''DROP TABLE films''')
cursor.execute('''DROP TABLE films_1''')
cursor.execute('''ALTER TABLE films_fin
               RENAME TO films''')

con.commit()
con.close()
