-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 20, 2024 at 05:02 PM
-- Server version: 10.6.16-MariaDB-0ubuntu0.22.04.1
-- PHP Version: 8.1.2-1ubuntu2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dda5us`
--

-- --------------------------------------------------------

--
-- Table structure for table `creates`
--

CREATE TABLE `creates` (
  `recipe_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dietary_warnings`
--

CREATE TABLE `dietary_warnings` (
  `recipe_id` int(11) NOT NULL,
  `spice_level` int(11) NOT NULL,
  `restrictions` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `food`
--

CREATE TABLE `food` (
  `food_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `ethnic_origin` varchar(255) NOT NULL,
  `meal_course` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `food`
--

INSERT INTO `food` (`food_id`, `name`, `ethnic_origin`, `meal_course`) VALUES
(1, 'Cheesecake', 'Western', 'Dessert'),
(2, 'Spaghetti Bolognese', 'Italian', 'Dinner'),
(3, 'Chicken Curry', 'Indian', 'Dinner'),
(4, 'Vegetable Stir Fry', 'Asian', 'Dinner'),
(5, 'Beef Stew', 'Western', 'Dinner'),
(6, 'Quiche Lorraine', 'French', 'Breakfast/Lunch'),
(7, 'Margherita Pizza', 'Italian', 'Lunch/Dinner'),
(8, 'Caesar Salad', 'Italian', 'Lunch/Dinner'),
(9, 'Grilled Salmon', 'General', 'Dinner'),
(10, 'Ratatouille', 'French', 'Dinner'),
(11, 'Pancakes', 'Western', 'Breakfast'),
(12, 'Tacos', 'Mexican', 'Lunch/Dinner'),
(13, 'Tomato Soup', 'General', 'Lunch/Dinner'),
(14, 'Lasagna', 'Italian', 'Dinner'),
(15, 'Hamburger', 'American', 'Lunch/Dinner'),
(16, 'Pad Thai', 'Thai', 'Dinner'),
(17, 'French Onion Soup', 'French', 'Lunch/Dinner'),
(18, 'Chocolate Cake', 'Western', 'Dessert'),
(19, 'Sushi Rolls', 'Japanese', 'Lunch/Dinner'),
(20, 'Banana Bread', 'Western', 'Breakfast/Dessert');

-- --------------------------------------------------------

--
-- Table structure for table `ingredients`
--

