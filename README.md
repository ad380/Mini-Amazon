# Team Data Dinos
## Members and Roles:
Tess Noonan - Users Guru: responsible for Account / Purchases
Nicki Lee - Products Guru: responsible for Products
Edgardy Reyes - Carts Guru: responsible for Cart / Order
Ankitha Durvasula - Sellers Guru: responsible for Inventory / Order Fulfillment
Kyle Tran - Social Guru: responsible for Feedback / Messaging
## What Everyone Has Done Since Milestone 2:
Tess Noonan:
* Added address field to registering a new user
* Added a private user profile page
* Added ability to edit a user’s information
* Added the ability to randomly generate a large number of users

Nicki Lee:
* Added detailed products page
* Added ability to sort products by ascending/descending price or seller id

Edgardy Reyes:
* Added cart button
* Added ability to add a product to the cart
* Added cart view with subtotal

Ankitha Durvasula:
* Added sellers only page with:
Seller Inventory
Ability to add products
Order History
* Updated database design to remove seller’s table and instead find sellers from products

Kyle Tran:
* Updated gen.py and generated data for users, products, purchases, and product reviews
* added product reviews (+ count / avg) to each detailed product page
* added user product reviews to their private user profile



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

