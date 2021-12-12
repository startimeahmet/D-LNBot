# D-LNBot

## Installing Bitcoin Core
OS version: Ubuntu 15.10 or above \
Get dependencies:

```
sudo apt-get update
sudo apt-get install -y \
  autoconf automake build-essential git libtool libgmp-dev libsqlite3-dev \
  python3 python3-mako python3-pip net-tools zlib1g-dev libsodium-dev \
  gettext
pip3 install --user mrkd
```

Now we can install Bitcoin Core via `snapd`
```
sudo apt-get install snapd
sudo snap install bitcoin-core
# Snap does some weird things with binary names; you'll
# want to add a link to them so everything works as expected
sudo ln -s /snap/bitcoin-core/current/bin/bitcoin{d,-cli} /usr/local/bin/
```

Create `bitcoin.conf`:\
`mkdir ~/.bitcoin` \
`touch ~/.bitcoin/bitcoin.conf`

Copy and paste below to `bitcoin.conf` that was just created
```
server=1
testnet=1
daemon=1
zmqpubrawblock=tcp://127.0.0.1:28332
zmqpubrawtx=tcp://127.0.0.1:28333
rpcuser=user
rpcpassword=passwd
```

## Running Bitcoin Core
Run the following command to start `bitcoind` server:\
`bitcoind`

Check the current block height:\
`bitcoin-cli getblockcount`

If it is equal to block height shown at https://blockstream.info/testnet/, that means node is fully synced.

## Installing `c-lightning`
Clone `c-lightning`:

```
git clone https://github.com/ElementsProject/lightning.git
cd lightning
```

Build lightning:

```
./configure
make
sudo make install
```

Running lightning:

```
./lightningd/lightningd &
./cli/lightning-cli help
```

### Creating a wallet
When `c-lightning` is run for the first time, a new wallet has to be created and funded:\
`./cli/lightning-cli newaddr p2sh-segwit`

Fund the returned wallet address with some testnet Bitcoin from https://testnet-faucet.mempool.co/.

### Creating Channels
To open a channel to 1ml.com's public node with a capacity of 100,000 satoshi.\
Run the following:\

`./cli/lightning-cli fundchannel 0217890e3aad8d35bc054f43acc00084b25229ecff0ab68debd82883ad65ee8266 100000`

### Sending a key send payment
`./cli/lightning-cli keysend destination amt`
