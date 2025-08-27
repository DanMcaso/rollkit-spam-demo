```markdown
# Rollkit Chain Spamming Demo

This demo sets up a Rollkit sovereign rollup with a local data availability (DA) layer and spams it with transactions containing large payloads (~1KB memos) to test speed and throughput. It includes a Bash script (`spam.sh`) for simple CLI-based spamming and a Python script (`spam.py`) for programmatic interaction via RPC, simulating full-stack app logic.

## Prerequisites
- Go 1.22+ (for Rollkit CLI)
- Docker (for local DA)
- Python 3.8+ (optional, for `spam.py`)
- Terminal access

## Setup Instructions

1. **Install Rollkit CLI**:
   ```bash
   git clone https://github.com/rollkit/rollkit.git
   cd rollkit
   make install
   ```
   Verify installation:
   ```bash
   rollkit version
   ```
   If issues arise, use:
   ```bash
   curl -L https://rollkit.dev/install.sh | bash
   ```

2. **Start Local DA Layer**:
   Run the provided script to start a local DA node (listens on port 7980):
   ```bash
   bash setup-local-da.sh
   ```
   Keep this terminal open.

3. **Start Rollkit Node**:
   Start the sovereign rollup node in aggregator mode for high throughput:
   ```bash
   rollkit start \
     --rollkit.aggregator true \
     --rollkit.da_address http://localhost:7980 \
     --rollkit.sequencer_rollup_id test-chain \
     --rollkit.namespace_id 0000000000000000000000000000000000000000000000000000000000000001 \
     --rollkit.da_start_height 0 \
     --rpc.laddr tcp://0.0.0.0:26657 \
     --log_level info
   ```
   Monitor logs for block production (e.g., "Finalized block height=X num_txs=Y").

4. **Add and Fund Accounts**:
   Add test accounts:
   ```bash
   rollkit keys add alice --keyring-backend test --chain-id rollkit-local
   rollkit keys add bob --keyring-backend test --chain-id rollkit-local
   ```
   Export addresses for scripting:
   ```bash
   export ALICE_ADDR=$(rollkit keys show alice -a --keyring-backend test)
   export BOB_ADDR=$(rollkit keys show bob -a --keyring-backend test)
   export CHAIN_ID=rollkit-local
   ```
   Update `config/genesis.json` with `ALICE_ADDR` and `BOB_ADDR` (replace placeholders) to assign initial balances. Copy to `~/.rollkit/config/genesis.json` and restart the node:
   ```bash
   cp config/genesis.json ~/.rollkit/config/genesis.json
   ```

5. **Run Spam Script**:
   - **Option 1: Bash (simpler)**:
     Run the Bash script to send 100 transactions with ~1KB random memos:
     ```bash
     bash spam.sh
     ```
   - **Option 2: Python (programmatic)**:
     Install dependencies:
     ```bash
     pip install ecdsa bech32
     ```
     Update `spam.py` with `ALICE_PRIV_KEY_HEX`, `ALICE_ADDR`, and `BOB_ADDR` (export private key via `rollkit keys export alice --unsafe --unarmored-hex`). Run:
     ```bash
     python spam.py
     ```

6. **Monitor Results**:
   - Check node logs for block production and transaction counts.
   - Query balance:
     ```bash
     rollkit query bank balances $ALICE_ADDR --chain-id $CHAIN_ID --node tcp://localhost:26657
     ```
   - Query a transaction:
     ```bash
     rollkit query tx <tx_hash> --chain-id $CHAIN_ID --node tcp://localhost:26657
     ```

7. **Cleanup**:
   - Stop the Rollkit node: Ctrl+C in the node terminal.
   - Stop the DA container: Ctrl+C in the DA terminal or `docker stop $(docker ps -q --filter ancestor=rollkit/local-da)`.

## Notes
- **Throughput**: Locally, expect 10-100 txs/block at 1-5s/block intervals. Adjust `sleep` in `spam.sh` or run multiple instances for higher TPS.
- **Payload Size**: Both scripts use ~1KB memos to simulate large payloads. Rollkit's modular DA layer handles these efficiently.
- **Production**: For real-world testing, replace local DA with Celestia mainnet.
- **Troubleshooting**: Check Rollkit GitHub issues or Telegram for support.

## Files
- `setup-local-da.sh`: Script to start the local DA layer.
- `spam.sh`: Bash script to spam 100 transactions with large memos.
- `spam.py`: Python script for programmatic spamming via RPC.
- `config/genesis.json`: Sample genesis file with placeholders for account addresses.
```