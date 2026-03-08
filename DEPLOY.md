# Local

cd wall-stash
python3 manage.py runserver

# VPS

## Initial setup

### Update
sudo apt update && sudo apt upgrade -y

### Prerequisites
sudo apt install python3 python3-pip python3-venv nginx git ufw -y

### Clone repo
cd /var/www
sudo git clone https://github.com/wojciech-szyba/stash-wall

### Init virtual environment
python3 -m venv venv
source venv/bin/activate

### Python prerequisites
pip install --upgrade pip
pip install -r requirements.txt

## User settings
sudo chown -R webapp:www-data /var/www/stash-wall/
chmod -R 755 /var/www/stash-wall/
chmod 700 /var/www/stash-wall//venv

## Service setup (gunicorn)
nano /etc/systemd/system/wall-stash.service
sudo systemctl daemon-reload && sudo systemctl restart wall-stash
