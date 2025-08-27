```bash
#!/bin/bash

# Spam Rollkit chain with large-payload transactions
for i in {1..100}; do
  # Generate ~1KB random memo
  LARGE_MEMO=$(head -c 1024 /dev/urandom | base64 -w 0)
  
  rollkit tx bank send $ALICE_ADDR $BOB_ADDR 1token \
    --chain-id $CHAIN_ID \
    --keyring-backend test \
    --node tcp://localhost:26657 \
    --memo "$LARGE_MEMO" \
    --yes \
    --gas auto \
    --fees 2000token
  
  echo "Sent tx $i with large memo"
  sleep 0.1  # Adjust for throughput
done
```