CREATE TABLE Users
(id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
 email VARCHAR(256) NOT NULL UNIQUE,
 password VARCHAR(256) NOT NULL,
 firstname VARCHAR(256) NOT NULL,
 lastname VARCHAR(256) NOT NULL,
 address VARCHAR(256) NOT NULL,
 balance DECIMAL(12,2) NOT NULL
);

CREATE TABLE Category
(category VARCHAR NOT NULL PRIMARY KEY
);

CREATE TABLE Products
(id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
seller_id INTEGER NOT NULL REFERENCES Users(id),
name VARCHAR(255) NOT NULL,
description VARCHAR NOT NULL,
category VARCHAR NOT NULL REFERENCES Category(category),
image VARCHAR NOT NULL,
price DECIMAL(12,2) NOT NULL,
available_quantity INTEGER NOT NULL
);

CREATE TABLE Cart
(buyer_id INTEGER NOT NULL REFERENCES Users(id),
product_id INTEGER NOT NULL REFERENCES Products(id),
PRIMARY KEY(buyer_id, product_id),
quantity INTEGER NOT NULL
);

CREATE TABLE Purchases
(id INTEGER NOT NULL PRIMARY KEY,
 uid INTEGER NOT NULL REFERENCES Users(id),
 seller_id INTEGER NOT NULL REFERENCES Users(id),
 time_purchased TIMESTAMP without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
 pid INTEGER NOT NULL REFERENCES Products(id),
 quantity INTEGER NOT NULL,
 fulfilled VARCHAR(256)
 CHECK(CASE
	WHEN fulfilled = 'f' THEN TRUE
	WHEN fulfilled = 'nf' THEN TRUE
	ELSE FALSE
       END
 )
);

CREATE TABLE SellerReviews
(seller_id INTEGER NOT NULL REFERENCES Users(id),
 buyer_id INTEGER NOT NULL REFERENCES Users(id),
 rating FLOAT NOT NULL CHECK(rating BETWEEN 0.0 AND 5.0),
 title VARCHAR(64) NOT NULL,	
 comment VARCHAR(512) NOT NULL,
 date TIMESTAMP without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
 PRIMARY KEY(seller_id, buyer_id)
);

CREATE TABLE SellerReviewsUpvotes
(uid INTEGER NOT NULL REFERENCES Users(id),
seller_id INTEGER NOT NULL REFERENCES Users(id),
buyer_id INTEGER NOT NULL REFERENCES Users(id),
vote INTEGER NOT NULL CHECK(vote in (-1, 0, 1)),
PRIMARY KEY (uid, seller_id, buyer_id),
FOREIGN KEY (seller_id, buyer_id) REFERENCES  SellerReviews(seller_id, buyer_id) ON DELETE CASCADE
);

CREATE TABLE ProductReviews
(product_id INTEGER NOT NULL REFERENCES Products(id),
 buyer_id INTEGER NOT NULL REFERENCES Users(id),
 rating FLOAT NOT NULL CHECK(rating BETWEEN 0.0 AND 5.0),
 title VARCHAR(64) NOT NULL,
 comment VARCHAR(512) NOT NULL,
 date TIMESTAMP without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
 image VARCHAR NOT NULL,
 PRIMARY KEY(product_id, buyer_id)
 );

CREATE TABLE ProductReviewsUpvotes
(uid INTEGER NOT NULL REFERENCES Users(id),
product_id INTEGER NOT NULL REFERENCES Products(id),
buyer_id INTEGER NOT NULL REFERENCES Users(id),
vote INTEGER NOT NULL CHECK(vote in (-1, 0, 1)),
PRIMARY KEY (uid, product_id, buyer_id),
FOREIGN KEY (product_id, buyer_id) REFERENCES  ProductReviews(product_id, buyer_id) ON DELETE CASCADE
);