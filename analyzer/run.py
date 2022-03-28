import logging
import argparse

from analyzer.notifier import *
from analyzer.sniffer import *
from analyzer.visualizer import *
from analyzer.ansi import *
from analyzer.persistence import data_import, data_export

logging.basicConfig(format=f"{magenta('%(asctime)s')} %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='Traffic analyzer.')
parser.add_argument('--interface', help='interface to listen on.')
parser.add_argument('--ip', help='host to capture traffic from/to.')
parser.add_argument('--ports', help='ports to capture traffic on.', nargs='?', const=1, default='80,443')
parser.add_argument('--address', help='location of shared directory.', nargs='?', const=1, default='./bus/analyzer.bus')
parser.add_argument('--dump', help='location of shared directory.')

args = parser.parse_args()
args.ports = args.ports.split(',')


async def main(args):
    loop = asyncio.get_event_loop()
    notifier = Notifier(args.address)
    sniffer = Sniffer(args.interface, args.ip, args.ports)

    def update(notification):
        if notification['exit']:
            packets, loads = sniffer.reset()
            capture = sniffer.filter

            if args.dump is not None:
                data_export(packets, loads, args.dump)

            plot_all(loads, packets, capture)
        else:
            sniffer.update_label(notification['label'])

    notifier.listen(update)
    loop.create_task(notifier.start())

    await sniffer.start()
    await sniffer.stats()


try:
    asyncio.run(main(args))
except KeyboardInterrupt:
    logger.info("shutting down.")
