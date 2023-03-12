from tonsdk.crypto import mnemonic_to_wallet_key
from tonsdk.contract.wallet import WalletV3ContractR2


def wallet_from_seed(client) -> tuple[WalletV3ContractR2, int]:
    """Import wallet from file SEED.txt
    returns WalletV3ContractR2 class and seqno"""

    with open("SEED.txt", "r") as f:
        mnemonics = f.read().split()

    keypair = mnemonic_to_wallet_key(mnemonics)

    wallet = WalletV3ContractR2(public_key=keypair[0], private_key=keypair[1])
    addr = wallet.address.to_string(True, True, True)

    seqno = client.seqno(addr)
    return wallet, seqno
