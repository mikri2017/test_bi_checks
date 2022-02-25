from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
from decimal import Decimal
from datetime import datetime
from sales_mgr import SalesMgr

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """ Обработка GET запроса
        """
        res = {
            'res': "ok"
        }

        sales_mgr = SalesMgr()

        parsed_path = parse.urlparse(self.path)
        command = parsed_path.path
        if command == '/add_check':
            check_sum = 0
            params = parsed_path.query.split("&")
            for param in params:
                param_data = param.split("=")
                if param_data[0] == "sum":
                    if len(param_data) == 2:
                        param_data[1] = param_data[1].replace(',','.').strip()
                        try:
                            check_sum = Decimal(param_data[1].replace(',','.'))
                        except Exception as ex:
                            res['res'] = "err"
                            res['msg'] = "Передано некорректное значение параметра " \
                                + "sum: %s, текст ошибки: %s" % (param_data[1], str(ex))
                            break
                    else:
                        res['res'] = "err"
                        res['msg'] = "Параметр передан некорректно (sum)"
                        break

            if res['res'] == "ok":
                if check_sum > 0:
                    res['sum'] = str(check_sum)
                    res_add = sales_mgr.add_sale(check_sum)
                    if res_add == False:
                        res['res'] = "err"
                        res['msg'] = sales_mgr.get_last_error()
                else:
                    res['res'] = "err"
                    res['msg'] = "Сумма продажи должна быть больше нуля"
        elif command == '/get_sale_stat':
            data = {}
            params_list = ["date_begin", "date_end"]

            params = parsed_path.query.split("&")
            for param in params:
                param_data = param.split("=")
                if param_data[0] in params_list:
                    if len(param_data) == 2:
                        try:
                            data[param_data[0]] = datetime.strptime(param_data[1], "%Y-%m-%d")
                        except ValueError:
                            res['res'] = "err"
                            res['msg'] = "Параметр передан некорректно (%s)" % (
                                param_data[0]
                            )
                            break
                    else:
                        res['res'] = "err"
                        res['msg'] = "Параметр передан некорректно (%s)" % (
                            param_data[0]
                        )
                        break

            if res['res'] == "ok":
                if len(data) == 2:
                    items = sales_mgr.get_sales_stat(
                        data['date_begin'],
                        data['date_end']
                    )

                    if isinstance(items, bool) and not items:
                        res['res'] = "err"
                        res['msg'] = sales_mgr.get_last_error()
                    else:
                        res['items'] = items
                else:
                    res['res'] = "err"
                    res['msg'] = "Переданы не все требуемые параметры"
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
