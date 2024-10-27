from flask import Flask
import subprocess
import os
import signal
import psutil
import logging
import random
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Setup rotating logs
log_file = '/home/sri/HomeAutomation/log/server.log'
handler = RotatingFileHandler(log_file, maxBytes=1000, backupCount=0)  # Rotate after 1000 bytes, keep 0 backup, rotate on the same file
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

def is_homebridge_running():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'homebridge' in proc.info['name']:
            return True
    return False

def is_vlc_running():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'vlc' in proc.info['name']:
            return True
    return False

def start_vlc_server():
    """Start VLC in the background using --one-instance."""
    if not is_vlc_running():
        vlc_command = [
            "cvlc",
            "--alsa-audio-device=hw:0,0", 
            "--extraintf", "rc", 
            "--rc-host=localhost:4212", 
            "--one-instance",  # Ensure only one instance of VLC runs
            "--no-video"
        ]
        subprocess.Popen(vlc_command)
        app.logger.info("VLC server started in the background.")
    else:
        app.logger.info("VLC is already running in the background.")

@app.route('/play_playlist', methods=['POST'])
def play_playlist():
    start_vlc_server()
    if is_vlc_running():
        try:
            send_command('clear')
            send_command("add /home/sri/Music/sri_playlist.m3u")
            app.logger.info("Started playing playlist.")
            return "Your playlist is playing now.", 200
        except Exception as e:
            error_message = f"Failed to play playlist: {e}"
            app.logger.error(error_message)
            return error_message, 500  # Relay the error back in the response        
    else:
        app.logger.warning("VLC is not running. Cannot play playlist.")
        return "VLC is not running. Start VLC server first.", 400


@app.route('/kill', methods=['POST'])
def kill_vlc():
    if is_vlc_running():
        for proc in psutil.process_iter(['pid', 'name']):
            if 'vlc' in proc.info['name']:
                os.kill(proc.info['pid'], signal.SIGTERM)  # Kill the VLC process
        app.logger.info("VLC process killed.")
        return "VLC has been stopped.", 200 
    else:
        app.logger.warning("VLC is not running. Cannot kill.")
        return "VLC is not running right now.", 400 

@app.route('/stop', methods=['POST'])
def stop():
    if is_vlc_running():
        send_command('stop')
        app.logger.info("Stopping VLC playback.")
        return "Stopping your playlist.", 200  
    else:
        app.logger.warning("VLC is not running. Cannot stop playback.")
        return "VLC is not running. Start VLC server first.", 400  

@app.route('/play', methods=['POST'])
def play():
    start_vlc_server()
    if is_vlc_running():
        send_command('play')
        app.logger.info("Resumed VLC playback.")
        return "Resuming your playlist.", 200  
    else:
        app.logger.warning("VLC is not running. Cannot resume playback.")
        return "VLC is not running. Start VLC server first.", 400 

@app.route('/pause', methods=['POST'])
def pause():
    if is_vlc_running():
        send_command('pause')
        app.logger.info("Paused VLC playback.")
        return "Playback paused.", 200  
    else:
        app.logger.warning("VLC is not running. Cannot pause playback.")
        return "VLC is not running. Start VLC server first.", 400  

@app.route('/next', methods=['POST'])
def next_track():
    if is_vlc_running():
        send_command('next')
        app.logger.info("Skipped to next track.")
        return "Skipped to the next track.", 200 
    else:
        app.logger.warning("VLC is not running. Cannot skip to next track.")
        return "VLC is not running. Start VLC server first.", 400 

@app.route('/previous', methods=['POST'])
def previous_track():
    if is_vlc_running():
        send_command('prev')
        app.logger.info("Playing the previous track.")
        return "Playing the previous track.", 200 
    else:
        app.logger.warning("VLC is not running. Cannot play the previous track.")
        return "VLC is not running. Start VLC server first.", 400  

@app.route('/status', methods=['GET'])
def get_status():
    if is_vlc_running():
        app.logger.info("VLC is running.")
        return "VLC is currently running.", 200 
    else:
        app.logger.warning("VLC is not running.")
        return "VLC is not running right now.", 400  

def send_command(command):
    """Send command to VLC through the remote control interface."""
    import telnetlib
    HOST = "localhost"
    PORT = 4212

    try:
        with telnetlib.Telnet(HOST, PORT) as tn:
            tn.write((command + "\n").encode('utf-8'))
            tn.read_until(b'>')
    except Exception as e:
        app.logger.error(f"Error sending command to VLC: {e}")
        raise e


if __name__ == '__main__':
    if not is_homebridge_running():
        subprocess.Popen(['homebridge'])
        app.logger.info("Homebridge started.")

    start_vlc_server()

    app.run(host='0.0.0.0', port=5000)

