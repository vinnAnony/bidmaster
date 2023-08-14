# BidMaster

A Django web app that manages live bidding in real-time using Websockets.

## Features

BidMaster provides the following features:

- [x] User authentication and authorization
- [x] Create, edit and delete bids/auctions
- [x] Create, edit and delete auctioneers
- [x] Create, edit and delete bidders
- [x] Create, edit and delete rooms (for bidding)
- [x] Websockets server for real-time bidding
- [x] Store bidding logs in MongoDB

## Playground

> NB. A user is added to the system by the admin, and assigned to a bidding room.
- To access the admin add `/admin` to the root url e.g. `localhost:8000/admin`
  
<a href="https://bidmaster.onrender.com/admin" target="_blank">BidMaster Admin Portal</a>
```
Default admin credentials:
username => admin
password => admin
```
1. Add a new user by creating a new entry in the `Users` list.
2. Add user as a bidder/auctioneer by either adding them to the `Bidders` or `Auctioneers` list in the Admin Portal.
3. Create an auction by creating a new entry in the `Auctions` list. This will automatically create an `Auction Room` for the auction.
4. Assign your auctioneer and bidders to an `Auction Room` by adding them to the `Auction Room Users` list.
5. Your setup is ready!

- Head over to the home page and log in as any of the users you created.
- To enjoy the websockets, log in as 2 different users assigned to the same `Auction Room` and place your bids. See the magic happen!
  > (either log in in 2 different browsers/open a private window)
