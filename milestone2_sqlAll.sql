-- SQL for Milestone 2

-- SQL we have 
-- creating tables

-- make users table
 CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    PRIMARY KEY (username),
                    UNIQUE (username, email)
                )
-- person_name
CREATE TABLE IF NOT EXISTS person_name (
                    username VARCHAR(255) NOT NULL,
                    first VARCHAR(255) NOT NULL,
                    last VARCHAR(255) NOT NULL,
                    PRIMARY KEY (username),
                    UNIQUE (username)
                )

-- food table
CREATE TABLE IF NOT EXISTS food (
                    food_id INT NOT NULL AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    ethnic_origin VARCHAR(255) NOT NULL,
                    meal_course VARCHAR(255) NOT NULL,
                    PRIMARY KEY (food_id),
                    UNIQUE (food_id)
                ) 
-- recipe table
CREATE TABLE IF NOT EXISTS recipe (
                    recipe_id INT NOT NULL AUTO_INCREMENT,
                    title VARCHAR(255) NOT NULL,
                    food_id INT NOT NULL,
                    PRIMARY KEY (recipe_id),
                    UNIQUE (recipe_id),
                    FOREIGN KEY (food_id) REFERENCES food(food_id)
                )

ALTER TABLE recipe 
ADD COLUMN IF NOT EXISTS average_rating DECIMAL(3, 2) DEFAULT NULL;

-- dietary_warnings table
CREATE TABLE IF NOT EXISTS dietary_warnings (
                    recipe_id INT NOT NULL,
                    spice_level INT NOT NULL,
                    restrictions VARCHAR(255) NOT NULL,
                    PRIMARY KEY (recipe_id),
                    UNIQUE (recipe_id),
                    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id)
                )

ALTER TABLE dietary_warnings
ADD CONSTRAINT chk_spice_level CHECK (spice_level BETWEEN 1 AND 5);

-- ingredients table
CREATE TABLE IF NOT EXISTS ingredients (
                    ingredient_id INT NOT NULL AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    PRIMARY KEY (ingredient_id),
                    UNIQUE (name)
                )
-- made_of table
CREATE TABLE IF NOT EXISTS made_of (
                    ingredient_id INT NOT NULL,
                    recipe_id INT NOT NULL,
                    PRIMARY KEY (ingredient_id, recipe_id),
                    UNIQUE (ingredient_id, recipe_id),
                    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id),
                    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id)
                )

--creates table
CREATE TABLE IF NOT EXISTS creates (
                    recipe_id INT NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    PRIMARY KEY (recipe_id, username),
                    UNIQUE (recipe_id, username),
                    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),
                    FOREIGN KEY (username) REFERENCES users(username)
                )

-- reviews table
CREATE TABLE IF NOT EXISTS reviews (
                    review_id INT NOT NULL AUTO_INCREMENT,
                    recipe_id INT NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    PRIMARY KEY (review_id, recipe_id, username),
                    UNIQUE (recipe_id, username),
                    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),
                    FOREIGN KEY (username) REFERENCES users(username)
                )

-- rating table
CREATE TABLE IF NOT EXISTS rating (
                    review_id INT NOT NULL,
                    recipe_id INT NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    star INT NOT NULL,
                    comment VARCHAR(255),
                    PRIMARY KEY (review_id, recipe_id, username),
                    UNIQUE (review_id, recipe_id, username),
                    FOREIGN KEY (review_id) REFERENCES reviews(review_id),
                    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),
                    FOREIGN KEY (username) REFERENCES users(username)
                )

-- sql we did for inserting starter data

-- insert into users
INSERT IGNORE INTO users (username, email, password)
VALUES ('hayden.johnson', 'cxy6nx@virginia.edu', 'securepassword')

INSERT IGNORE INTO users (username, email, password)
                VALUES ('maseel.shah', 'dda5us@virginia.edu', 'moresecurepassword')

 INSERT IGNORE INTO users (username, email, password)
                VALUES ('ilyas.jaghoori', 'zyh7ac@virginia.edu', 'evenmoresecurepassword')

INSERT IGNORE INTO users (username, email, password)
                VALUES ('mohammad.murad', 'vdr4jr@virginia.edu', 'mostsecurepassword')

