# FlutterFlow POS Blockchain Integration Guide & Testing Plan

## Overview
This guide provides step-by-step instructions to integrate your FlutterFlow wallet with the Python-based Proof-of-Stake blockchain. We'll run everything locally and expose it via ngrok for FlutterFlow access.

## Phase 1: Environment Setup

### 1.1 Install Python & Dependencies
```bash
# Check Python version (need 3.11+)
python --version

# Install dependencies
cd blockchain
pip install -r requirements/prod.txt
```

### 1.2 Install ngrok
```bash
# Using Chocolatey (as you found)
choco install ngrok

# Add your auth token (replace with your actual token)
ngrok config add-authtoken 3010awebrO4lO5AYvx7k2evWBM4_45ALAYwFHDLJELdCuF3dj
```

## Phase 2: Blockchain Setup & Testing

### 2.1 Start Blockchain Node
```bash
# From the blockchain directory
python run_node.py --ip=localhost --node_port=8010 --api_port=8050 --key_file=./keys/genesis_private_key.pem
```

### 2.2 Expose via ngrok
```bash
# In a new terminal
ngrok http 8050
```
**Note**: This will give you a URL like `https://abc123.ngrok.io`

### 2.3 Verify Blockchain is Running
- **Local test**: Visit `http://localhost:8050/api/v1/docs/`
- **Ngrok test**: Visit `https://[your-ngrok-url].ngrok.io/api/v1/docs/`
- **API test**: `https://[your-ngrok-url].ngrok.io/api/v1/blockchain/`

## Phase 3: FlutterFlow API Configuration

### 3.1 Add API Base URL
In FlutterFlow:
1. Go to **API Configuration** section
2. Set **Base URL**: `https://[your-ngrok-url].ngrok.io/api/v1/`
3. Replace `[your-ngrok-url]` with your actual ngrok subdomain

### 3.2 Configure API Endpoints
Add these endpoints to FlutterFlow:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/blockchain/` | GET | Get entire blockchain data |
| `/transaction/transaction_pool/` | GET | Get pending transactions |
| `/transaction/create/` | POST | Create new transaction |
| `/ping/` | GET | Health check |

## Phase 4: Wallet & Transaction Setup

### 4.1 Understanding Wallet Structure
The blockchain uses RSA key pairs:
- **Public Key**: Your wallet address (starts with `-----BEGIN PUBLIC KEY-----`)
- **Private Key**: Used for signing transactions (keep secure)

### 4.2 Test Wallet Setup
For testing, we'll use the provided keys:

**Genesis Wallet** (for testing):
- Private Key: `./keys/genesis_private_key.pem`
- Public Key: `./keys/genesis_public_key.pem`

**Staker Wallet** (for testing):
- Private Key: `./keys/staker_private_key.pem`
- Public Key: `./keys/staker_public_key.pem`

### 4.3 Create Test Transactions
Use the sample script to test:
```bash
python sample_transactions.py
```

## Phase 5: FlutterFlow Integration Testing

### 5.1 Test API Connection
Create a simple test in FlutterFlow:
1. **Test endpoint**: `GET /ping/`
2. **Expected response**: `{"success": "pong!"}`
3. **Success indicator**: 200 status code

### 5.2 Test Blockchain Data Retrieval
1. **Test endpoint**: `GET /blockchain/`
2. **Expected response**: JSON with blockchain data
3. **Verify**: Contains blocks array with transactions

### 5.3 Test Transaction Creation
**Important**: For FlutterFlow to create transactions, you need:
1. **Generate wallet keys** in FlutterFlow (RSA format)
2. **Sign transactions** with private key
3. **Send properly formatted transaction** to `/transaction/create/`

## Phase 6: Wallet Implementation in FlutterFlow

### 6.1 Key Generation Options
**Option A: Use existing test keys**
- Import the genesis/staker keys for testing
- **Risk**: Not secure for production

**Option B: Generate new keys in FlutterFlow**
- Use Flutter cryptography packages
- Generate RSA key pairs matching blockchain format

### 6.2 Transaction Format
Each transaction needs:
```json
{
  "sender_public_key": "-----BEGIN PUBLIC KEY-----\n...",
  "receiver_public_key": "-----BEGIN PUBLIC KEY-----\n...",
  "amount": 10,
  "type": "TRANSFER",
  "signature": "hex_signature_here"
}
```

### 6.3 Signing Process
1. **Create transaction payload** (sender + receiver + amount + type)
2. **Hash the payload** using SHA256
3. **Sign with private key** using RSA-PSS
4. **Send to blockchain** via POST `/transaction/create/`

## Testing Checklist

### ✅ Phase 1: Environment
- [ ] Python 3.11+ installed
- [ ] Dependencies installed (`pip install -r requirements/prod.txt`)
- [ ] ngrok installed and configured

### ✅ Phase 2: Blockchain
- [ ] Blockchain node starts successfully
- [ ] ngrok tunnel active
- [ ] Local API accessible at `http://localhost:8050/api/v1/docs/`
- [ ] Ngrok API accessible at `https://[your-url].ngrok.io/api/v1/docs/`

### ✅ Phase 3: FlutterFlow
- [ ] Base URL configured in FlutterFlow
- [ ] API endpoints added
- [ ] Test connection successful (`/ping/`)

### ✅ Phase 4: Wallet Testing
- [ ] Can retrieve blockchain data
- [ ] Can view transaction pool
- [ ] Can create test transactions (manual or via script)

### ✅ Phase 5: Transaction Flow
- [ ] FlutterFlow can generate wallet keys
- [ ] FlutterFlow can sign transactions
- [ ] FlutterFlow can send transactions to blockchain
- [ ] Transactions appear in blockchain

## Troubleshooting

### Common Issues
1. **Port conflicts**: Use different ports if 8010/8050 are taken
2. **ngrok timeout**: Free ngrok tunnels expire after 2 hours
3. **CORS issues**: May need to configure CORS in FlutterFlow
4. **Key format**: Ensure RSA keys are in PEM format

### Debug Commands
```bash
# Check if blockchain is running
curl http://localhost:8050/ping/

# Check blockchain data
curl http://localhost:8050/api/v1/blockchain/

# Check transaction pool
curl http://localhost:8050/api/v1/transaction/transaction_pool/
```

## Next Steps After Testing
1. **Production deployment** (cloud hosting)
2. **Enhanced security** (proper key management)
3. **Real-time updates** (WebSocket or polling)
4. **Multiple node setup** (for redundancy)

## Reporting Back
After completing each phase, report:
1. **Phase completed** and any issues encountered
2. **API responses** (especially any errors)
3. **Transaction results** (success/failure messages)
4. **Next phase readiness**

Start with Phase 1 and let me know your progress!
