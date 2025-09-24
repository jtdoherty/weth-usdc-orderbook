import asyncio
import websockets
import json

async def connect():
    # WebSocket URL with authentication and JSON format
    uri = "wss://api.bebop.xyz/pmm/ethereum/v3/pricing?name=bebop-fan199&authorization=8f6f651e-195b-4900-958b-f3147fadca34"
    # Define contract addresses for WETH and USDC
    weth = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    usdc = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

    # Format the pair key as per the API structure
    pair_key = f"{weth}/{usdc}"

    try:
        async with websockets.connect(uri, max_size=None) as websocket:
            print(f"Connected to WebSocket for WETH/USDC pair: {pair_key}")
            while True:
                try:
                    # Receive and parse WebSocket message
                    response = await websocket.recv()
                    data = json.loads(response)

                    # Check if the WETH/USDC pair exists in the data
                    if pair_key in data:
                        pair_data = data[pair_key]
                        bids = pair_data.get('bids', [])
                        asks = pair_data.get('asks', [])

                        # Extract top bid (highest price, first element) and top ask (lowest price, first element)
                        top_bid = bids[0] if bids else [None, None]
                        top_ask = asks[0] if asks else [None, None]

                        # Structure the orderbook output
                        orderbook = {
                            "pair": "WETH/USDC",
                            "last_update_ts": pair_data.get('last_update_ts', None),
                            "top_bid": {
                                "price": top_bid[0],
                                "quantity": top_bid[1]
                            } if top_bid[0] is not None else None,
                            "top_ask": {
                                "price": top_ask[0],
                                "quantity": top_ask[1]
                            } if top_ask[0] is not None else None
                        }

                        # Print structured orderbook
                        print("\nWETH/USDC Orderbook:")
                        print(f"Last Update: {orderbook['last_update_ts']}")
                        if orderbook['top_bid']:
                            print(f"Top Bid: {orderbook['top_bid']['price']} USDC/WETH, Quantity: {orderbook['top_bid']['quantity']} WETH")
                        else:
                            print("Top Bid: None (No bids available)")
                        if orderbook['top_ask']:
                            print(f"Top Ask: {orderbook['top_ask']['price']} USDC/WETH, Quantity: {orderbook['top_ask']['quantity']} WETH")
                        else:
                            print("Top Ask: None (No asks available)")
                    else:
                        print(f"Pair {pair_key} not found in data")

                except json.JSONDecodeError:
                    print("Error: Received invalid JSON data")
                except Exception as e:
                    print(f"Error processing data: {e}")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"WebSocket connection closed: {e}")
    except Exception as e:
        print(f"Error connecting to WebSocket: {e}")

if __name__ == "__main__":
    asyncio.run(connect())