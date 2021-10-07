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

CREATE TABLE Transactions
(order_id INTEGER NOT NULL PRIMARY KEY,
 buyer_id INTEGER NOT NULL REFERENCES Users(uid),
 seller_id INTEGER NOT NULL REFERENCES Sellers(seller_id),
 date_time TIMESTAMP NOT NULL,
 product_id INTEGER NOT NULL REFERENCES Products(product_id),
 quantity INTEGER NOT NULL,
 total_price INTEGER NOT NULL,
 status VARCHAR(256)
 CHECK(CASE
	WHEN grade = 'f' THEN TRUE
	WHEN grade = 'nf' THEN TRUE
	ELSE FALSE
       END
 )
);