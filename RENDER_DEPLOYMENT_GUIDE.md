# Render.com Deployment Guide for POS Blockchain

## 🚀 **Step-by-Step Render.com Deployment**

### **Step 1: Prepare for Deployment**

#### **1.1 Create Required Files**
Create these files in your project root:

**render.yaml** (deployment configuration):
```yaml
services:
  - type: web
    name: pos-blockchain
    env: python
    buildCommand: pip install -r blockchain/requirements/prod.txt
    startCommand: python blockchain/run_node.py --ip=0.0.0.0 --node_port=$PORT --api_port=$PORT --key_file=./blockchain/keys/genesis_private_key.pem
    envVars:
      - key: PYTHONPATH
        value: .
```

**runtime.txt** (Python version):
```
python-3.11.0
```

### **Step 2: Create Render Account**

1. **Go to**: https://render.com
2. **Sign up** with GitHub
3. **Connect your GitHub account**

### **Step 3: Deploy to Render**

#### **Option A: GitHub Deployment (Recommended)**

1. **Fork this repository** to your GitHub account
2. **Go to Render Dashboard**
3. **Click "New" → "Web Service"**
4. **Connect your GitHub account**
5. **Select your forked repository**
6. **Configure settings**:
   - **Name**: `pos-blockchain`
   - **Environment**: Python
   - **Build Command**: `pip install -r blockchain/requirements/prod.txt`
   - **Start Command**: `python blockchain/run_node.py --ip=0.0.0.0 --node_port=$PORT --api_port=$PORT --key_file=./blockchain/keys/genesis_private_key.pem`
   - **Instance Type**: Free

7. **Click "Create Web Service"**

#### **Option B: Manual Deployment**

1. **Create new web service**
2. **Upload your code**
3. **Use the same configuration as above**

### **Step 4: Environment Variables**

Add these environment variables in Render:
- **PYTHONPATH**: `.`
- **PORT**: (Render will set this automatically)

### **Step 5: Deploy & Test**

1. **Wait for deployment** (2-3 minutes)
2. **Get your URL**: `https://your-app.onrender.com`
3. **Test endpoints**:
   - `https://your-app.onrender.com/ping/`
   - `https://your-app.onrender.com/api/v1/blockchain/`

### **Step 6: FlutterFlow Configuration**

Once deployed, use these URLs in FlutterFlow:
- **Base URL**: `https://your-app.onrender.com/`
- **Health Check**: `https://your-app.onrender.com/ping/`
- **Blockchain Data**: `https://your-app.onrender.com/api/v1/blockchain/`
- **Transaction Pool**: `https://your-app.onrender.com/api/v1/transaction/transaction_pool/`

## 📋 **Complete Deployment Checklist**

### **Before Deployment:**
- [ ] Fork this repository to your GitHub
- [ ] Create Render.com account
- [ ] Connect GitHub to Render

### **During Deployment:**
- [ ] Create render.yaml file
- [ ] Configure Python environment
- [ ] Set correct start command
- [ ] Deploy and wait for completion

### **After Deployment:**
- [ ] Test all endpoints
- [ ] Update FlutterFlow with cloud URLs
- [ ] Verify FlutterFlow connection

## 🎯 **Expected Timeline**
- **Setup**: 5 minutes
- **Deployment**: 2-3 minutes
- **Testing**: 2 minutes
- **Total**: ~10 minutes

## **Ready to Deploy!**
Your blockchain is perfectly configured - just needs to be deployed to Render.com for FlutterFlow access!
