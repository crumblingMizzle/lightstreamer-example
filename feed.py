#!/usr/bin/env python3.10
import threading
import time
import random

from lightstreamer_adapter.server import DataProviderServer
from lightstreamer_adapter.interfaces.data import DataProvider


ITEM_NAME = "example"
SERVER_HOST = "localhost"
REQREP_PORT = 8001
NOTIFY_PORT = 8002


class ExampleDataAdapter(DataProvider):
    """This Remote Data Adapter example class shows an example implementation of a LightStream Data Provider in Python."""

    def __init__(self):
        self.thread = None
        self.executing = threading.Event()

        self.listener = None
    
    def initialize(self, params, config_file=None):
        """Invoked to provide initialization information to the Data Adapter."""
        pass

    def issnapshot_available(self, item_name):
        """Returns True if Snapshot information will be sent for the item_name item before the updates."""
        return False

    def set_listener(self, event_listener):
        """Caches the reference to the provided ItemEventListener instance."""
        self.listener = event_listener

    def subscribe(self, item_name):
        """Invoked to request data for the item_name item."""
        if item_name == ITEM_NAME:
            self.thread = threading.Thread(target=self.generate_data, name="Data Generator")
            self.thread.start()
        else:
            raise SubscribeError("No such item")

    def unsubscribe(self, item_name):
        """Invoked to end a previous request of data for an item."""
        if item_name == ITEM_NAME:
            self.executing.clear()
            self.thread.join()
    
    def generate_data(self):
        """Target method of the 'Data Generator' thread"""
        count = 0
        while not self.executing.is_set():
            data = {"message": f"example data: {count}", "timestamp": time.strftime("%a, %d %b %Y %H:%M:%S")}
            self.listener.update(ITEM_NAME, data, False)

            count += 1
            time.sleep(random.uniform(1, 2))

if __name__ == "__main__":
    # The adress of the Lightstreamer server, to be changed as required.
    address = (SERVER_HOST, REQREP_PORT, NOTIFY_PORT)

    # Creates a new DataProviderServer instance, passing a new ExampleDataAdpater
    # object and the remote address
    dataprovider_sever = DataProviderServer(ExampleDataAdapter(), address)
    # Starts the server instance.
    dataprovider_sever.start()

    while True:
        pass