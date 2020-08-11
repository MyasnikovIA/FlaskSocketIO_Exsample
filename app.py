from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, url_for, copy_current_request_context
from threading import Thread, Event
import importlib
import sys
import io
from contextlib import redirect_stdout

__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['PORT'] = 7070
app.config['HOST'] = '0.0.0.0'

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

# random number Generator Thread
thread = Thread()
thread_stop_event = Event()
roomMessage = {}


@app.route('/')
def index():
    return render_template('index.html')


def allvars_good(offset=0):
    frame = sys._getframe(1 + offset)
    d = frame.f_globals
    d.update(frame.f_locals)
    return d


def getFrm(arg):
    frm = ''
    m = importlib.import_module(arg)
    if hasattr(m, 'getForm'):
        function_name = getattr(m, 'getForm')
        frm = function_name()
    return frm


def runCommanFromroom(message, socketio):
    pass


def roomThreadDef(SID):
    print("Making random numbers")
    global roomMessage
    while not thread_stop_event.isSet():
        message = ''
        if SID in roomMessage:
            if len(roomMessage[SID]) > 0:
                message = roomMessage[SID][0]
                del roomMessage[SID][0]
        if message != '':
            # runCommanFromroom(message, socketio)
            if 'FunName' in message:
                defName = message['FunName']
                if '.' in defName:
                    packName = defName[:defName.rfind('.')]
                    defName = defName[defName.rfind('.') + 1:]
                    meth = importlib.import_module(packName)
                    with io.StringIO() as buf, redirect_stdout(buf):
                        if hasattr(meth, defName):
                            function_name = getattr(meth, defName)
                            res = function_name(message['args'])
                            if res == None:
                                socketio.emit(message['FunName'], buf.getvalue(), namespace='/socket_controller')
                            else:
                                socketio.emit(message['FunName'], res, namespace='/socket_controller')
                        else:
                            socketio.emit(message['FunName'], {'eval': """ console.log("No def","%s") """ % (message)},namespace='/socket_controller')
                    continue
                socketio.emit(message['FunName'], {'eval': """ console.log("%s") """ % (message)},namespace='/socket_controller')
            else:
                socketio.emit('javascript', {'eval': """ console.log("%s") """ % (message)},
                              namespace='/socket_controller')
            # socketio.sleep(2)


@socketio.on('message', namespace='/socket_controller')
def test_message(message):
    global roomMessage
    if request.sid in roomMessage:
        roomMessage[request.sid].append(message)
    else:
        roomMessage[request.sid] = []
        roomMessage[request.sid].append(message)


@socketio.on('connect', namespace='/socket_controller')
def socket_connect():
    global thread
    if not thread.isAlive():
        thread = socketio.start_background_task(roomThreadDef, request.sid, )


@socketio.on('disconnect', namespace='/socket_controller')
def socket_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
