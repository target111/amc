import logging, argparse

from lib.service import Service
from lib.constants import Config
from lib.utils import read_file, chunkify
from threading import Thread

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


class AMC(Thread):
    def __init__(self, combo):
        Thread.__init__(self)

        self.combo = combo
        self.s = Service(Config.URL, Config.HEADERS)

    def run(self):
        for user in self.combo:
            self.s.first_request()
            self.s.second_request(user, self.combo[user])

            self.s.reset_session()


def parse_args():
    parser = argparse.ArgumentParser(
        description="""AMC somthing""",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('input',
                        help="Combolist input file.",
                        type=argparse.FileType('r'),
                        default='-')
    parser.add_argument('-t',
                        '--threads',
                        help="Number of threads to use (default: 1)",
                        type=int,
                        default=1)

    args = parser.parse_args()
    return args


def run(args=None):
    logging.info("Starting AMC application with %s threads." %
                 str(args.threads))

    for combo in chunkify(read_file(args.input), args.threads):
        AMC(combo).start()


def main():
    run(parse_args())


if __name__ == "__main__":
    main()
