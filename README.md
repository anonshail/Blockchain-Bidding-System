# Blockchain-Bidding-System
This is an application to enable users to buy and sell items securely. Here, we implement a secure bidding system on a blockchain. The item information along with the bids are stored on the blockchain. In this project, we make use of Hyperledger Sawtooth.

Pre-requisites: Docker Compose Hyperledger Sawtooth

Files: client.py- This is the client file. This file connects to the validator and is responsible for making the transactions and batch list. There are four types of transactions: 1)Add an item for sale 2)View the items on sale 3)Place a bid 4)View existing bids

tp.py- This is the transaction processor. It is incharge of handling all the kinds of transactions. Currently, 3 handle cases have been implemented (1,2,3)

docker-compose.yaml- This is the yaml file that is incharge of setting up and deploying all the containers, namely, validator, bidding-processor, bidding-client, rest-api and so on.

Future Enhancements: We need to implement the 4th transaction handle case. We also need a mechanism to find the winner of the bid. After that, we need to perfect the command line interface. After which, we hope to implement GUI!

