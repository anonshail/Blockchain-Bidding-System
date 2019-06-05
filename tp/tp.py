
import traceback
import sys
import hashlib
import logging

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.core import TransactionProcessor
DEFAULT_URL = 'tcp://validator:4004'
list=[]
def hash(data):
    return hashlib.sha512(data.encode()).hexdigest()
#logging.basicConfig('tp.log')
LOGGER = logging.getLogger(__name__)
family = "bidding"

FAMILY_NAME = hash("bidding")[:6]
BIDDING_ENTRY_TABLE = hash("Bidding entries")[:6]
BIDS_TABLE = hash("bidders")

ITEMS_TABLE = hash("items")

BIDS_TABLE=FAMILY_NAME+BIDDING_ENTRY_TABLE+BIDS_TABLE[:58]

ITEMS_TABLE = FAMILY_NAME + BIDDING_ENTRY_TABLE + ITEMS_TABLE[:58]

def getItemAddress(itemName):
    return FAMILY_NAME + BIDDING_ENTRY_TABLE + hash(itemName)[:58]
class BiddingTransactionHandler(TransactionHandler):
    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return family

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        header = transaction.header
        payload_list = transaction.payload.decode().split(",")
        try:
            action = payload_list[0]
            data = payload_list[1]
        except:
            data = ''

        # Get the signer's public key, sent in the header from the client.
        from_key = data

        # Perform the action.
        LOGGER.info("Action = %s.", action)
        LOGGER.info("Name\ = %s.", data)
        
        if action == "addItem":
            self._add(context, data)
        elif action=="addBid":
            self._addbid(context,data)
        elif action == "count":
            self._count(context)
        elif action=="showItem":
            self._show(context)
        elif action=="showBid":
            self._showbids(context)
        
        elif action == "clear":
            self._empty_cookie_jar(context, partyName, from_key)
        else:
            LOGGER.info("Please check the keyword !")


    @classmethod
    def _show(cls, context):
        LOGGER.debug("entering show")
        state_entries = context.get_state([ITEMS_TABLE])
        
        for i in list:
            print (i)
            LOGGER.debug("items")
           
        LOGGER.debug("exiting show")

    @classmethod
    def _showbids(cls, context):
        LOGGER.debug("entering show")
        state_entries = context.get_state([BIDS_TABLE])
        
        for i in list:
            print (i)
            LOGGER.debug("items")
           
        LOGGER.debug("exiting show")

    @classmethod
    def _add(cls, context, itemName):
        LOGGER.debug("entering add")
        state_entries = context.get_state([ITEMS_TABLE])
        if state_entries:
                items = state_entries[0].data
                items = items.decode().split(',')
                if itemName not in items:
                        print (items)
                        items.append(itemName)
                        list.append(itemName)
                else:
	                print("Already present")
        else:
             items = [itemName]
        p = ','.join(items).encode()   
        addresses = context.set_state({ITEMS_TABLE: p})
        print (items)
        LOGGER.debug("exiting add")


    @classmethod
    def _addbid(cls, context, bidName):
        LOGGER.debug("entering add")
        state_entries = context.get_state([BIDS_TABLE])
        if state_entries:
                bids = state_entries[0].data
                bids = bids.decode().split(',')
                if bidName not in bids:
                        print (bids)
                        bids.append(bidName)
                        list.append(bidName)
                else:
	                print("Already present")
        else:
             bids = [bidName]
        p = ','.join(bids).encode()   
        addresses = context.set_state({BIDS_TABLE: p})
        print (bids)
        LOGGER.debug("exiting add")

    @classmethod
    def _count(cls, context):
        LOGGER.debug("entering count")
        state_entries = context.get_state([ITEMS_TABLE])
        items = state_entries[0].data
        LOGGER.debug(items)
        
        LOGGER.debug("exiting count")


def main():
   
    print ("----------\n----------\n")
    try:
        # Setup logging for this class.
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)

        # Register the Transaction Handler and start it.
        processor = TransactionProcessor(url=DEFAULT_URL)
        sw_namespace = FAMILY_NAME
        handler = BiddingTransactionHandler(sw_namespace)
        processor.add_handler(handler)
        processor.start()
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
