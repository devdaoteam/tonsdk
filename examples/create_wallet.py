from tonsdk.contract.wallet import WalletVersionEnum, Wallets
from tonsdk.crypto import mnemonic_new

from client import TonCenterTonClient


WALLET_WORKCHAIN = 0
WALLET_VERSION = WalletVersionEnum.v3r2
wallet_mnemonics = mnemonic_new()

_, _, _, wallet = Wallets.from_mnemonics(
    wallet_mnemonics, WALLET_VERSION, WALLET_WORKCHAIN)

# At this moment contract address is only calculated and
# it needs to be deployed to blockchain.
print("Wallet address:", wallet.address.to_string(True, True, True))
print("Mnemonics:", " ".join(wallet_mnemonics))

with open("SEED.txt", "w") as f:
    f.write(" ".join(wallet_mnemonics))

print("\nNow you need to send some coins to this address to deploy contract.")
input("\nPress Enter when you are ready...")

# Forming an external message with contract's data to deploy it.
query = wallet.create_init_external_message()

# Creating client instance for interaction with TON blockchain via API.
client = TonCenterTonClient()

# Sending external message to blockchain.
# BOC - Bag Of Cells - binary format for storing serialized TON data.
print(client.send_boc(query["message"].to_boc(False)))
