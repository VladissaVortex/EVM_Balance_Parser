
# Async Balance Fetcher

This repository contains a Python project for asynchronously fetching balances for multiple Ethereum wallet addresses and tokens using web3.py and aiohttp.

## Project Structure

- **ErrorHandler**: Class to classify and get messages for errors occurring in web3.py and aiohttp.
- **BalanceReader**: Class to read balances from Ethereum addresses using web3.py.
- **AsyncBalanceFetcher**: Class to asynchronously fetch balances for multiple wallets and tokens.
- **main**: Main function to fetch balances and measure execution time.

## Returned Values

### Successful Response

When the request is successful, the returned value is a list of dictionaries. Each dictionary contains the wallet address, the native token balance (ETH), and the balances of the specified custom tokens.

Example:
```json
[
  {
    "wallet_address": "0x68B531349EB44496943Be5FF15A5F510849D561f",
    "native_balance": 6.694098185682657,
    "token_balances": {
      "PEPE": 519052.07922536106,
      "WETH": 0.0,
      "USDC": 0.0
    }
  },
  {
    "wallet_address": "0xcdf65F2BF0D8D7B51d85c0F0a1115fB72dccF851",
    "native_balance": 0.003642641761430284,
    "token_balances": {
      "PEPE": 557183140.9854761,
      "WETH": 0.0,
      "USDC": 0.857963
    }
  }
]
```

### General Error Response

If a general error occurs during the fetching process, the returned value is a dictionary with an `error` key containing the type and message of the error.

Example:
```json
[
  {
    "error": {
      "type": "connection_to_node",
      "message": "UnicodeError: encoding with 'idna' codec failed (UnicodeError: label empty or too long)"
    }
  }
]
```

### Error in Fetching Native Token Balance

If there is an error while fetching the native token balance (ETH) for a specific wallet, the returned value contains the wallet address and an `error` key with the type and message of the error.

Example:
```json
[
  {
    "wallet_address": "0xd443b9E4002f8Ec25bd9cc47236cEEA5A85c5B47",
    "error": {
      "type": "invalid_address_format",
      "message": "ValueError: Unknown format '0xd443b9E4002f8Ec25bd9cc47236cEEA5A85c5B47', attempted to normalize to '0xd443b9e4002f8ec25bd9cc47236ceea5a85c5b47'"
    }
  }
]
```

### Error in Fetching Custom Token Balances

If there is an error while fetching the balance of a custom token for a specific wallet, the returned value contains the wallet address, the native balance, and an `errors` key with details about the failed token balance fetches.

Example:
```json
[
  {
    "wallet_address": "0x68B531349EB44496943Be5FF15A5F510849D561f",
    "native_balance": 6.694098185682657,
    "token_balances": {
      "PEPE": 519052.07922536106
    },
    "errors": {
      "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": {
        "error_type": "abi_error",
        "message": "ValueError: Could not format invalid value '[...]' as field 'abi'"
      }
    }
  }
]
```

## Usage

### Local Setup

1. Clone the repository.
2. Install the required packages.
3. Modify the `node_url`, `delay`, `token_abi`, `wallet_addresses`, and `token_addresses` in the `main` function as needed.
4. Run the script.

```bash
python main.py
```

### Docker Setup

1. Clone the repository.
2. Build the Docker image:

```bash
docker build -t async-balance-fetcher .
```

3. Run the Docker container:

```bash
docker run -it --rm --name async_balance_fetcher async-balance-fetcher
```

Alternatively, you can use Docker Compose:

1. Build and run the Docker container:

```bash
docker-compose up --build
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
