import urllib.parse
from tonsdk.utils import Address, to_nano
from tonsdk.contract.token.nft import NFTItem
from client import TonCenterTonClient
from import_wallet import wallet_from_seed

import sys


def serialize_uri(uri):
    return urllib.parse.quote(uri, safe='~@#$&()*!+=:;,?/\'').encode()


def main():
    if len(sys.argv) < 3:
        print("Usage: python nft_transfer.py <nft_addr> <to_addr>")
        return

    nft_addr_str = sys.argv[1]
    to_addr = Address(sys.argv[2])

    _nft = NFTItem()
    body = _nft.create_transfer_body(to_addr, to_addr)

    client = TonCenterTonClient()
    wallet, seqno = wallet_from_seed(client)

    query = wallet.create_transfer_message(
            to_addr=nft_addr_str,
            amount=to_nano(0.05, "ton"),
            seqno=seqno,
            payload=body,
        )

    print(client.send_boc(query['message'].to_boc(False)))


if __name__ == '__main__':
    main()
