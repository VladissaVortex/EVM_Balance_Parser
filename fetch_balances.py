import asyncio
from typing import Any, Dict, List
from error_handling import ErrorHandler
from read_balances import BalanceReader


class AsyncBalanceFetcher:
    """
    A class to asynchronously fetch balances for multiple wallets and tokens.

    Attributes
    ----------
    reader : BalanceReader
        The BalanceReader instance to read balances from.
    delay : float
        The delay between balance fetches to avoid node throttling.
    token_abi : str
        The ABI of the custom token contracts.

    Methods
    -------
    fetch_balances_for_wallet(wallet_address, token_addresses):
        Fetches balances for a single wallet address.

    fetch_all_balances(wallet_addresses, token_addresses):
        Fetches balances for multiple wallet addresses.
    """

    def __init__(self, node_url: str, delay: float, token_abi: str) -> None:
        """
        Initializes the AsyncBalanceFetcher with a node URL, delay, and token ABI.

        Parameters
        ----------
        node_url : str
            The URL of the Ethereum node to connect to.
        delay : float
            The delay between balance fetches to avoid node throttling.
        token_abi : str
            The ABI of the custom token contracts.
        """
        self.reader = BalanceReader(node_url)
        self.delay = delay
        self.token_abi = token_abi

    async def fetch_balances_for_wallet(self, wallet_address: str, token_addresses: List[str]) -> Dict[str, Any]:
        """
        Fetches balances for a single wallet address.

        Parameters
        ----------
        wallet_address : str
            The wallet address to fetch balances for.
        token_addresses : list of str
            The list of custom token addresses to check balances for.

        Returns
        -------
        dict
            A dictionary containing the wallet address, native balance, token balances, and errors if any.
        """
        try:
            native_balance = await self.reader.get_native_token_balance(wallet_address)
            if isinstance(native_balance, tuple):
                native_balance, native_error_type, native_error_message = native_balance
            else:
                native_error_type = None
                native_error_message = None

            if native_balance is not None:
                token_balances = {}
                errors = {}
                for token_address in token_addresses:
                    balance_result = await self.reader.get_custom_token_balance(token_address, self.token_abi,
                                                                                wallet_address)
                    if isinstance(balance_result, tuple) and len(balance_result) == 4:
                        balance, symbol, error_type, error_message = balance_result
                        if balance is not None and symbol is not None:
                            token_balances[symbol] = balance
                        else:
                            errors[token_address] = {"error_type": error_type, "message": error_message}
                    else:
                        balance, symbol = balance_result
                        token_balances[symbol] = balance

                if errors:
                    return {
                        'wallet_address': wallet_address,
                        'native_balance': native_balance,
                        'token_balances': token_balances,
                        'errors': errors
                    }
                else:
                    return {
                        'wallet_address': wallet_address,
                        'native_balance': native_balance,
                        'token_balances': token_balances
                    }
            else:
                return {
                    'wallet_address': wallet_address,
                    'error': {
                        'type': native_error_type,
                        'message': native_error_message
                    }
                }

        except Exception as e:
            error_type = ErrorHandler.classify_error(e)
            error_message = ErrorHandler.get_error_message(e)
            return {
                'wallet_address': wallet_address,
                'error': {
                    'type': error_type,
                    'message': error_message
                }
            }

    async def fetch_all_balances(self, wallet_addresses: List[str], token_addresses: List[str]) -> List[Dict[str, Any]]:
        """
        Fetches balances for multiple wallet addresses.

        Parameters
        ----------
        wallet_addresses : list of str
            The list of wallet addresses to fetch balances for.
        token_addresses : list of str
            The list of custom token addresses to check balances for.

        Returns
        -------
        list of dict
            A list of dictionaries containing balances and errors for each wallet address.
        """
        tasks = []
        total_wallets = len(wallet_addresses)
        for idx, wallet_address in enumerate(wallet_addresses):
            tasks.append(self.fetch_balances_for_wallet(wallet_address, token_addresses))
            await asyncio.sleep(self.delay)
            print(f"Received wallet balances: {idx + 1}/{total_wallets}")

        results = await asyncio.gather(*tasks, return_exceptions=True)
        final_results = []
        for result in results:
            if isinstance(result, Exception):
                error_type = ErrorHandler.classify_error(result)
                error_message = ErrorHandler.get_error_message(result)
                final_results.append({
                    'error': {
                        'type': error_type,
                        'message': error_message
                    }
                })
            else:
                final_results.append(result)
        return final_results
