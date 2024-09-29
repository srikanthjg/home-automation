from flask import Flask, jsonify
import subprocess
import os
import signal
import psutil

app = Flask(__name__)

# Store the VLC process
vlc_process = None

def is_homebridge_running():
    """Check if Homebridge is running."""
    for proc in psutil.process_iter(['pid', 'name']):
        if 'homebridge' in proc.info['name']:
            return True
    return False

@app.route('/play_playlist', methods=['POST'])
def play_playlist():

    global vlc_process
    if vlc_process is None:  # Check if VLC is not already running
        vlc_command = ["cvlc", "--alsa-audio-device=hw:0,0", "--extraintf", "rc", "--rc-host=localhost:4212", "/home/sri/Music/sri_playlist.m3u"]
        vlc_process = subprocess.Popen(vlc_command)
        return jsonify({"status": "VLC started playing the playlist"}), 200
    else:
        return jsonify({"status": "VLC is already running"}), 400

@app.route('/kill', methods=['POST'])
def kill_vlc():
    global vlc_process
    if vlc_process is not None:
        os.kill(vlc_process.pid, signal.SIGTERM)  # Terminate the VLC process
        vlc_process = None
        return jsonify({"status": "VLC has been stopped"}), 200
    else:
        return jsonify({"status": "VLC is not running"}), 400

@app.route('/play', methods=['POST'])
def play():
    if vlc_process:
        # Send the command to VLC through telnet or other means
        send_command('play')
        return jsonify({"status": "Playing"}), 200
    return jsonify({"status": "VLC is not running"}), 400

@app.route('/pause', methods=['POST'])
def pause():
    if vlc_process:
        send_command('pause')
        return jsonify({"status": "Paused"}), 200
    return jsonify({"status": "VLC is not running"}), 400

@app.route('/stop', methods=['POST'])
def stop():
    if vlc_process:
        send_command('stop')
        return jsonify({"status": "Stopped"}), 200
    return jsonify({"status": "VLC is not running"}), 400

@app.route('/volume/increase', methods=['POST'])
def increase_volume():
    if vlc_process:
        send_command('volume +10')
        return jsonify({"status": "Volume increased"}), 200
    return jsonify({"status": "VLC is not running"}), 400

@app.route('/volume/decrease', methods=['POST'])
def decrease_volume():
    if vlc_process:
        send_command('volume -10')
        return jsonify({"status": "Volume decreased"}), 200
    return jsonify({"status": "VLC is not running"}), 400

@app.route('/seek/<int:seconds>', methods=['POST'])
def seek(seconds):
    if vlc_process:
        command = f'seek {seconds}'
        send_command(command)
        return jsonify({"status": f"Seeked to {seconds} seconds"}), 200
    return jsonify({"status": "VLC is not running"}), 400

def send_command(command):
    import telnetlib

    HOST = "localhost"
    PORT = 4212

    try:
        with telnetlib.Telnet(HOST, PORT) as tn:
            tn.write((command + "\n").encode('utf-8'))
            tn.read_until(b'>')
    except Exception as e:
        print(f"Error sending command to VLC: {e}")

if __name__ == '__main__':
    # Check if Homebridge is already running
    if not is_homebridge_running():
        # Start Homebridge in a separate process
        subprocess.Popen(['homebridge'])
        print("Homebridge started and playlist is playing.")

    app.run(host='0.0.0.0', port=5000)

