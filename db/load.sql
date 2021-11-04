\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);
\COPY Category FROM 'Category.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);
\COPY Cart FROM 'Cart.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SellerReviews FROM 'SellerReviews.csv' WITH DELIMITER ',' NULL '' CSV
\COPY ProductReviews FROM 'ProductReviews.csv' WITH DELIMITER ',' NULL '' CSV