CREATE TABLE `ingredients` (
  `ingredient_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ingredients`
--

INSERT INTO `ingredients` (`ingredient_id`, `name`) VALUES
(70, 'all purpose flour'),
(16, 'baby corn'),
(27, 'bacon'),
(49, 'baking powder'),
(48, 'baking soda'),
(22, 'balsamic vinegar'),
(69, 'bay leaves'),
(8, 'beef bouillon cubes'),
(24, 'beef broth'),
(23, 'boneless beef chuck'),
(20, 'brown sugar'),
(80, 'carrot'),
(52, 'cheddar cheese'),
(13, 'chicken broth'),
(59, 'chicken stock'),
(73, 'chocolate buttercream frosting'),
(15, 'cinnamon'),
(71, 'coconut milk'),
(72, 'coconut oil'),
(1, 'cream cheese'),
(82, 'dark brown sugar'),
(37, 'dijon mustard'),
(47, 'egg'),
(30, 'egg white'),
(75, 'eggs'),
(54, 'flour tortillas'),
(35, 'fresh basil'),
(33, 'fresh mozzarella balls'),
(12, 'fresh tomatoes'),
(45, 'garlic powder'),
(3, 'graham cracker crumbs'),
(76, 'grain white rice'),
(6, 'ground beef'),
(14, 'heavy cream'),
(57, 'heavy whipping cream'),
(61, 'italian sausage'),
(64, 'lasagna noodles'),
(51, 'lean ground beef'),
(4, 'lemon juice'),
(41, 'lemon pepper'),
(40, 'parmesan cheese'),
(65, 'pasta sauce'),
(26, 'pie crust'),
(46, 'plain flour'),
(79, 'red onion'),
(55, 'red onions'),
(34, 'red pepper flakes'),
(7, 'red wine'),
(36, 'red wine vinegar'),
(78, 'rice vinegar'),
(63, 'ricotta cheese'),
(85, 'ripe bananas'),
(38, 'romaine lettuce'),
(44, 'salmon fillets'),
(56, 'san marzano'),
(32, 'san marzano tomatoes'),
(28, 'sharp white cheddar'),
(11, 'skinless chicken breasts'),
(2, 'sour cream'),
(19, 'soy sauce'),
(77, 'sriracha sauce'),
(60, 'sugar'),
(17, 'sugar snap peas'),
(9, 'tomato paste'),
(74, 'unsweetened cocoa powder'),
(5, 'vanilla extract'),
(18, 'water chestnuts'),
(66, 'white wine'),
(31, 'whole wheat pizza'),
(10, 'worcestershire sauce');

-- --------------------------------------------------------

--
-- Table structure for table `made_of`
--

CREATE TABLE `made_of` (
  `ingredient_id` int(11) NOT NULL,
  `recipe_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `person_name`
--

CREATE TABLE `person_name` (
  `username` varchar(255) NOT NULL,
  `first` varchar(255) NOT NULL,
  `last` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `person_name`
--

INSERT INTO `person_name` (`username`, `first`, `last`) VALUES
('hayden.johnson', 'Hayden', 'Johnson'),
('ilyas.jaghoori', 'Ilyas', 'Jaghoori'),
('maseel.shah', 'Maseel', 'Shah'),
('mohammad.murad', 'Mohammad', 'Murad');

-- --------------------------------------------------------

--
-- Table structure for table `rating`
--

CREATE TABLE `rating` (
  `review_id` int(11) NOT NULL,
  `recipe_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `star` int(11) NOT NULL,
  `comment` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `recipe`
--

CREATE TABLE `recipe` (
  `recipe_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `food_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `recipe`
--

INSERT INTO `recipe` (`recipe_id`, `title`, `food_id`) VALUES
(1, 'Best Classic Cheesecake Recipe', 1),
(2, 'Spaghetti Bolognese', 2),
(3, 'Chicken Curry', 3),
(4, 'The Easiest Vegetable Stir Fry', 4),
(5, 'Beef Stew with Carrots & Potatoes', 5),
(6, 'Classic Quiche Lorraine Recipe', 6),
(7, 'Margherita Pizza', 7),
(8, 'Caesar Salad Recipe', 8),
(9, 'Grilled Salmon', 9),
(10, 'Best Fluffy Pancakes', 11),
(11, 'Ground Beef Tacos', 12),
(12, 'Creamy Tomato Soup Recipe', 13),
(13, 'Easy Homemade Lasagna', 14),
(14, 'French Onion Soup', 17),
(15, 'The Best Chocolate Cake Recipe {Ever}', 18),
(16, 'Vegetarian Sushi Rolls', 19),
(17, 'My Favorite Banana Bread', 20),
(26, 'Grilled Salmon', 9),
(27, 'Best Fluffy Pancakes', 11),
(28, 'Ground Beef Tacos', 12),
(29, 'Creamy Tomato Soup Recipe', 13),
(30, 'Easy Homemade Lasagna', 14),
(31, 'French Onion Soup', 17),
(32, 'The Best Chocolate Cake Recipe {Ever}', 18),
(33, 'Vegetarian Sushi Rolls', 19),
(34, 'My Favorite Banana Bread', 20);

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `review_id` int(11) NOT NULL,
  `recipe_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `email`, `password`) VALUES
('hayden.johnson', 'cxy6nx@virginia.edu', 'securepassword'),
('ilyas.jaghoori', 'zyh7ac@virginia.edu', 'evenmoresecurepassword'),
('maseel.shah', 'dda5us@virginia.edu', 'moresecurepassword'),
('mohammad.murad', 'vdr4jr@virginia.edu', 'mostsecurepassword');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `creates`
--
ALTER TABLE `creates`
  ADD PRIMARY KEY (`recipe_id`,`username`),
  ADD UNIQUE KEY `recipe_id` (`recipe_id`,`username`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `dietary_warnings`
--
ALTER TABLE `dietary_warnings`
  ADD PRIMARY KEY (`recipe_id`),
  ADD UNIQUE KEY `recipe_id` (`recipe_id`);

--
-- Indexes for table `food`
--
ALTER TABLE `food`
  ADD PRIMARY KEY (`food_id`),
  ADD UNIQUE KEY `food_id` (`food_id`);

--
-- Indexes for table `ingredients`
--
ALTER TABLE `ingredients`
  ADD PRIMARY KEY (`ingredient_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `made_of`
--
ALTER TABLE `made_of`
  ADD PRIMARY KEY (`ingredient_id`,`recipe_id`),
  ADD UNIQUE KEY `ingredient_id` (`ingredient_id`,`recipe_id`),
  ADD KEY `recipe_id` (`recipe_id`);

--
-- Indexes for table `person_name`
--
ALTER TABLE `person_name`
  ADD PRIMARY KEY (`username`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `rating`
--
ALTER TABLE `rating`
  ADD PRIMARY KEY (`review_id`,`recipe_id`,`username`),
  ADD UNIQUE KEY `review_id` (`review_id`,`recipe_id`,`username`),
  ADD KEY `recipe_id` (`recipe_id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `recipe`
--
ALTER TABLE `recipe`
  ADD PRIMARY KEY (`recipe_id`),
  ADD UNIQUE KEY `recipe_id` (`recipe_id`),
  ADD KEY `food_id` (`food_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`review_id`,`recipe_id`,`username`),
  ADD UNIQUE KEY `review_id` (`review_id`,`recipe_id`,`username`),
  ADD KEY `recipe_id` (`recipe_id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`),
  ADD UNIQUE KEY `username` (`username`,`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `food`
--
ALTER TABLE `food`
  MODIFY `food_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `ingredients`
--
ALTER TABLE `ingredients`
  MODIFY `ingredient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=86;

--
-- AUTO_INCREMENT for table `recipe`
--
ALTER TABLE `recipe`
  MODIFY `recipe_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `review_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `creates`
--
ALTER TABLE `creates`
  ADD CONSTRAINT `creates_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`recipe_id`),
  ADD CONSTRAINT `creates_ibfk_2` FOREIGN KEY (`username`) REFERENCES `users` (`username`);

--
-- Constraints for table `dietary_warnings`
--
ALTER TABLE `dietary_warnings`
  ADD CONSTRAINT `dietary_warnings_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`recipe_id`);

--
-- Constraints for table `made_of`
--
ALTER TABLE `made_of`
  ADD CONSTRAINT `made_of_ibfk_1` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`ingredient_id`),
  ADD CONSTRAINT `made_of_ibfk_2` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`recipe_id`);

--
-- Constraints for table `rating`
--
ALTER TABLE `rating`
  ADD CONSTRAINT `rating_ibfk_1` FOREIGN KEY (`review_id`) REFERENCES `reviews` (`review_id`),
  ADD CONSTRAINT `rating_ibfk_2` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`recipe_id`),
  ADD CONSTRAINT `rating_ibfk_3` FOREIGN KEY (`username`) REFERENCES `users` (`username`);

--
-- Constraints for table `recipe`
--
ALTER TABLE `recipe`
  ADD CONSTRAINT `recipe_ibfk_1` FOREIGN KEY (`food_id`) REFERENCES `food` (`food_id`);

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`recipe_id`),
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`username`) REFERENCES `users` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
