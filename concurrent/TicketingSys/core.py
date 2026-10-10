# Based on RealPython Threading Example page at https://realpython.com/intro-to-python-threading/
import logging
import random
import time
import argparse
import pydash as _


def thread_function(index, evnt):
    logging.info("Thread %d: starting", index)
    time.sleep(1)
    evnt.set()
    logging.info("Thread %d: finishing", index)


def critical_section_acquire_release(name, sync_object):
    # Add random amount of time for sleep so that execution may be random
    time.sleep(random.randint(0, 10))
    sync_object.acquire()
    logging.debug("critical_section_acquire_release thread: %d acquired synchronization object.", name)
    thread_function(name)
    sync_object.release()
    logging.debug("critical_section_acquire_release thread: %d released synchronization object.", name)


class Core:

    file_username = None
    username_arg = None
    num_threads = 1
    part_id = ''

    def __init__(self, args_list=None, args=None):
        self.parser = argparse.ArgumentParser(description='Process command-line arguments')
        for arg in args_list:
            self.add_arg_parser_argument(arg)
        self.read_user_file()
        self.parse_args(args)
        output_file_name = "output-" + self.part_id + ".txt"
        open(output_file_name, 'w').close()

        _format = "%(asctime)s: %(message)s"
        _date_format = "%H:%M:%S"

        # 1. Create a main logger and set it to the lowest level you want to capture
        self.logger = logging.getLogger("tktsys")
        self.logger.setLevel(logging.DEBUG)  # Allows all logs to pass into the self.logger first
        self.logger.propagate = False # Prevents logs from duplicating into the root console output

         # 2. Console Handler (Captures everything DEBUG and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(fmt=_format, datefmt=_date_format)
        console_handler.setFormatter(console_formatter)

        # 3. File Handler (Captures other than DEBUG logs)
        file_handler = logging.FileHandler(output_file_name)
        file_handler.setLevel(logging.INFO)  # <--- This filters out DEBUG, INFO, and WARNING
        file_formatter = logging.Formatter(fmt=_format, datefmt=_date_format)
        file_handler.setFormatter(file_formatter)

        # 4. Add handlers to the self.logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)


    def read_user_file(self):
        file = open(".user", "r")
        self.file_username = file.readline()

    def test_username_equality(self, const_username):
        return self.file_username == self.username_arg and self.file_username == const_username

    def parse_args(self, args):
        namespace = self.parser.parse_args(args=args)
        if namespace:
            self.num_threads = int(_.get(namespace, 'num_threads', 1))
            self.username_arg = str(_.get(namespace, 'user', None))
            self.part_id = str(_.get(namespace, 'part_id', None))

    def add_arg_parser_argument(self, arg):
        self.parser.add_argument(arg[0], dest=arg[1], default=arg[2], help=arg[3])
