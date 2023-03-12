from abc import ABC, abstractmethod
import asyncio

import aiohttp
from tvm_valuetypes import serialize_tvm_stack

from tonsdk.provider import ToncenterClient, prepare_address, address_state
from tonsdk.utils import TonCurrencyEnum, from_nano
from tonsdk.boc import Cell


API_URL = "https://testnet.toncenter.com/api/v2/"
# change to your own API key
API_KEY = "c16c15f5af5766864798ce17500423c70be039770a34fd4efb74cecafd3d897e"


class AbstractTonClient(ABC):
    provider: ToncenterClient

    @abstractmethod
    def _run(self, to_run, *, single_query=True):
        raise NotImplementedError

    def get_address_information(
            self, address: str,
            currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton):
        return self.get_addresses_information([address], currency_to_show)[0]

    def get_addresses_information(
            self, addresses,
            currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton):
        if not addresses:
            return []

        tasks = []
        for address in addresses:
            address = prepare_address(address)
            tasks.append(self.provider.raw_get_account_state(address))

        results = self._run(tasks, single_query=False)

        for result in results:
            result["state"] = address_state(result)
            if "balance" in result:
                if int(result["balance"]) < 0:
                    result["balance"] = 0
                else:
                    result["balance"] = from_nano(
                        int(result["balance"]), currency_to_show)

        return results

    def seqno(self, addr: str):
        addr = prepare_address(addr)
        result = self._run(self.provider.raw_run_method(addr, "seqno", []))

        if '@type' in result and result['@type'] == 'smc.runResult':
            result['stack'] = serialize_tvm_stack(result['stack'])

        return int(result[0]['stack'][0][1], 16)

    def send_boc(self, boc: Cell):
        return self._run(self.provider.raw_send_message(boc))


class TonCenterTonClient(AbstractTonClient):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.provider = ToncenterClient(base_url=API_URL,
                                        api_key=API_KEY)

    def _run(self, to_run, *, single_query=True):
        return self.loop.run_until_complete(
            self.__execute(to_run, single_query))

    async def __execute(self, to_run, single_query):
        timeout = aiohttp.ClientTimeout(total=5)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            if single_query:
                to_run = [to_run]

            tasks = []
            for task in to_run:
                tasks.append(task["func"](
                                session, *task["args"], **task["kwargs"]))

            return await asyncio.gather(*tasks)

    async def call(self, contract_address: str,
                   method: str, stack: list) -> dict:
        """
        Run contract's get method.

        Returns stack dictionary like:

        {'@extra': '1678643876',
         '@type': 'smc.runResult',
         'exit_code': 0,
         'gas_used': 3918,
         'stack': [['cell',
                    {'bytes': 'te6cckEBAQA...2C8Hn',
                     'object': {'data': {'b64': 'gAs4wlP...dUdIA==',
                                         'len': 267},
                                'refs': []}}]]}

        See examples/get_methods.py for more details.
        """
        query = self.provider.raw_run_method(contract_address, method, stack)

        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            r = await query["func"](session, *query["args"], **query["kwargs"])
            return r
