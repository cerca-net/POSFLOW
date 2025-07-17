# FlutterFlow API Configuration - Exact Setup Guide

## Quick Start Configuration

### 1. Base API Setup
- **Base URL**: `http://localhost:8050/api/v1/`
- **No authentication required**
- **No special headers needed for GET requests**

### 2. Individual Endpoints to Configure

#### ✅ Health Check (Start Here)
**Purpose**: Test if blockchain is reachable
- **Method**: GET
- **Full URL**: `http://localhost:8050/api/v1/ping/`
- **Headers**: None
- **Query Parameters**: None
- **Expected Response**: `{"success": "pong!"}`

#### ✅ Get Blockchain Data
**Purpose**: View all blockchain data
- **Method**: GET
- **Full URL**: `http://localhost:8050/api/v1/blockchain/`
- **Headers**: None
- **Query Parameters**: None
- **Expected Response**: JSON with blocks and transactions

#### ✅ Get Transaction Pool
**Purpose**: View pending transactions
- **Method**: GET
- **Full URL**: `http://localhost:8050/api/v1/transaction/transaction_pool/`
- **Headers**: None
- **Query Parameters**: None
- **Expected Response**: Array of transactions (currently empty)

#### 🔄 Create Transaction (Advanced)
**Purpose**: Send new transactions
- **Method**: POST
- **Full URL**: `http://localhost:8050/api/v1/transaction/create/`
- **Headers**: 
  - `Content-Type: application/json`
- **Body Format**:
```json
{
  "transaction": "base64_encoded_signed_transaction"
}
```

## FlutterFlow Step-by-Step Setup

### Step 1: Add API Call
1. Go to **API Calls** in FlutterFlow
2. Click **+ Add API Call**
3. **Name**: "Test Connection"
4. **Method**: GET
5. **URL**: `http://localhost:8050/api/v1/ping/`
6. **Headers**: Leave empty
7. **Query Parameters**: Leave empty
8. **Test** - should return `{"success": "pong!"}`

### Step 2: Test Connection
1. Click **Test API Call**
2. Should see green success indicator
3. Response should show: `{"success": "pong!"}`

### Step 3: Add Blockchain Data Call
1. **Name**: "Get Blockchain"
2. **Method**: GET
3. **URL**: `http://localhost:8050/api/v1/blockchain/`
4. **Headers**: None
5. **Query Parameters**: None

### Step 4: Local Testing Notes
- **Your computer must be running** the blockchain
- **Same WiFi network** for mobile testing
- **No firewall blocking** port 8050
- **Use computer's IP** for mobile: `http://[YOUR-IP]:8050/api/v1/`

## Testing Order
1. **Start with GET /ping/** - verify connection works
2. **Test GET /blockchain/** - verify data retrieval
3. **Then add POST transaction** - requires wallet setup

## Troubleshooting
- **Connection failed**: Check blockchain is running
- **CORS issues**: May need to add CORS headers in FlutterFlow
- **Localhost vs IP**: Use computer's IP address for mobile testing

## Ready to Test
Start with the health check endpoint - it's the simplest and will confirm your connection works!
