# DataDrape AI - Deployment Guide

This guide covers various deployment options for DataDrape AI, from local development to production deployment.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [VPS Deployment](#vps-deployment)
4. [GitHub Pages + Backend Service](#github-pages--backend-service)
5. [SSL/TLS Setup](#ssltls-setup)
6. [Monitoring & Maintenance](#monitoring--maintenance)

## Local Development

### Quick Start

1. **Setup Environment**
```bash
cp .env.example .env
# Edit .env with your API key
```

2. **Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Run Development Server**
```bash
export FLASK_ENV=development
python app.py
```

### Development Tips

- Enable hot reload by setting `FLASK_ENV=development`
- Use `ngrok` for testing with HTTPS locally
- Monitor logs in real-time for debugging

## Docker Deployment

### Basic Docker Setup

1. **Build and Run**
```bash
docker build -t datadrape-ai .
docker run -p 5000:5000 --env-file .env datadrape-ai
```

2. **Using Docker Compose**
```bash
# Development
docker-compose up

# Production with nginx
docker-compose --profile production up -d
```

### Docker Configuration

**Custom docker-compose.override.yml** for local development:
```yaml
version: '3.8'
services:
  datadrape:
    environment:
      - FLASK_ENV=development
    volumes:
      - ./app.py:/app/app.py
      - ./index.html:/app/index.html
```

### Docker Hub Deployment

1. **Build and Tag**
```bash
docker build -t yourusername/datadrape-ai:latest .
docker push yourusername/datadrape-ai:latest
```

2. **Deploy on Any Docker Host**
```bash
docker run -d \
  --name datadrape \
  -p 5000:5000 \
  --env-file .env \
  --restart unless-stopped \
  yourusername/datadrape-ai:latest
```

## VPS Deployment

### Prerequisites

- Ubuntu 20.04+ or similar Linux distribution
- Domain name pointed to your VPS
- SSH access with sudo privileges

### Step-by-Step Deployment

1. **Update System**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx certbot python3-certbot-nginx -y
```

2. **Clone Repository**
```bash
cd /opt
sudo git clone https://github.com/yourusername/datadrape-ai.git
sudo chown -R $USER:$USER datadrape-ai
cd datadrape-ai
```

3. **Setup Python Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
nano .env  # Add your API key
```

5. **Setup Systemd Service**
```bash
sudo cp datadrape.service /etc/systemd/system/
sudo nano /etc/systemd/system/datadrape.service  # Update paths and API key
sudo systemctl daemon-reload
sudo systemctl enable datadrape
sudo systemctl start datadrape
```

6. **Configure Nginx**
```bash
sudo cp nginx.conf.example /etc/nginx/sites-available/datadrape
sudo nano /etc/nginx/sites-available/datadrape  # Update server_name
sudo ln -s /etc/nginx/sites-available/datadrape /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Setup SSL with Let's Encrypt**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Firewall Configuration

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## GitHub Pages + Backend Service

### Hybrid Deployment Strategy

Host the frontend on GitHub Pages (free) and backend on a small VPS or cloud service.

1. **Setup GitHub Pages**

Create `gh-pages` branch:
```bash
git checkout -b gh-pages
# Keep only index.html and CNAME
git rm -rf *.py *.txt *.sh *.bat Dockerfile docker-compose.yml
git commit -m "GitHub Pages setup"
git push origin gh-pages
```

2. **Update Frontend for Remote Backend**

Edit `index.html`:
```javascript
const BACKEND_URL = 'https://api.yourdomain.com';
```

3. **Configure CORS on Backend**

Update `app.py`:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://yourdomain.github.io', 'https://yourdomain.com'])
```

4. **Deploy Backend Separately**

Use any of these services:
- **Heroku**: Free tier available
- **Railway**: Simple deployment
- **DigitalOcean App Platform**: $5/month
- **AWS Lambda**: Pay per request

### Heroku Deployment Example

1. **Create Heroku App**
```bash
heroku create your-app-name
heroku config:set OPENROUTER_API_KEY=your-key-here
```

2. **Add Procfile**
```
web: gunicorn app:app
```

3. **Deploy**
```bash
git push heroku main
```

## SSL/TLS Setup

### Let's Encrypt (Recommended)

1. **Install Certbot**
```bash
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

2. **Obtain Certificate**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. **Auto-Renewal**
```bash
sudo certbot renew --dry-run
# Cron job is automatically created
```

### Manual SSL Setup

1. **Generate Self-Signed Certificate** (for testing)
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/datadrape.key \
  -out /etc/ssl/certs/datadrape.crt
```

2. **Configure Nginx**
```nginx
ssl_certificate /etc/ssl/certs/datadrape.crt;
ssl_certificate_key /etc/ssl/private/datadrape.key;
```

## Monitoring & Maintenance

### Health Checks

1. **Setup Uptime Monitoring**
   - Use services like UptimeRobot or Pingdom
   - Monitor endpoint: `https://yourdomain.com/health`

2. **Log Monitoring**
```bash
# View logs
sudo journalctl -u datadrape -f

# Export logs
sudo journalctl -u datadrape --since "1 hour ago" > datadrape.log
```

### Backup Strategy

1. **Automated Backups**
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf /backup/datadrape_$DATE.tar.gz /opt/datadrape-ai
find /backup -name "datadrape_*.tar.gz" -mtime +7 -delete
```

2. **Cron Job**
```bash
0 2 * * * /opt/scripts/backup.sh
```

### Performance Optimization

1. **Nginx Caching**
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

2. **Gunicorn Workers**
```python
# gunicorn_config.py
workers = multiprocessing.cpu_count() * 2 + 1
```

3. **Database Connection Pooling** (if using database)
```python
# Use connection pooling for better performance
```

### Security Best Practices

1. **Regular Updates**
```bash
# System updates
sudo apt update && sudo apt upgrade -y

# Python packages
pip install --upgrade -r requirements.txt
```

2. **Security Headers**
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
```

3. **Rate Limiting**
```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api/ {
    limit_req zone=api burst=20 nodelay;
}
```

### Troubleshooting

**Common Issues:**

1. **502 Bad Gateway**
   - Check if backend is running: `sudo systemctl status datadrape`
   - Check logs: `sudo journalctl -u datadrape -n 50`

2. **SSL Certificate Issues**
   - Renew certificate: `sudo certbot renew`
   - Check nginx config: `sudo nginx -t`

3. **High Memory Usage**
   - Reduce gunicorn workers
   - Add swap space if needed

**Debug Commands:**
```bash
# Check service status
sudo systemctl status datadrape

# Test backend directly
curl http://localhost:5000/health

# Check nginx errors
sudo tail -f /var/log/nginx/error.log
```

## Production Checklist

- [ ] SSL/TLS certificate installed
- [ ] Environment variables secured
- [ ] Firewall configured
- [ ] Automated backups enabled
- [ ] Monitoring setup
- [ ] Error logging configured
- [ ] Rate limiting enabled
- [ ] Security headers added
- [ ] Auto-restart on failure
- [ ] Regular update schedule

---

For additional support, please refer to the main [README.md](README.md) or open an issue on GitHub.