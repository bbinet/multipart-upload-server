# -*- coding: utf-8 -*-
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import logging
import re
import unicodedata

from tornado.options import define, options, parse_command_line

define("port", default=8080, help="run on the given port", type=int)

UPLOAD_DIR = os.path.join(os.getcwd(), "uploaded")
logging.info("UPLOAD_DIR={}".format(UPLOAD_DIR))
os.makedirs(UPLOAD_DIR, exist_ok=True)

def normalize_path(path: str) -> str:
    return re.sub(r"[^A-Za-z0-9_./-]", "", 
            unicodedata.normalize("NFKD", path)
                .encode("ascii", "ignore").decode("ascii")
            ).strip("._")

def is_safe_path(basedir, path, follow_symlinks=True):
    # resolves symbolic links
    if follow_symlinks:
        matchpath = os.path.realpath(path)
    else:
        matchpath = os.path.abspath(path)
    return basedir == os.path.commonpath((basedir, matchpath))

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        if "upfile" in self.request.files:
            upfile = self.request.files['upfile'][0]
            filename = upfile['filename']
            data = upfile['body']
        else:
            filename = self.get_query_argument("filename", default=None)
            data = self.request.body

        if filename is None or data is None:
            raise tornado.web.HTTPError(400)

        filepath = normalize_path(os.path.normpath(os.path.join(
            UPLOAD_DIR, self.get_argument("updir", default=""), filename)))
        if not is_safe_path(UPLOAD_DIR, filepath):
            logging.error("UPLOAD_DIR=%s filepath=%s", UPLOAD_DIR, filepath)
            raise tornado.web.HTTPError(400)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            with open(filepath, "wb") as f:
                f.write(data)
            logging.info("{} uploaded {}, saved as {}".format(self.request.remote_ip, filename, filepath))
            self.write({"result": "upload OK"})
        except OSError as e:
            logging.error("Failed to write file due to OSError %s", str(e))
            self.write({"result": "upload FAIL"})
            raise

def make_app():
    return tornado.web.Application(
        handlers=[
            (r"/", UploadHandler),
        ],
        template_path=os.path.join(os.getcwd(), "templates"),
        #debug=True,
        )

if __name__ == "__main__":
    options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


