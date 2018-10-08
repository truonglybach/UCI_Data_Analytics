USE sakila;

#1a
SELECT first_name, last_name
FROM actor;

#1b
SELECT CONCAT(first_name, ' ', last_name) as `Actor Name`
FROM actor;

#2a
SELECT actor_id, first_name, last_name
FROM actor a
WHERE a.first_name LIKE 'JOE%';

#2b
SELECT first_name, last_name
FROM actor a
WHERE a.last_name
LIKE '%G%' '%E%' '%N%';

#2c
SELECT last_name, first_name
FROM actor a
WHERE a.last_name
LIKE '%L%' '%I%'
ORDER BY last_name;

#2d
SELECT country_id, country
FROM country c
WHERE c.country
IN ('Afghanistan', 'Bangladesh', 'China');

#3a
ALTER TABLE actor
ADD description BLOB AFTER last_update;

#3b
ALTER TABLE actor
DROP description;

#4a
SELECT last_name AS 'Last Name' , count(last_name) AS 'Number of Actors With This Last Name'
FROM actor
GROUP BY last_name;

#4b
SELECT last_name AS 'Last Name' , count(last_name) AS 'Number of Actors With This Last Name'
FROM actor
GROUP BY last_name
HAVING count(last_name) > 1;

#4c
UPDATE actor
SET first_name = 'HARPO'
WHERE first_name = 'GROUCHO' AND last_name = 'WILLIAMS';

#4d
UPDATE actor
SET first_name = 'GROUCHO'
WHERE first_name = 'HARPO' AND last_name = 'WILLIAMS';

#5a
SHOW CREATE TABLE address;

#6a
SELECT s.first_name, s.last_name, a.address
FROM staff s
JOIN address a ON 
s.address_id = a.address_id;

#6b
SELECT CONCAT(s.first_name, ' ', s.last_name) AS 'Employee', SUM(p.amount) as 'Amount'
FROM staff s
JOIN payment p
ON s.staff_id = p.staff_id
WHERE p.payment_date LIKE '%2005-08%'
GROUP BY CONCAT(s.first_name, ' ', s.last_name);

#6c
SELECT f.title AS 'Title of Movie', COUNT(fa.actor_id) 'Number of Actors/Actresses'
FROM film f
JOIN film_actor fa
ON f.film_id = fa.film_id
GROUP BY f.film_id;

#6d
SELECT COUNT(inventory_id) AS 'Number of Copies'
FROM inventory
WHERE film_id IN(
SELECT film_id
FROM film f
WHERE f.title = 'HUNCHBACK IMPOSSIBLE'
);

#6e
SELECT c.first_name AS 'First Name', c.last_name AS 'Last Name', SUM(p.amount) AS 'Total Amount Paid'
FROM customer c
JOIN payment p
ON c.customer_id = p.customer_id
GROUP BY c.customer_id
ORDER BY c.last_name ASC;

#7a
SELECT f.title AS 'Title of Movie', f.language_id AS 'Language ID'
FROM film f
WHERE f.title LIKE 'K%'
UNION
SELECT f.title, f.language_id
FROM film f
WHERE f.title LIKE 'Q%';

#7b
SELECT first_name AS 'First Name', last_name AS 'Last Name'
FROM actor
WHERE actor_id IN(
SELECT actor_id
FROM film_actor
WHERE film_id IN(
SELECT film_id
FROM film
WHERE title = 'Alone Trip'));

#7c
SELECT first_name AS 'First Name', last_name AS 'Last Name', email AS 'Email'
FROM customer
WHERE address_id IN(
SELECT address_id
FROM address
WHERE city_id IN(
SELECT city_id
FROM city
WHERE country_id IN(
SELECT country_id
FROM country
WHERE country = 'Canada')));

#7d
SELECT title AS 'All Family Films in Stock'
FROM film
WHERE film_id IN(
SELECT film_id
FROM film_category
WHERE category_id = 8);

#7e
SELECT title AS 'Title of Movie', rental_rate AS 'Rental Rate'
FROM film
ORDER BY rental_rate DESC;

#7f
SELECT store_id AS 'Store ID', SUM(amount) AS 'Total Business in Dollars'
FROM store, payment
WHERE customer_id IN(
SELECT customer_id
FROM customer)
GROUP BY store_id;

#7g
SELECT store_id
FROM store;

SELECT city
FROM city
WHERE city_id IN(
SELECT city_id
FROM address
WHERE address_id IN(
SELECT address_id
FROM store)
);

SELECT country
FROM country
WHERE country_id IN(
SELECT country_id
FROM city
WHERE city_id IN(
SELECT city_id
FROM city
WHERE city_id IN(
SELECT city_id
FROM address
WHERE address_id IN(
SELECT address_id
FROM store)
)
)
);

#7h
SELECT `name`
FROM category
WHERE category_id IN(
SELECT category_id
FROM film_category
WHERE film_id IN(
SELECT film_id
FROM inventory
WHERE inventory_id IN(
SELECT inventory_id
FROM rental
WHERE rental_id IN (
SELECT rental_id
FROM payment))));

SELECT r.rental_id, p.amount
FROM payment p
JOIN rental r
ON p.rental_id = r.rental_id;

SELECT film_id
FROM inventory
WHERE inventory_id IN(
SELECT inventory_id
FROM rental
WHERE rental_id IN (
SELECT rental_id
FROM payment));

#8a
CREATE VIEW join_category_filmc AS 
SELECT c.category_id, c.`name`, fc.film_id
FROM category c
JOIN film_category fc
ON c.category_id = fc.category_id;

#8b
SELECT * FROM join_category_filmc;

#8c
DROP VIEW join_category_filmc;



















