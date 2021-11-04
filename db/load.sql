\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);
\COPY Sellers FROM 'data/Sellers.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Category FROM 'data/Category.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);
\COPY Cart FROM 'data/Cart.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);s
\COPY SellerReviews FROM 'data/SellerReviews.csv' WITH DELIMITER ',' NULL '' CSV
\COPY ProductReviews FROM 'data/ProductReviews.csv' WITH DELIMITER ',' NULL '' CSV



