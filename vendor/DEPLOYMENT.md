# Vendor Frontend Deployment Guide (Vercel)

## Steps to Deploy Vendor App

### 1. Install Vercel CLI (Optional)
```bash
npm install -g vercel
```

### 2. Deploy via Vercel Dashboard (Easiest)

1. **Go to vercel.com** and sign in with GitHub
2. **Click "Add New Project"**
3. **Import your repository**
4. **Configure:**
   - Framework Preset: Vite
   - Root Directory: `vendor`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   
5. **Environment Variables:**
   - Add: `VITE_API_BASE_URL` = `https://your-api.onrender.com`

6. **Click Deploy**

### 3. Deploy via CLI (Alternative)
```bash
cd d:\fynd\vendor
vercel
```

Follow the prompts:
- Set up and deploy? Y
- Which scope? (your account)
- Link to existing project? N
- Project name: vendor-review-app
- Directory: ./
- Override settings? N

---

## After Deployment

You'll get a URL like: `https://vendor-review-app.vercel.app`

### Update API URL
Make sure your deployed app points to the deployed backend:
- In Vercel dashboard → Settings → Environment Variables
- Add: `VITE_API_BASE_URL` = `https://your-backend-api.onrender.com`
- Redeploy

---

## Custom Domain (Optional)

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain (e.g., `vendor.yourdomain.com`)
3. Update DNS records as instructed by Vercel
