import http.server
import json
import logging
import random
import sys
import threading
import time

PORT = 3000

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class RestHandler(http.server.BaseHTTPRequestHandler):
    """
    モックアップ。特定の画像ファイルへのPathを与えると、AIで分析し、その画像が所属するClassを返却するAPI。
    is_successがFalseの場合は500エラーとします。
    """

    def do_POST(self):
        logger.info("POST request received")
        # リクエスト取得
        content_len = 0
        if content_len_str := self.headers.get("content-length"):
            content_len = int(content_len_str)

        body = json.loads(self.rfile.read(content_len).decode("utf-8"))
        logger.info(f"Request headers: {self.headers}")
        logger.info(f"Request body: {body}")
        logger.info(f"Content-Length: {content_len}")

        # is_successがFalseの場合は500エラーとします。
        if body.get("is_success"):
            self.send_response(200)
            response_data = {
                "success": True,
                "message": "success",
                "estimated_data": {
                    # classとconfidenceの値をランダムに生成する
                    "class": random.randint(1, 10),
                    "confidence": random.randint(0, 10000) / 10000.0,
                },
            }
        else:
            self.send_response(500)
            response_data = {
                "success": False,
                "message": "Error:E50012",
                "estimated_data": {},
            }

        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

        self.wfile.write(json.dumps(response_data).encode("utf-8"))
        return


def rest_server(port):
    httpd_rest = http.server.ThreadingHTTPServer(("", port), RestHandler)
    httpd_rest.serve_forever()


def main():
    logger.info(f"Mock server is running on port {PORT}")

    try:
        t1 = threading.Thread(target=rest_server, args=(PORT,), daemon=True)
        t1.start()
        while True:
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down mock server...")
        sys.exit()


if __name__ == "__main__":
    main()