INSERT IGNORE INTO person_name (username, first, last)
                VALUES ('hayden.johnson', 'Hayden', 'Johnson')

INSERT IGNORE INTO person_name (username, first, last)
                VALUES ('maseel.shah', 'Maseel', 'Shah')

INSERT IGNORE INTO person_name (username, first, last)
                VALUES ('ilyas.jaghoori', 'Ilyas', 'Jaghoori')

INSERT IGNORE INTO person_name (username, first, last)
                VALUES ('mohammad.murad', 'Mohammad', 'Murad')

-- will not include sql commands for inserting recipe and dietary warnings
    -- as that information is nested with python syntax, not just in quotes.
        -- that information can be show in the create_db.py file

-- advanced sql

-- Trigger function make sure users only review a recipe once
CREATE TRIGGER IF NOT EXISTS UpdateAverageRating 
    AFTER INSERT ON rating 
    FOR EACH ROW 
    BEGIN 
        DECLARE new_avg DECIMAL(3, 2); 
        SELECT AVG(star) INTO new_avg FROM rating WHERE recipe_id = NEW.recipe_id; 
        UPDATE recipe SET average_rating = new_avg WHERE recipe_id = NEW.recipe_id; 
    END;

-- make sure rating is between 1 and 5

 ALTER TABLE rating
        ADD CONSTRAINT check_rating_range
        CHECK (star >= 1 AND star <= 5)

-- make sure email is valid

ALTER TABLE users
       ADD CONSTRAINT chek_email_format 
       CHECK (email LIKE '%@%.%' AND email NOT LIKE '%@%..%' AND email NOT LIKE '%@.%');

-- FUTURE SQL COMMANDS TO RUN/ WILL BE USED IN PROJECT
-- will use dummy variable names for high level description

INSERT INTO users (username, email, password) 
VALUES ('username', 'email@email.com', 'password');

DELETE FROM users WHERE username = 'username';

INSERT INTO person_name (username, first, last) VALUES ('username', 'First', 'Last');

INSERT INTO food (name, ethnic_origin, meal_course) VALUES ('FoodName', 'Origin', 'Course');

DELETE FROM food WHERE name = 'FoodName';

INSERT INTO recipe (title, food_id, average_rating) 
VALUES ('RecipeTitle', food_id, null);

INSERT INTO dietary_warnings (recipe_id, spice_level, restrictions) 
VALUES (recipe_id, 3, 'Restrictions');

UPDATE dietary_warnings SET spice_level = 4 WHERE recipe_id = recipe_id;

INSERT INTO ingredients (name) VALUES ('IngredientName');

UPDATE ingredients SET name = 'NewName' WHERE ingredient_id = id;

DELETE FROM ingredients WHERE ingredient_id = id;

INSERT INTO made_of (ingredient_id, recipe_id) VALUES (ingredient_id, recipe_id);

SELECT * FROM food WHERE name = 'FoodName';

SELECT * FROM recipe WHERE title = 'RecipeTitle';

SELECT * FROM dietary_warnings WHERE recipe_id = recipe_id;

SELECT * FROM recipe WHERE meal_course = 'CourseType';

-- all ingredients for a recipe
SELECT i.* 
FROM ingredients i INNER JOIN made_of m ON i.ingredient_id = m.ingredient_id 
WHERE m.recipe_id = recipe_id;

-- all recipes created by a user
SELECT r.* 
FROM recipe r INNER JOIN creates c ON r.recipe_id = c.recipe_id 
WHERE c.username = 'username';

SELECT AVG(star) AS average_rating 
FROM rating 
WHERE recipe_id = recipe_id;

--revies and the users who made them

SELECT r.*, u.username 
FROM reviews r INNER JOIN users u ON r.username = u.username 
WHERE r.recipe_id = recipe_id;

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
INNER JOIN rating rt ON r.recipe_id = rt.recipe_id
WHERE rt.star = desired_rating;

-- comments for recipe reviews
SELECT r.comment
FROM reviews r
INNER JOIN rating ra ON r.review_id = ra.review_id
WHERE r.recipe_id = recipe_id;












