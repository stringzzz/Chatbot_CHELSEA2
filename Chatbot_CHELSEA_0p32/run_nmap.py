import asyncio
import sys
from NET_DANCER import Net_Dancer

async def main():

	file_path = sys.argv[1]

	net_dancer = Net_Dancer(file_path)
	await net_dancer.observe_network()

if __name__ == "__main__":
	asyncio.run(main())