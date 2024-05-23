import aiohttp
import requests
from web3.exceptions import (
    BadFunctionCallOutput,
    BlockNumberOutofRange,
    ProviderConnectionError,
    CannotHandleRequest,
    TooManyRequests,
    MultipleFailedRequests,
    InvalidAddress,
    NameNotFound,
    StaleBlockchain,
    MismatchedABI,
    ABIEventFunctionNotFound,
    ABIFunctionNotFound,
    FallbackNotFound,
    Web3ValidationError,
    ExtraDataLengthError,
    NoABIFunctionsFound,
    NoABIFound,
    NoABIEventsFound,
    InsufficientData,
    TimeExhausted,
    TransactionNotFound,
    BlockNotFound,
    LogTopicError,
    InvalidEventABI,
    ContractLogicError,
    InvalidTransaction,
    TransactionTypeMismatch,
    BadResponseFormat,
    MethodUnavailable,
)


class ErrorHandler:
    """
    ErrorHandler class to classify and get messages for errors occurring in web3.py and aiohttp.

    Methods
    -------
    classify_error(error):
        Classifies the error based on its type.

    get_error_message(error):
        Gets a descriptive error message based on the error type.
    """

    @staticmethod
    def classify_error(error: Exception) -> str:
        """
        Classifies the error based on its type.

        Parameters
        ----------
        error : Exception
            The error to classify.

        Returns
        -------
        str
            The classification of the error.
        """
        # Network-related errors
        if isinstance(error, (ProviderConnectionError, aiohttp.ClientConnectionError, aiohttp.ClientResponseError,
                              aiohttp.ClientPayloadError, aiohttp.ClientOSError, aiohttp.InvalidURL,
                              requests.exceptions.ConnectionError, requests.exceptions.Timeout)):
            return "connection_to_node"

        # Address-related errors
        elif isinstance(error, InvalidAddress):
            return "invalid_address"
        elif isinstance(error, ValueError) and "when sending a str, it must be a hex string" in str(error):
            return "invalid_address_format"
        elif isinstance(error, ValueError) and "Unknown format" in str(error):
            return "invalid_address_format"

        # Validation errors
        elif isinstance(error, Web3ValidationError):
            return "validation"

        # ABI-related errors (with specific checks for ValueError)
        elif isinstance(error, BadFunctionCallOutput):
            return "bad_function_call_output"
        elif isinstance(error, InvalidEventABI):
            return "invalid_event_abi"
        elif isinstance(error, ABIFunctionNotFound):
            return "abi_function_not_found"
        elif isinstance(error, ABIEventFunctionNotFound):
            return "abi_event_function_not_found"
        elif isinstance(error, MismatchedABI):
            return "mismatched_abi"
        elif isinstance(error, ValueError) and "Could not format invalid value" in str(error):
            return "abi_error"
        elif isinstance(error, FallbackNotFound):
            return "fallback_not_found"
        elif isinstance(error, LogTopicError):
            return "log_topic_error"

        # Blockchain data-related errors
        elif isinstance(error, BlockNumberOutofRange):
            return "block_number_out_of_range"
        elif isinstance(error, BlockNotFound):
            return "block_not_found"
        elif isinstance(error, TransactionNotFound):
            return "transaction_not_found"
        elif isinstance(error, NameNotFound):
            return "name_not_found"
        elif isinstance(error, StaleBlockchain):
            return "stale_blockchain"

        # Request handling errors
        elif isinstance(error, CannotHandleRequest):
            return "cannot_handle_request"
        elif isinstance(error, TooManyRequests):
            return "too_many_requests"
        elif isinstance(error, MultipleFailedRequests):
            return "multiple_failed_requests"
        elif isinstance(error, MethodUnavailable):
            return "method_unavailable"

        # Contract execution errors
        elif isinstance(error, ContractLogicError):
            return "contract_logic_error"
        elif isinstance(error, TimeExhausted):
            return "time_exhausted"

        # Data format errors
        elif isinstance(error, ExtraDataLengthError):
            return "extra_data_length_error"
        elif isinstance(error, NoABIFunctionsFound):
            return "no_abi_functions_found"
        elif isinstance(error, NoABIFound):
            return "no_abi_found"
        elif isinstance(error, NoABIEventsFound):
            return "no_abi_events_found"
        elif isinstance(error, InsufficientData):
            return "insufficient_data"

        # Transaction-related errors
        elif isinstance(error, InvalidTransaction):
            return "invalid_transaction"
        elif isinstance(error, TransactionTypeMismatch):
            return "transaction_type_mismatch"

        # Response format errors
        elif isinstance(error, BadResponseFormat):
            return "bad_response_format"

        # Unicode errors
        elif isinstance(error, UnicodeError):
            return "connection_to_node"

        else:
            return "unknown"

    @staticmethod
    def get_error_message(error: Exception) -> str:
        """
        Gets a descriptive error message based on the error type.

        Parameters
        ----------
        error : Exception
            The error to get the message for.

        Returns
        -------
        str
            The descriptive error message.
        """
        error_message = str(error) if str(error) else "*no detailed info is provided*"
        return f"{type(error).__name__}: {error_message}"
