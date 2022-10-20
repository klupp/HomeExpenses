#!/bin/sh

project_dir="$( cd "$( dirname "$0" )" && pwd )/app"

OUTFILE=/lib/systemd/system/utilities.service
EXECUTE="cd $project_dir && source ../venv/bin/activate && python main.py FLASK_APP=main.py"
echo $EXECUTE
sudo out=$OUTFILE exec="$EXECUTE" sh -c 'cat << EOF > $out
[Unit]
Description=Home Utilities Service
After=multi-user.target

[Service]
Type=idle
Restart=on-failure
User=root
ExecStart=/bin/bash -c "$exec"

[Install]
WantedBy=multi-user.target
EOF'

python_app=$project_dir"/main.py"

sudo chmod 644 /lib/systemd/system/utilities.service
sudo chmod 755 "$python_app"

sudo systemctl daemon-reload
sudo systemctl enable utilities.service
sudo systemctl start utilities.service
service_status=$(sudo systemctl status utilities.service)
echo "$service_status"
