import os	#for system
import hashlib

def hash(name,n=0):
	if(n==0):
		return hashlib.sha512(name.encode()).hexdigest()
	else:

		return hashlib.sha512(name.encode()).hexdigest()[:n]

def main():
    while 1:
        print("1. Add item")
        print("2. View items")
        print("3. Place a bid")
        print("4. View bids")
        print("Press anything else to exit")

        ch = input()
        if ch=='1':
            #add item
            print("Enter item name, description and duration in hours")
            item_name = input()
            desc = input()
            duration = input()
            item_id = hash(item_name, 5)
            fs = item_id+'@'+item_name+'@'+desc+'@'+duration
            os.system("python3 client.py addItem "+fs)
            
        elif ch=='2':
            #view items
            items = os.popen("python3 client.py showItem").read()
            print(items)

        elif ch=='3':
            #place a bid
            print("Enter bidder name, Item ID and Amount")
            bn = input()
            bid = hash(bn, 5)
            item_id = input()
            amount = input()
            fs = bn+"@"+bid+"@"+item_id+"@"+amount
            os.system("python3 client.py addBid "+fs)

        elif ch=='4':
            #view bids
            bids = os.popen("python3 client.py showBid").read()
            print(bids)

        else:
            break

main()
