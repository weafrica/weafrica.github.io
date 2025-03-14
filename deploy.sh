[Unit]
Description=Gunicorn instance to serve yourapp
After=network.target

[Service]
User=youruser
Group=www-data
WorkingDirectory=/mnt/c/Users/saule/OneDrive/Documents/weafrica.github.io
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app

[Install]
WantedBy=multi-user.target