# Home Automation with VLC and Flask

This project allows you to control VLC playback on your Raspberry Pi using a Flask-based web server. You can play, stop, pause, and manage playlists via API endpoints, making it easy to automate media playback.

## Features

- **VLC Control**: Start, stop, and control playback using a web interface.
- **Scheduler**: Automate playback actions using a scheduler.
- **Interact from Siri**: Interact with the vlc player on raspberry pi from siri

## Setup and Configuration

### 1. Running the Flask Server

Create a Python script (`server.py`) with the following code:

### 2. Systemd Service Setup

To keep the Flask server running continuously, set it up as a systemd service.

1. **Create the service file**:
   ```bash
   sudo nano /etc/systemd/system/flask_homebridge.service
   ```

2. **Add the following content**:
   ```ini
   [Unit]
   Description=Flask Homebridge Control
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /home/sri/HomeAutomation/server.py
   WorkingDirectory=/home/sri/HomeAutomation
   Restart=always
   User=sri

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start the service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable flask_homebridge.service
   sudo systemctl start flask_homebridge.service
   ```

4. **Check the service status**:
   ```bash
   sudo systemctl status flask_homebridge.service
   ```

### 3. Scheduler Script

To automate playback actions, you can use `play_scheduler.py`.


### 4. Setting Up Cron for Automation

Use crontab to schedule the playback automation.

1. **Edit the crontab**:
   ```bash
   sudo crontab -e
   ```

2. **Add the following line to run the scheduler every day at 6:00 AM**:
   ```bash
   0 6 * * * /usr/bin/python3 /home/sri/HomeAutomation/play_scheduler.py
   ```

### 5. VLC Command for Manual Start

You can manually start VLC to control it via the RC (remote control) interface:

```bash
cvlc --alsa-audio-device=hw:0,0 --extraintf rc --rc-host=localhost:4212 ~/Music/playlist.m3u
```

#### Explanation:
- **`--alsa-audio-device=hw:0,0`**: Forces VLC to use the AUX output.
- **`--extraintf rc`**: Enables the remote control interface.
- **`--rc-host=localhost:4212`**: Sets up remote control via telnet on port 4212.

## Available API Endpoints

- **Start Playlist**:
  ```bash
  curl -X POST http://<your-raspberry-pi-ip>:5000/play_playlist
  ```
- **Stop Playback**:
  ```bash
  curl -X POST http://<your-raspberry-pi-ip>:5000/stop
  ```

(Other API examples go here...)


# Setting Up Siri Shortcut to Start `/play_playlist`

You can use Siri Shortcuts on your iPhone to easily trigger the `/play_playlist` endpoint on your Raspberry Pi, enabling you to start the playlist using a voice command.

## Step-by-Step Guide

### 1. Ensure Your Raspberry Pi is Accessible

- Make sure your Raspberry Pi is connected to your local network and can be accessed via its IP address. 
- You need to know the local IP address of your Raspberry Pi (e.g., `192.168.0.10`).

### 2. Setting Up Flask Endpoint

Before creating the Siri Shortcut, ensure your Flask server is running and that you have the `/play_playlist` endpoint correctly configured as described earlier.

### 3. Create the Shortcut on Your iPhone

1. **In Shortcut App, Create a New Shortcut**:
   - Tap on the **“+”** button in the top right to create a new shortcut.

2. **Add an Action**:
   - Tap **“Add Action”**.
   - select **“URL”**.
   - Enter your Raspberry Pi’s IP address and endpoint in the URL field:
     ```
     http://192.168.0.17:5000/play_playlist
     ```

3. **Add a Second Action**:
   - Tap **“Add Action”** again.
   - type **“Get Contents of URL”** and select it.
   - This action will make a POST request to the URL.

4. **Configure the Method to POST**:
   - Tap **“Show More”** on the **“Get Contents of URL”** action.
   - Change the **“Method”** to **POST**.

7. **Name the Shortcut**:
   - Tap **“Next”** in the top right corner.
   - Give the shortcut a name like **“Play Playlist”**.
   - Tap **“Done”**.

### 4. Use Siri to Start the Playlist

Now that your shortcut is set up, you can activate it by saying:

- **“Hey Siri, Play Playlist”**

Siri will trigger the shortcut, which sends a POST request to your Raspberry Pi’s `/play_playlist` endpoint, starting your playlist.


### Final Notes

With this setup, you can control your Raspberry Pi’s playback conveniently using Siri Shortcuts, making your home automation system even easier to use.

