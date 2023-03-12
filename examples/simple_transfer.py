from tonsdk.utils import to_nano
from client import TonCenterTonClient
from import_wallet import wallet_from_seed

import sys


def main():
    if len(sys.argv) < 3:
        print('Usage: python simple_transfer.py <address> <amount> "<comment>"')
        return

    addr_str = sys.argv[1]
    comment = sys.argv[2]
    amount = to_nano(float(sys.argv[3]), "ton")

    client = TonCenterTonClient()

    wallet, seqno = wallet_from_seed(client)

    query = wallet.create_transfer_message(
            to_addr=addr_str,
            amount=amount,
            seqno=seqno,
            payload=comment,
        )

    print(client.send_boc(query['message'].to_boc(False)))


if __name__ == '__main__':
    main()
