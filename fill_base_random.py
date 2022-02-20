import random
import MySQLdb
import settings

mdb_con = MySQLdb.connect(
    settings.statdb_mycon[0],
    settings.statdb_mycon[1],
    settings.statdb_mycon[2],
    settings.statdb_mycon[3],
    port = settings.statdb_mycon[4],
    charset = 'utf8mb4'
)

mdb_cur = mdb_con.cursor()

mdb_cur.execute("SET NAMES utf8mb4")
mdb_cur.execute("SET CHARACTER SET utf8mb4")


for month in range(7, 9):
    for day in range (1, 32):
        for h in range(9, 21):
            m = random.randint(0, 59)
            s = random.randint(0, 59)
            sum = round(random.uniform(1,1000), 2)

            query = """insert into checks
                        (date, sum) 
                    values
                        ('2021-0%i-%i %i:%i:%i', '%s')""" % (
                            month, day, h, m, s, str(sum)
                        )

            try:
                mdb_cur.execute(query.encode('utf8'))
                mdb_con.commit()
            except MySQLdb.Error as error:
                error_msg = "Ошибка при попытке внести в БД продажу" \
                    + "{}".format(error)
                print(error_msg)
                exit(1)

mdb_con.close()
