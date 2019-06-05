
from sys import *
import hashlib

import hashlib
import base64
import random
import time
import requests
import yaml
import datetime

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch

def hash(data):
    return hashlib.sha512(data.encode()).hexdigest()

#LOGGER = logging.getLogger(__name__)
family = "bidding"

FAMILY_NAME = hash("bidding")[:6]
BIDDING_ENTRY_TABLE = hash("Bidding entries")[:6]
BIDS_TABLE = hash("bidders")

ITEMS_TABLE = hash("items")

BIDS_TABLE=FAMILY_NAME+BIDDING_ENTRY_TABLE+BIDS_TABLE[:58]

ITEMS_TABLE = FAMILY_NAME + BIDDING_ENTRY_TABLE + ITEMS_TABLE[:58]


base_url="http://rest-api:8008"
import optparse
import argparse
FAMILY_NAME=hashlib.sha256("bidding".encode()).hexdigest()[:6]
parser=optparse.OptionParser()
parser.add_option('-U','--url',action="store",dest="url",default="spam")
namespace=""

context=create_context('secp256k1')

private_key=context.new_random_private_key()
signer=CryptoFactory(context).new_signer(private_key)

public_key=signer.get_public_key().as_hex()


def hash(name,n=0):
	if(n==0):
		return hashlib.sha512(name.encode()).hexdigest()
	else:

		return hashlib.sha512(name.encode()).hexdigest()[:n]


def showitems():
        result = send_to_rest_api("state/{}".format(ITEMS_TABLE))
        try:
            return (base64.b64decode(yaml.safe_load(result)["data"])).decode()
        except BaseException as e:
            print ("BaseExceprion: {}".format(e))
            return None
			

def showbids():
        result = send_to_rest_api("state/{}".format(BIDS_TABLE))
        try:
            return (base64.b64decode(yaml.safe_load(result)["data"])).decode()
        except BaseException:
            return None

def itemaddition(itemName):
        namespace=FAMILY_NAME+hash("Bidding entries",6)+hash(itemName,58)
        print("CURRENT TIME         ",str(datetime.datetime.now()))
        timestamp = str(datetime.datetime.now()+datetime.timedelta(hours=int(itemName.split('@')[-1])))
        print("EXPIRY TIME          ",timestamp)
        itemName = itemName+"@"+timestamp
        wrap_and_send("addItem",str(itemName))

'''def bidaddition(Name):
	namespace=FAMILY_NAME+hash("Bidding entries",6)+hash(Name,58)
	timestamp = str(datetime.datetime.now().time())
	#this is a comment
	Name = Name+"@"+timestamp
	k = showbids()
	k=k.split(',')
              
        #for item in k:
        #    bid = bid.split('@')
        #    if bid[2] == item[1]
        #         if bid[5][
           
        wrap_and_send("addBid",str(Name))'''

def bidaddition(Name):
        namespace = FAMILY_NAME+hash("Bidding entries",6)+hash(Name,58)
        timestamp1 = datetime.datetime.now()
        timestamp = str(timestamp1)
        list1=[]
        Name = Name + "@" + timestamp
        values = Name.split('@')
        k = showitems()
        k=k.split(',')
        #print ("k - ",k)
        for item in k:
             item=item.split('@')
             if item[0]==values[1]:
                 #print(item[-1] + " " + timestamp)
                 if item[-1]<timestamp:
                     print ("The bidding for this item has been closed.")
                     #function to print winning bidder keyword:keyword
                     bids = showbids()
                     bids = bids.split(',')
                     m = 0 
                     #print ("bids - ",bids)
                     for bid in bids:
                          bid = bid.split('@')
                          if bid[1]==item[0]:
                              if int(bid[3])>max:
                                   m=int(bid[3])
                                   bidder_id= bid[0]
                     print ("The bid id of the Winner is - "+bidder_id)
                     return
        bids = showbids()
        bids = bids.split(',')
        #print ("bids - ",bids)
        for bid in bids:
             bid = bid.split('@')
             if values[1]==bid[1]:
                 list1.append(bid)
                 #print('difference ',str((timestamp1-item[-1])))
                 if list1[-1][3]>values[3]:
                      print ("Your bid has been rejected coz a larger bid has already been placed.")
                      return 
        wrap_and_send("addBid",str(Name))


#def castVote(partyName):
#namespace=FAMILY_NAME+hash("Voting entries",6)+hash(partyName,58)
#pass

