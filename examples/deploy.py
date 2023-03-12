# Deploy new contract with wallet

from tonsdk.boc import Cell
from tonsdk.utils import to_nano
from tonsdk.contract import Contract

from client import TonCenterTonClient
from import_wallet import wallet_from_seed

import sys


class MyContract(Contract):
    def create_data_cell(self):
        return self.options['data']


def main():
    if len(sys.argv) < 3:
        print("Usage: python deploy.py <CODE_HEX> <DATA_HEX>")
        return

    code_cell = Cell.one_from_boc(sys.argv[1])
    data_cell = Cell.one_from_boc(sys.argv[2])

    my_contract = MyContract()
    my_contract.options['code'] = code_cell
    my_contract.options['data'] = data_cell

    result = my_contract.create_state_init()
    state_init = result['state_init']
    address = result['address']

    print(f"New Contract Address: {address.to_string(True, True, True)}")

    # You can store any body you want to be processed
    # by contract in the first message
    body = Cell()
    body.bits.write_uint(0xffff, 32)

    client = TonCenterTonClient()
    wallet, seqno = wallet_from_seed(client)

    query = wallet.create_transfer_message(
            to_addr=address,
            amount=to_nano(0.05, "ton"),
            seqno=seqno,
            state_init=state_init,
            payload=body,
        )

    print(client.send_boc(query['message'].to_boc(False)))


if __name__ == '__main__':
    main()
