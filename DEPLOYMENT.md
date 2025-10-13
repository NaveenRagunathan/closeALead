# 🚀 CloseALead Deployment Guide

## Local Development (Already Set Up)

### Quick Start
```bash
# Terminal 1 - Backend
./start-backend.sh

# Terminal 2 - Frontend  
./start-frontend.sh
```

---

## Production Deployment Options

### Option A: Netlify (Frontend) + Render (Backend)

This is a great “serverless static + managed API” setup.

#### 1) Backend on Render

1. Push this repository to GitHub.
2. In Render, click “New +” → “Web Service”.
3. Connect your GitHub repo.
4. Service Settings:
   - Name: `closealead-backend`
   - Root Directory: `backend`
   - Environment: Docker (we ship a `backend/Dockerfile`)
   - Health Check Path: `/`
5. If Render detects Docker automatically, you’re set. If not, use these commands:
   - Build Command: (not needed with Docker)
   - Start Command: (not needed with Docker)
6. Environment Variables (Render → your service → Environment):
   ```env
   # Recommended
   DATABASE_URL=postgresql://<user>:<pass>@<host>:5432/<db>   # Use Render PostgreSQL add-on
   
   # Required
   SECRET_KEY=<long-random-string>
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION=86400
   OPENAI_API_KEY=sk-...
   
   # CORS (add your Netlify domain once created)
   CORS_ORIGINS=https://<your-netlify-site>.netlify.app, https://<your-custom-domain>
   ```
7. Click “Create Web Service” and wait for deploy.
8. Copy your backend URL, e.g. `https://closealead-backend.onrender.com`.

Notes:
- SQLite is fine for quick tests, but switch to Render PostgreSQL for production.
- Our `render.yaml` in the repo can be used for Infrastructure-as-Code (optional).

#### 2) Frontend on Netlify

1. In Netlify, click “Add new site” → “Import from Git”.
2. Connect your GitHub repo.
3. Build Settings:
   - Build Command: `npm run build`
   - Publish Directory: `dist`
   - Node Version: `18` (set in `netlify.toml` already)
4. Environment Variables (Netlify → Site settings → Environment):
   ```env
   VITE_API_URL=https://closealead-backend.onrender.com
   ```
5. Redirects/Proxy for SPA + API:
   - We added `netlify.toml` with:
     ```toml
     [[redirects]]
     from = "/api/*"
     to = "https://your-render-backend.onrender.com/:splat"
     status = 200
     force = true

     [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
     ```
   - Replace `your-render-backend.onrender.com` with your actual Render backend URL.
6. Deploy the site.

After deploy:
- Frontend should be available at `https://<your-netlify-site>.netlify.app`
- Backend at `https://<your-render-service>.onrender.com`
- API docs: `https://<your-render-service>.onrender.com/docs`

#### 3) Post-deploy checks

1. Test CORS:
   - Open the Netlify URL and ensure API calls succeed (Network tab).
2. Update CORS if needed:
   - Add your Netlify/custom domains in `CORS_ORIGINS` on Render and redeploy.
3. Update Frontend Env if backend changes:
   - Change `VITE_API_URL` in Netlify env and trigger a redeploy.

Troubleshooting:
- 401/403: Ensure JWT secrets and CORS are set correctly on the backend.
- 404 on SPA routes: Ensure the SPA redirect is enabled (in `netlify.toml`).
- Mixed content: Ensure both frontend and backend are HTTPS.

### Option 1: Vercel (Frontend) + Railway (Backend)

#### **Frontend to Vercel**

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Build and Deploy**
```bash
npm run build
vercel --prod
```

3. **Configure Environment**
```
VITE_API_URL=https://your-backend.railway.app
```

#### **Backend to Railway**

1. **Install Railway CLI**
```bash
npm i -g @railway/cli
```

2. **Deploy**
```bash
cd backend
railway login
railway init
railway up
```

3. **Add Environment Variables in Railway Dashboard**
```
DATABASE_URL=postgresql://...  (Railway provides this)
SECRET_KEY=your-production-secret
OPENAI_API_KEY=sk-your-key
CORS_ORIGINS=https://your-app.vercel.app
```

4. **PostgreSQL Setup**
```bash
railway add postgresql
# DATABASE_URL automatically set
```

---

### Option 2: Render (Full Stack)

#### **Backend Service**

1. Create new Web Service on Render
2. Connect GitHub repo
3. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3.11

4. Environment Variables:
```
DATABASE_URL=postgresql://... (from Render Postgres)
SECRET_KEY=random-secure-key-here
OPENAI_API_KEY=sk-your-key
CORS_ORIGINS=https://your-frontend.onrender.com
```

#### **Frontend Static Site**

1. Create new Static Site
2. Settings:
   - **Build Command**: `npm run build`
   - **Publish Directory**: `dist`
3. Environment:
```
VITE_API_URL=https://your-backend.onrender.com
```

---

### Option 3: AWS (Scalable)

#### **Frontend - S3 + CloudFront**

1. **Build**
```bash
npm run build
```

2. **S3 Bucket**
- Create bucket: `closealead-frontend`
- Enable static hosting
- Upload `dist/*` files

3. **CloudFront**
- Create distribution pointing to S3
- Configure custom domain
- Enable HTTPS

#### **Backend - EC2 + RDS**

1. **EC2 Instance**
```bash
# SSH into instance
ssh ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3.11 python3-pip nginx

# Clone repo
git clone your-repo
cd closealead/backend

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure systemd service
sudo nano /etc/systemd/system/closealead.service
```

**closealead.service:**
```ini
[Unit]
Description=CloseALead API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/closealead/backend
Environment="PATH=/home/ubuntu/closealead/backend/venv/bin"
ExecStart=/home/ubuntu/closealead/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable closealead
sudo systemctl start closealead
```

