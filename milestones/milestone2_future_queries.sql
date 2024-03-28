-- SQL for Milestone 2


-- The SQL we have made so far is in the .sql file and includes the creates/ starting inserts.
 -- We do not plan on making any new tables.

-- FUTURE SQL COMMANDS TO RUN/ WILL BE USED IN PROJECT
-- will use dummy variable names for high level description

-- inserting data in tables

-- inserting into users table
INSERT INTO users (username, email, password) 
VALUES ('username', 'email@email.com', 'password');

-- inserting into person_name table
INSERT INTO person_name (username, first, last) 
VALUES ('username', 'First', 'Last');

-- inserting into food table
INSERT INTO food (name, ethnic_origin, meal_course) 
VALUES ('FoodName', 'Origin', 'Course');

-- inserting into recipe table
INSERT INTO recipe (title, food_id,average_rating) 
VALUES ('RecipeTitle', food_id, average_rating);

-- inserting into dietary_warnings table
INSERT INTO dietary_warnings (recipe_id, spice_level, restrictions) 
VALUES (recipe_id, 3, 'Restrictions');

-- inserting into ingredients table
INSERT INTO ingredients (name) 
VALUES ('IngredientName');

-- inserting into made_of table
INSERT INTO made_of (ingredient_id, recipe_id) 
VALUES (ingredient_id, recipe_id);

-- inserting into creates table
INSERT INTO creates (recipe_id, username) 
VALUES (recipe_id, 'username');

-- inserting into reviews table
INSERT INTO reviews (review_id, recipe_id, username) 
VALUES (review_id, recipe_id, 'username');

-- inserting into rating table
INSERT INTO rating (review_id, recipe_id, username, star, comment) 
VALUES (review_id, recipe_id, 'username', 5, 'Great recipe!');

-- deleting from users table
DELETE FROM users 
WHERE username = 'username';

-- deleting from food table
DELETE FROM food 
WHERE name = 'FoodName';

-- deleting data from ingredients table
DELETE FROM ingredients 
WHERE ingredient_id = id;

-- deleting data from person_name table
DELETE FROM person_name 
WHERE username = 'username';

-- deleting data from recipe table
DELETE FROM recipe 
WHERE recipe_id = recipe_id;

-- deleting data from dietary_warnings table
DELETE FROM dietary_warnings 
WHERE recipe_id = recipe_id;

-- deleting data from made_of table
DELETE FROM made_of 
WHERE ingredient_id = ingredient_id AND recipe_id = recipe_id;

-- deleting data from creates table
DELETE FROM creates 
WHERE recipe_id = recipe_id AND username = 'username';

-- deleting data from reviews table
DELETE FROM reviews 
WHERE review_id = review_id;

-- deleting data from rating table
DELETE FROM rating 
WHERE review_id = review_id;

-- selecting from food table
SELECT * FROM food 
WHERE name = 'FoodName';

-- selecting specific recipe from recipe table
SELECT * FROM recipe 
WHERE title = 'RecipeTitle';

-- selecting from dietary_warnings table
SELECT * FROM dietary_warnings 
WHERE recipe_id = recipe_id;

-- selecting from recipe table for a specific course
SELECT * FROM recipe 
WHERE meal_course = 'CourseType';

-- all ingredients for a recipe
SELECT i.name
FROM ingredients i
INNER JOIN made_of m ON i.ingredient_id = m.ingredient_id
WHERE m.recipe_id = 'recipe_id';


-- all recipes created by a user
SELECT r.title, r.food_id, r.recipe_id
FROM recipe r
INNER JOIN creates c ON r.recipe_id = c.recipe_id
WHERE c.username = 'username';

-- getting average rating of recipe
SELECT AVG(star) AS average_rating 
FROM rating 
WHERE recipe_id = recipe_id;

--reviews and the users who made them

SELECT r.review_id, r.recipe_id, r.username, r.comment, u.username AS reviewer_username
FROM reviews r
INNER JOIN users u ON r.username = u.username
WHERE r.recipe_id = 'recipe_id';


-- getting a recipe and its ingredients

SELECT r.title AS recipe_title, i.name AS ingredient_name
FROM recipe r
INNER JOIN made_of m ON r.recipe_id = m.recipe_id
INNER JOIN ingredients i ON m.ingredient_id = i.ingredient_id
WHERE r.recipe_id = recipe_id; 

-- getting a recipe and its dietary warnings

SELECT r.title AS recipe_title, d.spice_level, d.restrictions
FROM recipe r
INNER JOIN dietary_warnings d ON r.recipe_id = d.recipe_id
WHERE r.recipe_id = recipe_id;

-- getting a recipe and its average rating

SELECT r.title AS recipe_title, AVG(star) AS average_rating
FROM recipe r
INNER JOIN rating ra ON r.recipe_id = ra.recipe_id
WHERE r.recipe_id = recipe_id

-- getting a recipe from a specific background
SELECT r.title, r.recipe_id
FROM recipe r
INNER JOIN food f ON r.food_id = f.food_id
WHERE f.ethnic_origin = 'EthnicBackground';

-- recipes without a certain ingredient
SELECT r.title AS recipe_title
FROM recipe r
LEFT JOIN made_of m ON r.recipe_id = m.recipe_id
LEFT JOIN ingredients i ON m.ingredient_id = i.ingredient_id
WHERE i.name IS NULL OR i.name NOT IN ('Ingredient1', 'Ingredient2');

-- recipes without a certain ingredient

SELECT r.title AS recipe_title
FROM recipe r
LEFT JOIN dietary_warnings dw ON r.recipe_id = dw.recipe_id
WHERE dw.restrictions IS NULL OR dw.restrictions NOT LIKE '%DietaryRestriction%';

-- recipes with a certain spice level
SELECT r.title AS recipe_title
FROM recipe r 
INNER JOIN dietary_warnings dw ON r.recipe_id = dw.recipe_id
WHERE dw.spice_level = 3;

-- recipes with a certain rating
SELECT r.title AS recipe_title
FROM recipe r
INNER JOIN rating rat ON r.recipe_id = rat.recipe_id
WHERE rat.star = desired_rating;

-- recpies with a certain rating threshold
SELECT r.title AS recipe_title, AVG(rt.star) AS average_rating
FROM recipe r
LEFT JOIN rating rt ON r.recipe_id = rt.recipe_id
GROUP BY r.title
HAVING AVG(rt.star) > desired_rating;

-- comments for recipe reviews
SELECT r.comment
FROM reviews r
INNER JOIN rating ra ON r.review_id = ra.review_id
WHERE r.recipe_id = recipe_id;


-- deleting a recipe

DELETE rec, made, c, rev, rate
FROM recipe rec
LEFT JOIN made_of made ON rec.recipe_id = made.recipe_id
LEFT JOIN creates c ON rec.recipe_id = c.recipe_id
LEFT JOIN reviews rev ON rec.recipe_id = rev.recipe_id
LEFT JOIN rating rate ON rev.review_id = rate.review_id
WHERE r.title = 'RecipeTitle';

-- updating a recipes name
UPDATE recipe
SET title = 'NewRecipeTitle'
WHERE recipe_id = recipe_id;

-- update spice level
UPDATE dietary_warnings 
SET spice_level = 4 
WHERE recipe_id = recipe_id;

-- changing ingredient name
UPDATE ingredients 
SET name = 'NewName' 
WHERE ingredient_id = id;

-- update recipe ingredients
UPDATE made_of
SET ingredient_id = 'new ingredient id'
WHERE recipe_id = 'recipe_id' AND ingredient_id = 'old ingredient id';





