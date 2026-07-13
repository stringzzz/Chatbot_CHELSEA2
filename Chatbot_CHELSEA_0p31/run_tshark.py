import asyncio
from NET_DANCER import Net_Dancer
import sys

async def main():

	file_path = sys.argv[1]
	source1 = sys.argv[2]
	source2 = sys.argv[3]
	duration_minutes = sys.argv[4]

	net_dancer = Net_Dancer(file_path)
	await net_dancer.listen_to_environment(source1, source2, str(duration_minutes))

	net_dancer.analyze_network_snapshot()

if __name__ == "__main__":
	asyncio.run(main())