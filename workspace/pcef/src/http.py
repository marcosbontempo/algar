#!/usr/bin/python
# coding: utf-8

# HTTP POST
# 
# This class requests the POST method in the URL with the given data

# Import libraries
import httplib2
import traceback

ERROR_POST = 400 # HTTP POST error

class HTTP:   
    def POST(self, url, data):
        try:
            # Construct objects
            http = httplib2.Http()
            # POST
            headers = {'Content-Type': 'application/json'}
            response, content = http.request(url, 'POST', headers=headers, body=data)
                    
            # Return response
            #return json.loads(content)
            return content
        except Exception:
            print traceback.format_exc()
            return ERROR_POST
        