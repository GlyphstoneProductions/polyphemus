
# Polyphemus Camera Server
# This is the RESTful service that snaps photos and sends them to a network client
# Author: Breanna Anderson
# Copyright: Glyphstone Productions (Mirrim3d) (c) 2015, All Rights Reserved
# Contact: breanna@mirrim3d.com, breanna@glyphstone.net
#

from flask import Flask, send_file
from flask import json
from flask import request
from picamera import PiCamera
import picamera

from werkzeug.local import LocalProxy

import time

# ====================================================================
class PolypServer(Flask):


    def __init__(self, *args, **kwargs):
        super(PolypServer, self).__init__( *args, **kwargs)
        self.preview = False
        self.active = False
        self.camera = None


    def __delete__(self):
        if self.preview :
            self.stopPreview()
        if self.active :
            self.stopCamera()

    def service(self):
        return json.jsonify(name="PolyphemusServer", version="0.1.1", copyright="Glyphstone Productions (c)2015")


    def initCamera(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1024,768)
        self.camera.framerate = 30
        self.camera.rotation = 180
        self.active = True

    def stopCamera(self) :
        self.camera.close()
        self.active = False

    def startPreview(self):
        if self.active == False :
            self.initCamera()

        self.camera.start_preview()
        self.preview = True
        time.sleep(2)
        return json.jsonify(camera="Active", preview=True)

    def stopPreview(self):
        self.camera.stop_preview()
        self.preview = False
        return json.jsonify(camera="Active", preview=False)

    def getPicture(self):
        if( self.active == False ) :
            self.startPreview()

        self.camera.capture("snap.png", use_video_port=True)
        return send_file("snap.png")

# =======================================================================

app = PolypServer("polypserver1")

@app.route('/')
def service():
    return app.service()

@app.route('/camera/on')
def camactive():
    return app.startPreview()

@app.route('/camera/off')
def camdeactive():
    return app.stopPreview()

@app.route('/camera/get')
def camsnap():
    return app.getPicture()

if __name__ == "__main__":
    app.run( host="0.0.0.0", port=8081, debug=True)


