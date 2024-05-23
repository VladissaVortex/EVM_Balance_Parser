import asyncio
import json
import time
from typing import Any, Dict, List, Tuple
from fetch_balances import AsyncBalanceFetcher

NODE_URL = """https://rpc.ankr.com/eth"""
"""str:
    Node address of the selected network. It is recommended to use paid nodes for resource-intensive tasks and to 
    minimize the delay parameter.
"""

DELAY = 0.3  # in seconds
"""float:
    Delay between asynchronous wallet parsing tasks. It is recommended to set it to about 2-3 seconds if you are 
    using a free node with low request limits.
"""

ERC20_ABI = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]'
"""str:
    This is the ABI (set of instructions) for interacting with ERC20 token contracts. It includes all the necessary 
    methods that may be needed for this project. You won't need anything more, but if you want to modify the project, 
    you are free to do so.
"""


async def main() -> Tuple[List[Dict[str, Any]], float]:
    """
    Main function to fetch balances and measure execution time.

    Returns
    -------
    tuple
        A tuple containing the list of balance results and the elapsed time.
    """

    wallet_addresses = [
        '0xd443b9E4002f8Ec25bd9cc47236cEEA5A85c5B47',
        '0x68B531349EB44496943Be5FF15A5F510849D561f',
        '0xcdf65F2BF0D8D7B51d85c0F0a1115fB72dccF851'
    ]
    """list: Wallet addresses for which you want to obtain balances."""

    token_addresses = [
        '0x6982508145454Ce325dDbE47a25d4ec3d2311933',
        '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
    ]
    """list:
        Addresses of token smart contracts for which you want to obtain balances for the selected wallets. 
        (The balance of the native token of this network is obtained by default; it is not an ERC20 token, and you 
        do not need to provide its address in this list.)
    """

    fetcher = AsyncBalanceFetcher(NODE_URL, DELAY, ERC20_ABI)

    start_time = time.time()
    balances = await fetcher.fetch_all_balances(wallet_addresses, token_addresses)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(json.dumps(balances, indent=2))
    print(f"Execution time: {elapsed_time:.2f} seconds")

    return balances, elapsed_time


if __name__ == '__main__':
    asyncio.run(main())