def send_to_rest_api(suffix, data=None, content_type=None):
        '''Send a REST command to the Validator via the REST API.
           Called by count() &  _wrap_and_send().
           The latter caller is made on the behalf of bake() & eat().
        '''
        url = "{}/{}".format(base_url, suffix)
        #print("URL to send to REST API is {}".format(url))

        headers = {}

        if content_type is not None:
            headers['Content-Type'] = content_type

        try:
            if data is not None:
                
                result = requests.post(url, headers=headers, data=data)
                #print(url)
            else:
                
                #print(url)
	
                result = requests.get(url, headers=headers)

            if not result.ok:
                raise Exception("Error {}: {}".format(
                    result.status_code, result.reason))
        except requests.ConnectionError as err:
            raise Exception(
                'Failed to connect to {}: {}'.format(url, str(err)))
        except BaseException as err:
            print(err)
            raise Exception(err)

        return result.text

def wait_for_status(batch_id, wait, result):
        '''Wait until transaction status is not PENDING (COMMITTED or error).
           'wait' is time to wait for status, in seconds.
        '''
        if wait and wait > 0:
            waited = 0
            start_time = time.time()
            while waited < wait:
                result = send_to_rest_api("batch_statuses?id={}&wait={}"
                                               .format(batch_id, wait))
                status = yaml.safe_load(result)['data'][0]['status']
                waited = time.time() - start_time

                if status != 'PENDING':
                    return result
            return "Transaction timed out after waiting {} seconds." \
               .format(wait)
        else:
            return result


def wrap_and_send(action, data='', wait=None):
        # Generate a CSV UTF-8 encoded string as the payload.
        raw_payload = ",".join([action,data])
        payload = raw_payload # Convert Unicode to bytes
        
        # Construct the address where we'll store our state.
        # We just have one input and output address (the same one).
        input_and_output_address_list = [namespace]

        # Create a TransactionHeader.
        header = TransactionHeader(
            signer_public_key=public_key,
            family_name="bidding",
            family_version="1.0",
            inputs=input_and_output_address_list,
            outputs=input_and_output_address_list,
            dependencies=[],
            payload_sha512=hash(payload),
            batcher_public_key=public_key,
            nonce=random.random().hex().encode()
        ).SerializeToString()

        # Create a Transaction from the header and payload above.
        transaction = Transaction(
            header=header,
            payload=payload.encode(),
            header_signature=signer.sign(header)
        )

        transaction_list = [transaction]

        # Create a BatchHeader from transaction_list above.
        header = BatchHeader(
            signer_public_key=public_key,
            transaction_ids=[txn.header_signature for txn in transaction_list]
        ).SerializeToString()

        # Create Batch using the BatchHeader and transaction_list above.
        batch = Batch(
            header=header,
            transactions=transaction_list,
            header_signature=signer.sign(header))

        # Create a Batch List from Batch above
        batch_list = BatchList(batches=[batch])
        batch_id = batch_list.batches[0].header_signature

        # Send batch_list to the REST API
        result = send_to_rest_api("batches",
                                       batch_list.SerializeToString(),
                                       'application/octet-stream')

        # Wait until transaction status is COMMITTED, error, or timed out
        return wait_for_status(batch_id, wait, result)

if __name__=='__main__':
        opts, args=parser.parse_args()
        
        #base_url=opts.url
        if(argv[1]=="addItem"):
                try:
                        itemaddition(argv[2])
                        print("Item name added is "+argv[2])
                        #base_url=argv[3]
                except Exception as e:
                        #print("Enter the item name")
                        print ("Exception",e)

        if(argv[1]=="addBid"):
                try:
                        bidaddition(argv[2])
                        print("Info of the placed bid is "+argv[2])
                        #base_url=argv[3]
                except Exception as e:
                        #print("Enter the bid name")
                        print ("Exception",e)

        if(argv[1]=="showItem"):
               try:
                   k=showitems()
                   k=k.split(',')

                   print("ItemID\tName\tDesc\tDuration\tTime Stamp")
                   for item in k:
                        item = item.split('@')
                        for i in item:
                              print(i,end='')
                        print('') 
               except:
                   print("e")

        if(argv[1]=="showBid"):
               try:

                   k=showbids()
                   k=k.split(',')
              
                   print("BidderID\tItemID\tBidID\tAmount\tTime Stamp")
                   for item in k:
                        item = item.split('@')
                        for i in item:
                            print(i,end='') 
                        print('')
               except Exception as e:
                   print('exception ',e)


