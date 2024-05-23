from error_handling import ErrorHandler
from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from typing import Tuple, Union


class BalanceReader:
    """
    A class to read balances from Ethereum addresses using web3.py.

    Attributes
    ----------
    web3 : Web3
        The Web3 instance connected to an Ethereum node.

    Methods
    -------
    get_custom_token_balance(token_address, token_abi, wallet_address):
        Gets the balance of a custom token for a given wallet address.

    get_native_token_balance(wallet_address):
        Gets the balance of the native token (ETH) for a given wallet address.
    """

    def __init__(self, node_url: str) -> None:
        """
        Initializes the BalanceReader with a node URL.

        Parameters
        ----------
        node_url : str
            The URL of the Ethereum node to connect to.
        """
        self.web3 = Web3(AsyncHTTPProvider(node_url))
        self.web3.eth = AsyncEth(self.web3)

    async def get_custom_token_balance(self, token_address: str, token_abi: str, wallet_address: str) -> Tuple[
        Union[float, None], Union[str, None], Union[str, None], Union[str, None]]:
        """
        Gets the balance of a custom token for a given wallet address.

        Parameters
        ----------
        token_address : str
            The address of the custom token contract.
        token_abi : str
            The ABI of the custom token contract.
        wallet_address : str
            The wallet address to check the balance for.

        Returns
        -------
        tuple
            A tuple containing the balance, token symbol, error type, and error message.
        """
        try:
            checksum_wallet_address = self.web3.to_checksum_address(wallet_address)
            checksum_token_address = self.web3.to_checksum_address(token_address)

            token_contract = self.web3.eth.contract(address=checksum_token_address, abi=token_abi)

            balance_of_token = await token_contract.functions.balanceOf(checksum_wallet_address).call()
            token_decimals = await token_contract.functions.decimals().call()
            ether_balance = balance_of_token / 10 ** token_decimals
            token_symbol = await token_contract.functions.symbol().call()

            return ether_balance, token_symbol, None, None

        except Exception as e:
            error_type = ErrorHandler.classify_error(e)
            error_message = ErrorHandler.get_error_message(e)
            return None, None, error_type, error_message

    async def get_native_token_balance(self, wallet_address: str) -> Tuple[
        Union[float, None], Union[str, None], Union[str, None]]:
        """
        Gets the balance of the native token (ETH) for a given wallet address.

        Parameters
        ----------
        wallet_address : str
            The wallet address to check the balance for.

        Returns
        -------
        tuple
            A tuple containing the balance, error type, and error message.
        """
        try:
            checksum_wallet_address = self.web3.to_checksum_address(wallet_address)
            balance = await self.web3.eth.get_balance(checksum_wallet_address)
            return balance / 10 ** 18, None, None

        except Exception as e:
            error_type = ErrorHandler.classify_error(e)
            error_message = ErrorHandler.get_error_message(e)
            return None, error_type, error_message
