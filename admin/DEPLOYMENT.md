# Admin Frontend Deployment Guide (Vercel)

## Steps to Deploy Admin App

### 1. Deploy via Vercel Dashboard

1. **Go to vercel.com** and sign in
2. **Click "Add New Project"**
3. **Import your repository** (same repo, different root directory)
4. **Configure:**
   - Framework Preset: Vite
   - Root Directory: `admin`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   
5. **Environment Variables:**
   - Add: `VITE_API_BASE_URL` = `https://your-api.onrender.com`

6. **Click Deploy**

### 2. Deploy via CLI (Alternative)
```bash
cd d:\fynd\admin
vercel
```

---

## After Deployment

You'll get a URL like: `https://admin-review-app.vercel.app`

**Login Credentials:**
- Email: `admin@example.com`
- Password: `admin123`

---

## Security Note

For production, you should:
1. Implement real authentication (not demo login)
2. Add environment-based auth
3. Restrict admin access by IP or VPN
