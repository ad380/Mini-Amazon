# Team Data Dinos
## Members and Roles:
Tess Noonan - Users Guru: responsible for Account / Purchases

Nicki Lee - Products Guru: responsible for Products

Edgardy Reyes - Carts Guru: responsible for Cart / Order

Ankitha Durvasula - Sellers Guru: responsible for Inventory / Order Fulfillment

Kyle Tran - Social Guru: responsible for Feedback / Messaging
## Grading Option:
Tess Noonan - Team

Nicki Lee - Team

Edgardy Reyes - Individual

Ankitha Durvasula - Team

Kyle Tran - Team
## What Everyone Has Done Since Milestone 3:
Tess Noonan:
* Changed editing user information from one form for everything to editing one item (i.e. name) at a time
* Added password verification when editing user information (for security)
* Modified columns in the private user profile’s recent purchases
* Added ability to sort a user’s past purchases (in a drop down menu)
* Created public user profiles
* Added links to public user profiles from products and purchases tables
* I commented my code so if a new person picked it up, they’d be able to understand it
* Incorporated the Kyle’s seller reviews to user profiles
* Worked with Ankitha to add functionality for a non-seller to become a seller by adding a product (linked from user profile)
* Added product name search bar to recent user purchases

Nicki Lee:
* Implemented search by product name feature
* Changed sorting and filtering from individual buttons to drop down menus 
* Made a Review Product form for reviewing previously purchased products
* Implemented Review Product checking so that users may only review products once signed-in, may only review products they have purchased, and can only leave one review per product
* Added the category section to the detailed product page of each product
* Adding sort by average rating to index page

Edgardy Reyes:
* Reimplemented cart functionality
* Reimplemented add to cart button on detailed product page
* Instead of using sessions, adding to cart just adds a product_id buyer_id pair to the cart table and then queries the cart table to show all the products associated with the current user id, so that cart items are persistent for each user
* Implemented submit order button, which updates the cart, purchases, product, and user tables to reflect new changes in balance, quantities, order history, etc.

Ankitha Durvasula:
* Moved Seller Inventory into User page
* Fixed add products submission to generate a new product id and add to the database 
* Added edit and delete product pages to view product information and either edit the quantity or delete
* Added edit to order status 
* Separated inventory page and orders page
* Added images to tables and add products
* Added order by quantity for inventory
* Added sort by product name to inventory
* Added filter by order status along with search by buyer name and product name to order history
* Added visualization of order status counts

Kyle Tran:
* Redid entire UI for reviews
* Made summary ratings sections for reviews with average and number of ratings
* Added ability to convert a raw rating score into stars
* Made drop down button to sort reviews by rating and most recent
* Added ability to add, edit, and delete reviews for products/sellers
* Made it so you can submit image to review
* Made pages for user to list their ratings/reviews that they authored
* developed upvote functionality for ratings/reviews, also display the top reviews
* Generated large testing database with realistic data





## Accessing Our Work
See our GitLab repository [here](https://gitlab.oit.duke.edu/data-dinos/mini-amazon-skeleton).
Our code files are as follows:
**db/gen.py**
* Code for creating and populating csv files to use for database

**db/data**
* Contains CSV files with data for each table

**db/create.sql**
* Creates all necessary tables

**db/load.sql**
* Loads csv data into tables
## How to load new generated data
Run the following commands

`sudo service postgresql restart`

`bash setup.sh`
