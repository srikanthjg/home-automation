import logging
from logging.handlers import RotatingFileHandler
import requests
from datetime import datetime

# Configure logging with rotation after 1000 bytes
log_file = '/home/sri/HomeAutomation/log/play_scheduler.log'
handler = RotatingFileHandler(log_file, maxBytes=1000, backupCount=0)  # Rotate after 1000 bytes, keep 0 backup
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger('play_scheduler')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Flask server URL
FLASK_URL = "http://localhost:5000"

def log_and_request(endpoint, action_description):
    """Send a POST request to Flask app and log the response."""
    try:
        url = f"{FLASK_URL}{endpoint}"
        response = requests.post(url)

        # Check if response contains JSON data
        if response.status_code == 200:
            try:
                response_json = response.json()
                logger.info(f"{action_description} successful: {response_json}")
            except ValueError:  # Handle cases where the response isn't JSON
                logger.info(f"{action_description} successful: {response.text}")
        else:
            logger.error(f"{action_description} failed: {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"Exception while {action_description}: {e}")

def schedule_vlc_action():
    """Schedule the playback and stop actions for VLC."""
    # Get the current time for logging (not used in decision-making)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"Scheduler running at {current_time}")

    # 1. Stop VLC if it's running before starting a new playlist
    log_and_request('/stop', 'Stopping VLC')

    # 2. Play the playlist
    log_and_request('/play_playlist', 'Playing playlist')

if __name__ == '__main__':
    logger.info("Scheduler started")
    schedule_vlc_action()
    logger.info("Scheduler finished")

