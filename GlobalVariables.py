# Импорт библиотеки
import sqlite3
# Подключение к БД
con = sqlite3.connect("my_userRecords.db")

# Создание курсора
cur = con.cursor()

# Выполнение запроса и получение всех результатов
lastName = cur.execute("""SELECT username FROM records
            WHERE id = 1""").fetchall()[0][0]
lastNumberOfVictoriesInARow = cur.execute("""SELECT numberOfWins FROM records
            WHERE id = 1""").fetchall()[0][0]

con.close()
