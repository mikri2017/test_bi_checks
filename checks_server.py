from email import message
from http.server import BaseHTTPRequestHandler
from ntpath import join
from urllib import parse
import json
from decimal import Decimal

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        res = {
            'res': "ok"
        }

        parsed_path = parse.urlparse(self.path)
        command = parsed_path.path
        if command == '/add_check':
            check_sum = 0
            params = parsed_path.query.split("&")
            for param in params:
                data = param.split("=")
                if data[0] == "sum":
                    if len(data) == 2:
                        data[1] = data[1].replace(',','.').strip()
                        try:
                            check_sum = Decimal(data[1].replace(',','.'))
                        except Exception as ex:
                            res['res'] = "err"
                            res['msg'] = "Передано некорректное значение параметра " \
                                + "sum: %s, текст ошибки: %s" % (data[1], str(ex))
                    else:
                        res['res'] = "err"
                        res['msg'] = "Параметр передан некорректно (sum)"

            if res['res'] == "ok":
                if check_sum > 0:
                    res['sum'] = str(check_sum)
                else:
                    res['res'] = "err"
                    res['msg'] = "Сумма проджажи должна быть больше нуля"
        elif command == '/get_sale_stat':
            res['msg'] = "Получить статистику продаж"
        else:
            res['res'] = "err"
            res['msg'] = "Неизвестная команда"

        self.send_response(200)
        self.send_header('Content-Type', 'application/json;  charset=utf-8')
        self.end_headers()

        msg = json.dumps(res)
        self.wfile.write(msg.encode('utf-8'))


if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8080), GetHandler)
    print('Запуск сервера, нажмите Ctrl+C для остановки')
    server.serve_forever()
