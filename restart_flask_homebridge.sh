#!/bin/bash

# Reload systemd manager configuration
sudo systemctl daemon-reload

# Restart the flask_homebridge service
sudo systemctl restart flask_homebridge.service

# Check the status of the flask_homebridge service
sudo systemctl status flask_homebridge.service