2. **RDS PostgreSQL**
- Create RDS instance
- Note connection string
- Update DATABASE_URL in .env

3. **Nginx Reverse Proxy**
```nginx
server {
    listen 80;
    server_name api.closealead.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

### Option 4: Docker (Any Platform)

#### **Build Images**

**Frontend Dockerfile:**
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Build and Run:**
```bash
# Backend
cd backend
docker build -t closealead-backend .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-xxx closealead-backend

# Frontend
docker build -t closealead-frontend .
docker run -p 3000:80 closealead-frontend
```

#### **Docker Compose (Provided)**
```bash
docker-compose up -d
```

---

## Database Migration

### From SQLite to PostgreSQL

1. **Export SQLite data** (if needed)
```bash
sqlite3 closealead.db .dump > backup.sql
```

2. **Update .env**
```env
DATABASE_URL=postgresql://user:pass@host:5432/closealead
```

3. **Restart backend**
- Tables auto-created by SQLAlchemy

---

## Environment Variables Checklist

### Production Backend
```env
✅ DATABASE_URL=postgresql://...
✅ SECRET_KEY=long-random-string-min-32-chars
✅ OPENAI_API_KEY=sk-your-key
✅ CORS_ORIGINS=https://your-frontend-domain.com
✅ STRIPE_SECRET_KEY=sk_live_... (if using payments)
✅ AWS_ACCESS_KEY_ID=... (if using S3)
✅ AWS_SECRET_ACCESS_KEY=...
✅ S3_BUCKET=closealead-production
```

### Production Frontend
```env
✅ VITE_API_URL=https://api.yourdomain.com
```

---

## SSL/HTTPS Setup

### Let's Encrypt (Free)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

Auto-renewal:
```bash
sudo certbot renew --dry-run
```

---

## Performance Optimization

### Frontend
1. **Enable Gzip** (nginx.conf)
```nginx
gzip on;
gzip_types text/css application/javascript application/json;
```

2. **Cache Static Assets**
```nginx
location /assets/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Backend
1. **Gunicorn Workers**
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. **Redis Caching** (optional)
```python
# Add to requirements.txt
redis==5.0.1

# Cache frequently accessed data
```

---

## Monitoring

### 1. Sentry (Error Tracking)

**Frontend:**
```bash
npm install @sentry/react
```

**Backend:**
```bash
pip install sentry-sdk
```

### 2. Uptime Monitoring
- UptimeRobot (free)
- Pingdom
- AWS CloudWatch

### 3. Logs
```bash
# View logs
tail -f /var/log/closealead/app.log

# Or with Docker
docker logs -f closealead-backend
```

---

## Backup Strategy

### Database Backups

**Automated Daily Backup:**
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d)
pg_dump $DATABASE_URL > /backups/closealead-$DATE.sql
aws s3 cp /backups/closealead-$DATE.sql s3://closealead-backups/

# Delete backups older than 30 days
find /backups -name "closealead-*.sql" -mtime +30 -delete
```

**Cron Job:**
```bash
0 2 * * * /path/to/backup.sh
```

---

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**
   - AWS ELB
   - Nginx load balancer
   - Cloudflare

2. **Multiple Backend Instances**
```bash
# Instance 1
uvicorn main:app --port 8000

# Instance 2
uvicorn main:app --port 8001
```

3. **Database Read Replicas**
   - PostgreSQL replication
   - Read from replicas
   - Write to primary

---

## Cost Estimation

### Small Scale (< 100 users)
- **Vercel Free** + **Railway Hobby ($5/mo)** = **$5/month**
- **Render Free tier** (both) = **$0/month** (with limitations)

### Medium Scale (100-1000 users)
- **Vercel Pro ($20)** + **Railway Pro ($20)** + **PostgreSQL ($15)** = **$55/month**

### Large Scale (1000+ users)
- **AWS**: $100-500/month depending on traffic
- Consider reserved instances for cost savings

---

## Security Checklist

- [x] HTTPS enabled everywhere
- [x] Environment variables not committed
- [x] CORS properly configured
- [x] SQL injection prevention (ORM)
- [x] XSS protection (React)
- [x] Rate limiting on API
- [x] JWT tokens with expiry
- [x] Password hashing (bcrypt)
- [ ] Regular security audits
- [ ] Dependency updates
- [ ] Penetration testing

---

## Post-Deployment Testing

1. **Smoke Tests**
```bash
# Check backend health
curl https://api.yourdomain.com/health

# Check frontend loads
curl https://yourdomain.com
```

2. **Full User Flow**
- Sign up new user
- Create offer
- Export PDF
- Verify emails work (if implemented)

3. **Performance**
- Run Lighthouse audit
- Check API response times
- Monitor error rates

---

## Rollback Strategy

### Quick Rollback
```bash
# Vercel
vercel rollback

# Railway
railway rollback

# Docker
docker-compose down
docker-compose up -d --build
```

### Database Rollback
```bash
# Restore from backup
psql $DATABASE_URL < /backups/closealead-20251013.sql
```

---

## Support Resources

- **Documentation**: All docs in `/docs`
- **API Reference**: `/docs` endpoint
- **Monitoring**: Sentry dashboard
- **Logs**: Platform-specific dashboards

---

## Next Steps After Deployment

1. ✅ Verify all features work in production
2. ✅ Test payment flow (if implemented)
3. ✅ Monitor error rates for 24 hours
4. ✅ Set up automated backups
5. ✅ Configure monitoring alerts
6. ✅ Add custom domain
7. ✅ Enable analytics
8. ✅ Create status page
9. ✅ Document incident response
10. ✅ Plan for scaling

---

**Deployment Checklist Complete! 🎉**
