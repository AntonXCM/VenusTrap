from http.server import BaseHTTPRequestHandler, HTTPServer
import stats, discord

HOST = "localhost"
PORT = 7385
client: discord.Client
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/stats":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(str.encode(stats.get_ban_stats_str([(guild.id, guild.name) for guild in client.guilds])))
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        pass  # Отключить вывод логов

def start(p_client: discord.Client):
    global client
    client = p_client
    HTTPServer((HOST, PORT), Handler).serve_forever()
    