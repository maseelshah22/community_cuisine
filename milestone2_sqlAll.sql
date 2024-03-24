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
        CHECK (rating >= 1 AND rating <= 5)

-- make sure email is valid

ALTER TABLE users
       ADD CONSTRAINT chek_email_format 
       CHECK (email LIKE '%@%.%' AND email NOT LIKE '%@%..%' AND email NOT LIKE '%@.%');

