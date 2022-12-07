# AuctionsBox - auction app
An auction app based on Django, Django REST Framework and PostgreSQL.

## Table of contents
* [Introduction](#introduction)
* [Web page](#web-page)
* [Technologies](#technologies)
* [Features](#features)
* [Illustrations](#illustrations)

## Introduction
The idea to create this app was born when I completed CS50's task. I wanted to build a more complex auction app. And use in one project most technologies I know.

## Web page
https://auctions-box.up.railway.app/

You can log in as a demo user to test functionality:
- login: user
- password: demo#321

Or create your own one.

PS: Unfortunately, free Postgres support is no longer available on Heroku. So the app is now deployed on the Railway.app service. But I faced there an issue with collecting static. So the AuctionsBox will work in debug mode till I find a solution.

## Technologies
- Python 3.10
- Django 4.0
- Django REST Framework 3.13
- PostgreSQL 10
- HTML 5
- CSS 3
- Docker
- Heroku/Railway
- Swagger

## Features
Using this app, you can:
- Check all active listings on the homepage
- Sort and order listings
- Get all active listings by category
- Get complete information about a listing
- Search for listings by name, description, or author
- Get API docs

If authenticated, you also can:
- Bid listings
- Add listings to your watchlist
- Add comments
- Create new listings
- Get a list of all your bids
- Get a list of all your listings
- Check and change your account info

Admin panel extended with:
- Extra info
- Filtering
- Search

API features:
- Documented with Swagger
- Token authentication
- Raw JSON serialized data
- Same functionality as with UI
- Change the max page size

## Illustrations
- Authentication
  - Registration, log in, log out
  ![auth_demo](https://user-images.githubusercontent.com/44866199/200441438-0213dcf1-d284-4045-bb51-2e2dd96c3de1.gif)
  - User Info
  ![change_user_info_demo](https://user-images.githubusercontent.com/44866199/200441452-2ad0e9d7-918c-4f7d-b2e2-5d73a54c25b0.gif)

- Unauthenticated user interface demo:

  - Navigation
  ![navigation_demo](https://user-images.githubusercontent.com/44866199/200444779-54affd1f-c446-4796-916f-00330c6d8604.gif)
  
  - Search
  ![search_demo_lq](https://user-images.githubusercontent.com/44866199/200446606-700ba73a-1c12-42d9-9672-cb25db1dd8eb.gif)
  
  - Pagination
  ![pagination_demo_1](https://user-images.githubusercontent.com/44866199/200621856-01bc25a1-3767-4d78-a34f-c40422bfa765.gif)
  ![pagination_demo_2](https://user-images.githubusercontent.com/44866199/200621886-b22f2d24-74b2-4238-b7dc-f5d444391ba8.gif)
  ![pagination_demo_3](https://user-images.githubusercontent.com/44866199/200621901-33417912-8914-4b2f-8f14-fce0507735d9.gif)
  
  - Detailed listing
  ![detailed_listing_demo](https://user-images.githubusercontent.com/44866199/200447451-ca21d81b-5f37-4e20-8217-31b4d487dbff.gif)

- Authenticated user interface demo:

  - Navigation
  ![nav_bar_demo](https://user-images.githubusercontent.com/44866199/200440426-1d1dbe5a-1b38-4e93-a61c-2ea7785a87c9.gif)

  - Bidding
  ![bid_demo](https://user-images.githubusercontent.com/44866199/200440617-0f0f4bdf-8422-44a2-bdb4-14d55e0fde1d.gif)

  - Watchlist
  ![watch_demo](https://user-images.githubusercontent.com/44866199/200440707-d8c22d60-693e-4696-a929-1efd5676ac4c.gif)

  - Comment
  ![comment_demo](https://user-images.githubusercontent.com/44866199/200440784-ec319bdf-d4ee-449e-ab3c-a5c2708e6f39.gif)

  - Add listing
  ![add_listing_demo](https://user-images.githubusercontent.com/44866199/200441023-92758cda-c70e-458a-9430-ac18ba15f938.gif)

- Admin-panel demo
![Admin-panel demo](https://user-images.githubusercontent.com/44866199/190412901-a6578c1d-ed08-4381-8b77-cb36f1510d38.gif)

- API:
    - Docs
    ![API_docs_demo_lq](https://user-images.githubusercontent.com/44866199/200445769-b8dd64d5-156b-4f99-ab8a-b72e8e509f18.gif)

    - Unauthenticated usage
    ![unauthorized_user_demo](https://user-images.githubusercontent.com/44866199/206253961-4c996b03-5831-4506-9134-dbfe334e26cd.gif)

    - Token authentication
    ![token_authorization_demo](https://user-images.githubusercontent.com/44866199/206254171-9c08a46e-1b51-436b-b2d2-ec0388ba0ca9.gif)

    - Authenticated usage
    ![authorized_user_demo](https://user-images.githubusercontent.com/44866199/206254240-8f9d1d09-eb34-4695-95e2-d2509f0f454b.gif)
