from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import urllib.parse
import html

PORT = 8000

NAV_HTML = '''
<nav>
    <a href="/">Главная</a> |
    <a href="/about">О сайте</a> |
    <a href="/services">Контент</a> |
    <a href="/contact">Контакт</a> |
    <a href="/feedback">Обратная связь</a>
</nav>
<hr>
'''

class MyHandler(BaseHTTPRequestHandler):

    def log_request_info(self, method):
        path_only = urlparse(self.path).path
        ip = self.client_address[0]
        print(f"{method}-запрос: {path_only} от {ip}")

    def do_GET(self):
        self.log_request_info('GET')
        path = urlparse(self.path).path

        if path == '/':
            self.send_page("Главная", "<p>Добро пожаловать на самый базовый/простой HTTP сайт!</p>")
        elif path == '/about':
            self.send_page("О сайте", "<p>Лабораторная работа №2 по Интернет-Технологиям — демонстрация работы HTTP в Python.</p>")
        elif path == '/services':
            services_html = "<ul><li>Веб-разработка</li><li>Сетевые технологии</li><li>Интернет Технологии</li></ul>"
            self.send_page("Контент", services_html)
        elif path == '/contact':
            contact_html = "<p>Email: den.2610@mail.ru<br>Телефон: +7 913 788 26 10</p>" \
                           "<p>Для обратной связи воспользуйтесь формой: <a href=\"/feedback\">Обратная связь</a></p>"
            self.send_page("Контакт", contact_html)
        elif path == '/feedback':
            self.send_form()
        elif path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
        else:
            self.send_404()

    def do_POST(self):
        self.log_request_info('POST')
        path = urlparse(self.path).path

        if path == '/submit':
            self.handle_form_submission()
        else:
            self.send_404()

    def send_page(self, title, content_html):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html_page = f"""<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{html.escape(title)}</title>
</head>
<body>
{NAV_HTML}
<h1>{html.escape(title)}</h1>
{content_html}
</body>
</html>"""
        self.wfile.write(html_page.encode('utf-8'))

    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html_page = f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>404 - Не найдено</title></head>
<body>
{NAV_HTML}
<h1>404 - Страница не найдена</h1>
<p>Запрошенный URL: {html.escape(urlparse(self.path).path)}</p>
</body>
</html>"""
        self.wfile.write(html_page.encode('utf-8'))

    def send_form(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        form_html = '''<form action="/submit" method="post">
    <p>
        <label>Имя (обязательно):</label><br>
        <input type="text" name="name" required>
    </p>
    <p>
        <label>Email (обязательно):</label><br>
        <input type="email" name="email" required>
    </p>
    <p>
        <label>Тема:</label><br>
        <input type="text" name="subject">
    </p>
    <p>
        <label>Сообщение:</label><br>
        <textarea name="message" rows="5" cols="50"></textarea>
    </p>
    <p>
        <button type="submit">Отправить</button>
    </p>
</form>
'''
        html_page = f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>Обратная связь</title></head>
<body>
{NAV_HTML}
<h1>Обратная связь</h1>
{form_html}
</body>
</html>"""
        self.wfile.write(html_page.encode('utf-8'))

    def handle_form_submission(self):
        # Читаем тело POST
        try:
            content_length = int(self.headers.get('Content-Length', 0))
        except (TypeError, ValueError):
            content_length = 0

        body = self.rfile.read(content_length).decode('utf-8')
        form = parse_qs(body)

        name = form.get('name', [''])[0].strip()
        email = form.get('email', [''])[0].strip()
        subject = form.get('subject', [''])[0].strip()
        message = form.get('message', [''])[0].strip()

        if not name or not email:
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            error_html = f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>Ошибка</title></head>
<body>
{NAV_HTML}
<h1>Ошибка: обязательные поля не заполнены</h1>
<p>Пожалуйста, укажите имя и email.</p>
<p><a href="/feedback">Вернуться к форме</a></p>
</body>
</html>"""
            self.wfile.write(error_html.encode('utf-8'))
            return

        safe_data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }
        ip = self.client_address[0]
        print(f"Получены данные: {safe_data} от {ip}")

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        esc = html.escape
        confirmation_html = f"""
<h2>Спасибо, {esc(name)}!</h2>
<p>Я получил ваше сообщение.</p>
<ul>
    <li><strong>Email:</strong> {esc(email)}</li>
    <li><strong>Тема:</strong> {esc(subject)}</li>
    <li><strong>Сообщение:</strong> <pre style="white-space:pre-wrap">{esc(message)}</pre></li>
</ul>
<p><a href="/">На главную</a></p>
"""
        html_page = f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>Отправлено</title></head>
<body>
{NAV_HTML}
{confirmation_html}
</body>
</html>"""
        self.wfile.write(html_page.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=MyHandler, port=PORT):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print(f"http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
        httpd.server_close()
        print("Сервер остановлен.")

if __name__ == '__main__':
    run()
