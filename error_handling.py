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
        match error:
            case (ProviderConnectionError() | aiohttp.ClientConnectionError() |
                  aiohttp.ClientResponseError() | aiohttp.ClientPayloadError() |
                  aiohttp.ClientOSError() | aiohttp.InvalidURL() |
                  requests.exceptions.ConnectionError() | requests.exceptions.Timeout()):
                return "connection_to_node"

            case InvalidAddress():
                return "invalid_address"

            case ValueError() if "when sending a str, it must be a hex string" in str(error):
                return "invalid_address_format"

            case ValueError() if "Unknown format" in str(error):
                return "invalid_address_format"

            case Web3ValidationError():
                return "validation"

            case BadFunctionCallOutput():
                return "bad_function_call_output"

            case InvalidEventABI():
                return "invalid_event_abi"

            case ABIFunctionNotFound():
                return "abi_function_not_found"

            case ABIEventFunctionNotFound():
                return "abi_event_function_not_found"

            case MismatchedABI():
                return "mismatched_abi"

            case ValueError() if "Could not format invalid value" in str(error):
                return "abi_error"

            case FallbackNotFound():
                return "fallback_not_found"

            case LogTopicError():
                return "log_topic_error"

            case BlockNumberOutofRange():
                return "block_number_out_of_range"

            case BlockNotFound():
                return "block_not_found"

            case TransactionNotFound():
                return "transaction_not_found"

            case NameNotFound():
                return "name_not_found"

            case StaleBlockchain():
                return "stale_blockchain"

            case CannotHandleRequest():
                return "cannot_handle_request"

            case TooManyRequests():
                return "too_many_requests"

            case MultipleFailedRequests():
                return "multiple_failed_requests"

            case MethodUnavailable():
                return "method_unavailable"

            case ContractLogicError():
                return "contract_logic_error"

            case TimeExhausted():
                return "time_exhausted"

            case ExtraDataLengthError():
                return "extra_data_length_error"

            case NoABIFunctionsFound():
                return "no_abi_functions_found"

            case NoABIFound():
                return "no_abi_found"

            case NoABIEventsFound():
                return "no_abi_events_found"

            case InsufficientData():
                return "insufficient_data"

            case InvalidTransaction():
                return "invalid_transaction"

            case TransactionTypeMismatch():
                return "transaction_type_mismatch"

            case BadResponseFormat():
                return "bad_response_format"

            case UnicodeError():
                return "connection_to_node"

            case _:
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
