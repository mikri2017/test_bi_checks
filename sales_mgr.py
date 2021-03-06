import MySQLdb
import settings
from decimal import Decimal

class SalesMgr():
    def __init__(self):
        self.__error_msg = ""
        self.__conn = None
        self.__cursor = None


    def __connect_to_base(self):
        try:
            self.__conn = MySQLdb.connect(
                settings.statdb_mycon[0],
                settings.statdb_mycon[1],
                settings.statdb_mycon[2],
                settings.statdb_mycon[3],
                port = settings.statdb_mycon[4],
                charset = 'utf8mb4'
            )

            self.__cursor = self.__conn.cursor()

            self.__cursor.execute("SET NAMES utf8mb4")
            self.__cursor.execute("SET CHARACTER SET utf8mb4")
        except MySQLdb.Error as error:
            self.__error_msg = "Ошибка при попытке подключения к БД MySQL " \
                + "хост[%s] порт[%i] БД[%s]:" % (
                    settings.statdb_mycon[0],
                    settings.statdb_mycon[4],
                    settings.statdb_mycon[3]
                )

            return False

        return True

    def __close_connection(self):
        self.__conn.close()


    def get_last_error(self):
        return self.__error_msg

    def add_sale(self, sum):
        if isinstance(sum, Decimal):
            if not self.__connect_to_base():
                return False

            query = "insert into checks (sum) values ('%s')" % (str(sum))

            try:
                self.__cursor.execute(query.encode('utf8'))
                self.__conn.commit()
            except MySQLdb.Error as error:
                self.__error_msg = "Ошибка при попытке внести в БД продажу" \
                    + "{}".format(error)
                return False

            self.__close_connection()
        else:
            self.__error_msg = "Параметр sum другого типа"
            return False

        return True


    def get_sales_stat(self, date_begin, date_end):
        if not self.__connect_to_base():
            return False

        query = """select
                    ch.id,
                    ch.date,
                    ch.sum
                from checks ch
                where ch.date between '%s 00:00:00' AND '%s 23:59:59';""" % (
                    date_begin.strftime("%Y-%m-%d"),
                    date_end.strftime("%Y-%m-%d")
                )

        items = []
        try:
            self.__cursor.execute(query)

            row = self.__cursor.fetchone()
            while row:
                items.append(
                    {
                        'id': row[0],
                        'date': row[1].strftime("%Y-%m-%d %H:%M:%S"),
                        'sum': float(row[2])
                    }
                )

                row = self.__cursor.fetchone()
        except MySQLdb.Error as error:
            self.__error_msg = "Ошибка при попытке получить данные из БД: " \
                    + "{}".format(error)
            return False

        return items
