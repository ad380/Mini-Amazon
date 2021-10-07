CREATE TABLE Users
(uid INTEGER NOT NULL PRIMARY KEY,
 email VARCHAR(256) NOT NULL UNIQUE,
 password VARCHAR(256) NOT NULL,
 name VARCHAR(256) NOT NULL,
 address VARCHAR(256) NOT NULL,
 balance FLOAT NOT NULL
);

CREATE TABLE Sellers
(seller_id INTEGER NOT NULL PRIMARY KEY REFERENCES Users(uid)
);

CREATE TABLE Products
(product_id INTEGER NOT NULL PRIMARY KEY,
seller_id INTEGER NOT NULL REFERENCES Sellers(seller_id),
name VARCHAR NOT NULL,
description VARCHAR NOT NULL,
category VARCHAR NOT NULL REFERENCES Category(category),
image BYTEA NOT NULL,
price FLOAT NOT NULL,
available_quantity INTEGER NOT NULL
);

CREATE TABLE Cart
(buyer_id INTEGER NOT NULL PRIMARY KEY REFERENCES Users(uid),
product_id INTEGER NOT NULL UNIQUE REFERENCES Products(product_id),
quantity INTEGER NOT NULL
);

CREATE TABLE Category
(category VARCHAR NOT NULL PRIMARY KEY
);

CREATE TABLE Transactions
(order_id INTEGER NOT NULL PRIMARY KEY,
 buyer_id INTEGER NOT NULL REFERENCES Users(uid),
 seller_id INTEGER NOT NULL REFERENCES Sellers(seller_id),
 date_time TIMESTAMP NOT NULL,
 product_id INTEGER NOT NULL REFERENCES Products(product_id),
 quantity INTEGER NOT NULL,
 total_price FLOAT NOT NULL,
 status VARCHAR(256)
 CHECK(CASE
	WHEN grade = 'f' THEN TRUE
	WHEN grade = 'nf' THEN TRUE
	ELSE FALSE
       END
 )
);

CREATE TABLE SellerReviews
(seller_id INTEGER NOT NULL REFERENCES Sellers(seller_id),
 buyer_id INTEGER NOT NULL REFERENCES Users(uid),
 rating INTEGER NOT NULL CHECK(rating BETWEEN 0 AND 5),
 comment VARCHAR(512) NOT NULL,
 PRIMARY KEY(seller_id, buyer_id)
);

CREATE TABLE ProductReviews
(product_id INTEGER NOT NULL REFERENCES Products(product_id),
 buyer_id INTEGER NOT NULL REFERENCES Users(uid),
 rating INTEGER NOT NULL CHECK(rating BETWEEN 0 AND 5),
 comment VARCHAR(512) NOT NULL,
 PRIMARY KEY(product_id, buyer_id)
 );
