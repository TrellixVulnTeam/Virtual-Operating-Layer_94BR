import multiprocessing
import sys
# from cefpython3 import cefpython as cef
import time
import winsound
from multiprocessing import Process
from http import server
import os
from time import sleep
from pexpect.popen_spawn import PopenSpawn
from term import send, main as term_main, cmd_process
from container import start_container

HOST = 'localhost'
PORT = 8093
INTERACE_READY = False
browser = None
session = None
commands = {}
sessions = {}

from pexpect import exceptions
from winpty import PtyProcess
from winpty import PTY


def main():
    path = os.path.abspath(os.path.dirname(__file__))
    home = os.path.join(path, 'home')
    # os.chdir(home)
    # global session
    #session = term_main('main', callback=callback)
    global browser
    session = {
        'name': 'main',
        'app': 'C:\\Windows\\System32\\cmd.exe',
        'early': (),
        'decode': 'ascii',
    }

    sessions[session['name']] = session
    commands[session['name']] = ()
    #pc = PopenSpawn(session['app'])
    cols, rows = 80, 25
    proc = PTY(cols, rows)
    proc.spawn(session['app'])

    browser, cef = start_container(home, [LoadHandler()])
    set_javascript_bindings(browser, cef)
    print('Loaded.')

    cmd_process(browser, cef, proc, session)
    print('Shutting down')
    cef.Shutdown()


def dlog(*a):
    pass

from transcoder import from_cli, to_cli

def cmd_process(browser, cef, process, session):
    run = 1

    while run:
        cef.MessageLoopWork()
        _commands = commands.get('main', ())
        if len(_commands) > 0:
            commands['main'] = ()
            log('>', _commands)
            for item in _commands:
                process.write(item)
                #process.send(item)

        # Read from pipe
        string = ''
        try:
            string = process.read()
            string = from_cli(string, process, session)
            # string = process.read(size=1024)
            #string = process.read_nonblocking(size=1024, timeout=1)
        except exceptions.EOF as e:
            #End Of File (EOF).
            log('Command process terminal exiting due to EOF', _commands, e)
            run = 0

        if len(string) == 0:
            try:
                sleep(.001)
            except KeyboardInterrupt:
                run = 0
            continue

        send_to_view(browser, session, string)

    log('End of process')


from log import get_logger
logger = get_logger()

def log(*strings):
    logger.info(' '.join(map(str, strings)))


def send_to_view(browser, session, string):
    log('send_to_view', session['name'], browser)

    waiting = browser is None
    if waiting: log('Waiting for interface 1/2')
    while waiting:
        log('.')
        time.sleep(.01)
        waiting = browser is None

    waiting = INTERACE_READY is False
    if waiting:
        log('Waiting for interface 2/2')
        session['early'] += (string, )
    log('send_to_view', session['name'])
    try:
        browser.ExecuteFunction("sessionOutput", session, string)
    except Exception as e:
        log('sessionOutput failed', e)


def session_key_input(name, value):
    print('session_input', name, value)
    value = to_cli(value, name)
    # Push to send loop: cmd_process
    commands[name] += (value,)

def session_input(name, value):
    print('session_input', name, value)
    commands[name] += (value,)


def beep(frequency=1400, duration=100):
    winsound.Beep(frequency, duration)


class External(object):
    def __init__(self, browser):
        self.browser = browser

    def test_multiple_callbacks(self, js_callback):
        """Test both javascript and python callbacks."""
        js_print(self.browser, "Python", "test_multiple_callbacks",
                 "Called from Javascript. Will call Javascript callback now.")

        def py_callback(msg_from_js):
            js_print(self.browser, "Python", "py_callback", msg_from_js)
        js_callback.Call("String sent from Python", py_callback)


def wake_ready(content):
    global INTERACE_READY
    INTERACE_READY = True
    session = sessions.get(content['name'], {})
    early = session.get('early', ())
    for item in early:
        send_to_view(browser, session, item)
    print('\n\nWake Ready', content, session)


def set_javascript_bindings(browser, cef):
    external = External(browser)
    bindings = cef.JavascriptBindings(
            bindToFrames=False, bindToPopups=False)
    bindings.SetProperty("python_property", "This property was set in Python")
    bindings.SetProperty("cefpython_version", cef.GetVersion())
    bindings.SetFunction("wake_ready", wake_ready)
    bindings.SetFunction("sessionInput", session_input)
    bindings.SetFunction("sessionKeyInput", session_key_input)
    bindings.SetObject("external", external)
    browser.SetJavascriptBindings(bindings)


    # http_proc = Process(target=start_vol)
    # http_proc.start()
    #cont_proc.join()
    #http_proc.join()

def js_print(browser, lang, event, msg):
    # Execute Javascript function "js_print"
    browser.ExecuteFunction("js_print", lang, event, msg)


class LoadHandler(object):
    def OnLoadingStateChange(self, browser, is_loading, **_):
        # This callback is called twice, once when loading starts
        # (is_loading=True) and second time when loading ends
        # (is_loading=False).
        if not is_loading:
            # Loading is complete. DOM is ready.
            js_print(browser, "Python", "OnLoadingStateChange",
                     "Loading from py is complete")

if __name__ == '__main__':
    main()