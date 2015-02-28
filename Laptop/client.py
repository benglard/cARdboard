import websocket, subprocess, cv2, base64
from tornado.escape import json_encode, json_decode

def on_message(ws, message):
    data = json_decode(message)
    if data['msg'] == 'frame' and data['get']:
        path = './Laptop/static/test.png'
        try:
            subprocess.call('screencapture {}'.format(path), shell=True)
            img = cv2.imread(path)
            img = cv2.resize(img, (640, 480))
            code = cv2.imencode('.png', img)[1]
            b64 = base64.encodestring(code)
            rv = json_encode({
                'msg': 'frame',
                'frame': b64,
                'get': False
            })
            ws.send(rv)
        except:
            pass

def on_error(ws, error):
    print 'Connection error: {}'.format(error)

def on_close(ws):
    print 'Connection Closed'

def on_open(ws):
    print 'Connection opened'

if __name__ == '__main__':
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp('ws://ec2-52-11-8-41.us-west-2.compute.amazonaws.com:8080/ws/CCD1C1/laptop',
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()