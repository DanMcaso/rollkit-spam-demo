```python
import requests
import json
import base64
import random
import string
from ecdsa import SigningKey, SECP256k1
from bech32 import bech32_encode, convertbits

# RPC endpoint
RPC_URL = "http://localhost:26657"

# Replace with actual values (export private key via: rollkit keys export alice --unsafe --unarmored-hex)
ALICE_PRIV_KEY_HEX = "YOUR_ALICE_PRIVATE_KEY_HERE"  # Placeholder
ALICE_ADDR = "rollkit1..."  # Placeholder: Replace with actual Alice address
BOB_ADDR = "rollkit1..."    # Placeholder: Replace with actual Bob address
CHAIN_ID = "rollkit-local"
DENOM = "token"

def generate_large_memo(size=1024):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

def sign_tx(priv_key_hex, tx):
    sk = SigningKey.from_string(bytes.fromhex(priv_key_hex), curve=SECP256k1)
    msg_hash = hash(json.dumps(tx).encode())  # Simplified; use StdSignDoc in production
    signature = sk.sign(msg_hash)
    return base64.b64encode(signature).decode()

def send_tx(to_addr, amount, memo):
    tx_body = {
        "messages": [{
            "@type": "/cosmos.bank.v1beta1.MsgSend",
            "from_address": ALICE_ADDR,
            "to_address": to_addr,
            "amount": [{"denom": DENOM, "amount": str(amount)}]
        }],
        "memo": memo
    }
    
    account_res = requests.get(f"{RPC_URL}/cosmos/auth/v1beta1/accounts/{ALICE_ADDR}").json()
    account_num = account_res['account']['account_number']
    sequence = account_res['account']['sequence']
    
    auth_info = {
        "signer_infos": [{"mode_info": {"single": {"mode": "SIGN_MODE_DIRECT"}}}],
        "fee": {"amount": [{"denom": DENOM, "amount": "2000"}], "gas_limit": "200000"}
    }
    
    tx = {"body": tx_body, "auth_info": auth_info, "signatures": []}
    sig = sign_tx(ALICE_PRIV_KEY_HEX, tx)
    tx['signatures'] = [sig]
    
    broadcast_payload = {"tx_bytes": base64.b64encode(json.dumps(tx).encode()).decode(), "mode": "BROADCAST_MODE_BLOCK"}
    res = requests.post(f"{RPC_URL}/cosmos/tx/v1beta1/txs", json=broadcast_payload)
    return res.json()

# Spam loop
for i in range(100):
    memo = generate_large_memo(1024)
    response = send_tx(BOB_ADDR, 1, memo)
    print(f"Sent tx {i}: {response.get('txhash', 'Error')}")
```