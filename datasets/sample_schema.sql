CREATE TABLE users (
  user_id INT PRIMARY KEY,
  user_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE,
  created_at TIMESTAMP
);

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(255) NOT NULL,
  price DECIMAL(10, 2),
  category_id INT
);

CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  user_id INT,
  order_date DATE,
  total_amount DECIMAL(10, 2),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);