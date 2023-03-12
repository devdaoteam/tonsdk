# Get methods callings example

import asyncio
from pprint import pprint
from base64 import b64decode

from tonsdk.provider import prepare_address, serialize_stack
from tonsdk.boc import Cell, Slice
from tonsdk.utils import Address

from client import TonCenterTonClient


async def get_nft_item_data(addr: str) -> dict:
    client = TonCenterTonClient()
    addr = prepare_address(addr)
    result = await client.call(addr, "get_nft_data", [])

    init = int(result['stack'][0][1], 16) == -1
    index = int(result['stack'][1][1], 16)

    hex_owner_addr_cell = b64decode(result['stack'][3][1]['bytes']).hex()
    hex_collection_addr_cell = b64decode(result['stack'][2][1]['bytes']).hex()
    hex_content_cell = b64decode(result['stack'][4][1]['bytes']).hex()

    owner_addr_cell = Cell.one_from_boc(hex_owner_addr_cell)
    collection_addr_cell = Cell.one_from_boc(hex_collection_addr_cell)
    content_cell = Cell.one_from_boc(hex_content_cell)

    owner_addr = Slice(owner_addr_cell).read_msg_addr()
    collection_addr = Slice(collection_addr_cell).read_msg_addr()

    # read_msg_addr may return None if address is null
    assert owner_addr and collection_addr

    individual_content_uri = Slice(content_cell).read_string()

    nft_data = {
        'init': init,
        'index': index,
        'owner': owner_addr.to_string(True, True, True),
        'collection': collection_addr.to_string(True, True, True),
        'content_uri': individual_content_uri,
        'content_cell': content_cell
    }

    return nft_data


async def get_nft_address_by_index(addr: str, index: int) -> str:
    client = TonCenterTonClient()
    addr = prepare_address(addr)
    stack = serialize_stack([index])
    result = await client.call(addr, "get_nft_address_by_index", stack)
    hex_nft_addr_cell = b64decode(result['stack'][0][1]['bytes']).hex()
    nft_addr_cell = Cell.one_from_boc(hex_nft_addr_cell)
    nft_addr = Slice(nft_addr_cell).read_msg_addr()
    assert nft_addr
    return nft_addr.to_string(True, True, True)


async def get_nft_content(collecion_addr: str,
                          individual_nft_content: Cell | str,
                          index: int | None = None) -> str:
    client = TonCenterTonClient()
    collecion_addr = prepare_address(collecion_addr)

    if type(individual_nft_content) == str:
        uri = individual_nft_content
        individual_nft_content = Cell()
        individual_nft_content.bits.write_string(uri)

    stack = serialize_stack([index or 0, individual_nft_content])
    result = await client.call(collecion_addr, "get_nft_content", stack)
    hex_content_uri_cell = b64decode(result['stack'][0][1]['bytes']).hex()
    content_cell = Cell.one_from_boc(hex_content_uri_cell)
    content_slice = Slice(content_cell)
    content_slice.read_uint(8)  # offchain tag
    base_content_uri = content_slice.read_string()
    individual_content_uri = Slice(content_slice.read_ref()).read_string()
    return base_content_uri + individual_content_uri


async def get_jetton_wallet_addr(master_addr: str, owner_addr: str) -> str:
    client = TonCenterTonClient()
    master_addr = prepare_address(master_addr)
    _owner_addr = Address(owner_addr)
    stack = serialize_stack([_owner_addr])
    result = await client.call(master_addr, "get_wallet_address", stack)
    hex_wallet_addr_cell = b64decode(result['stack'][0][1]['bytes']).hex()
    wallet_addr_cell = Cell.one_from_boc(hex_wallet_addr_cell)
    wallet_addr = Slice(wallet_addr_cell).read_msg_addr()
    assert wallet_addr
    return wallet_addr.to_string(True, True, True)


async def main():
    nft_addr = "EQD8OiqtBZOTwaIZ05WrWzZdmYGyzK8MjHiBcKURLQnr1qr1"

    nft_data = await get_nft_item_data(nft_addr)
    print("\nNFT Data: ", end="")
    pprint(nft_data)

    print("\n10000th NFT Address:", await get_nft_address_by_index(
        nft_data['collection'], 10000))

    print("\nNFT Item Content Uri:", await get_nft_content(
                                                nft_data['collection'],
                                                nft_data['content_cell']))

    jetton_master = "EQBpWQUDqeQ5hF0ps-GIOaQCeyrFVYbwFeYmPPyCavO8SdkO"
    owner_addr = "EQC4lxeD8zFIwAzeDdgimJisBDxPQG0qHx5BzwkAc9ocW-Mf"
    print("\nJetton Wallet Address:",
          await get_jetton_wallet_addr(jetton_master, owner_addr))


if __name__ == "__main__":
    asyncio.run(main())
