#!/usr/bin/python
# coding: utf-8

# server

# Import libraries
import json
import SocketServer
import daemon
import syslog
# Import classes
from BaseHTTPServer import BaseHTTPRequestHandler

class ServerHandler(BaseHTTPRequestHandler):
    logfile = '/tmp/ocs_log'
    PORT = 10000
    
    def do_POST(self):
        try:
            # Log received data
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            self.log(data_string)
            # Send headers
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # Return result JSON
            result = json.dumps({"result": "OK"})
            self.wfile.write(result)      

        except Exception as e:
            self.log("Exception: "+str(e))
    
    def setQoS(self, message):
        print message
            
    def log(self, message):
        fd = open(self.logfile, 'a+')
        fd.write(message+'\n')
        fd.close()
        
# MAIN
if __name__ == '__main__':
    syslog.syslog(syslog.LOG_INFO, "Starting...")
    try:
        # Construct objects
        Handler = ServerHandler
        # HTTP Server
        httpd = SocketServer.TCPServer(("", Handler.PORT), Handler)
        httpd.serve_forever()
    except (KeyboardInterrupt, SystemExit): 
        httpd.shutdown()