# connect to websocket
# load data to dictionary
# logic to sort data
# structure the orderbook data


import asyncio
import websockets
import json

async def connect():
    uri = "wss://api.bebop.xyz/pmm/ethereum/v3/pricing?name=bebop-fan199&authorization=8f6f651e-195b-4900-958b-f3147fadca34"

    weth = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    usdc = "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

    pair = weth/usdc

    async with websockets.connect(uri, max_size=None) as websocket:

        while True:  # keep listening
            response = await websocket.recv()
            
            data = json.loads(response)

            bids = data.get('bids')
            asks = data.get('asks')

        
            print(data)

if __name__ == "__main__":
    asyncio.run(connect())