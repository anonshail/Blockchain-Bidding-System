## Problem Statement
To create a trustworthy bidding system and implement using blockchain technology where the user can either place an item for sale or they can bid on the existing items, and the result of the bid can be trusted by all and it cannot be tampered with.

The item information along with description is stored on the blockchain. All the valid bids are also stored on the blockchain, thus the result of the bid can always be trusted to be true.

## Abstract
The main aim of this project is to design and implement a secure online bidding system using blockchain technology. For this, we make use of the Hyperledger Sawtooth framework

The project aims to create a system in which a client can connect to the validator network can put an item or commodity of his choice up for auction. Other clients can view the various items put up for sale and can connect to the validator network to place a bid on any of these items. For each item, after a set time has elapsed, the highest bidder wins and purchases the item for the price of his bid. This system, therefore, provides an online platform with an easy to use user interface to enable users to sell and purchase various goods.

All the information regarding an item including the bids for each item and its related information will be stored on the blockchain. As a result, this information can be stored securely and is tamperproof. Therefore, a detailed record of all the bids for an item is maintained and cannot be altered after a sale is confirmed. This ensures that the highest bidder always wins and must make the purchase for the amount quoted in the bid. Furthermore, the information regarding the item is also maintained on the blockchain, the user who is putting the item up for sale cannot mislead the bidders about the item as the item must meet the description provided when it was put up for sale. This ensures that both the seller and the bidder must fulfil their ends of the purchase and the sale is amenable to both parties.

## Requirements
1. Docker
2. Docker Compose
3. Hyperledger Sawtooth

## Use Case
There are two main actors in the system – the seller and the bidder.

The seller can log onto the system, and place an item or commodity on sale. When he does this, the item information (description, price and so on) will be written on the blockchain. This information is viewable to all other users of the system.

The bidder can log onto the system, and view information about the various items posted. They can then proceed to make a bid on any of the item. The user information, along with the bid is then placed onto the blockchain. The user must bid for more value than the previous bid. Once the bidding period is over, the highest bidder wins, and the item is considered sold.
Since the bidding information is stored on the blockchain, the result of the bid can be trusted. Thus, only the highest bidder wins.

![Use Case Diagram](https://github.com/anonshail/Blockchain-Bidding-System/blob/master/resources/ucdiagram.png "")

## Role of client and types of transactions
A user can either post an item for sale, or make a bid on existing items. Therefore, there are four defined transactions that the client can perform:
1. Post an Item for Bidding – The client will post an item along with relevant information on the blockchain
2. View items – The list of items that can be bid on
3. Place bid – Making a bid on the listed items
4. View bids – View the existing bids on the items

## Tables stored in blockchain
There are two implemented tables:
1. Items table – This table consists of all available items for bidding, and all associated information
2. Bids table – This table contains the list of all bids made.

## Fields for Item
There are five fields for each item:
1. Item ID
2. Item Name
3. Item Description
4. Post time
5. Bidding Expiry Time

## Fields for Bid
There are five fields for each bid:
1. Bidder ID
2. Bidder Name
3. Item ID
4. Amount
5. Timestamp

![Schema Diagram](https://github.com/anonshail/Blockchain-Bidding-System/blob/master/resources/schema.png "")
