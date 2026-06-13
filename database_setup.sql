CREATE DATABASE IF NOT EXISTS finvue_db;
USE finvue_db;

CREATE TABLE tbl_users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    currency_code VARCHAR(3) DEFAULT 'INR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tbl_categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    flow_type ENUM('Income', 'Expense') NOT NULL
);

CREATE TABLE tbl_transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    description TEXT,
    actual_date DATE NOT NULL,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES tbl_users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES tbl_categories(category_id)
);

CREATE TABLE tbl_budgets (
    budget_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    limit_amount DECIMAL(12,2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES tbl_users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES tbl_categories(category_id)
);

CREATE TABLE tbl_audit_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    action_performed VARCHAR(100) NOT NULL,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES tbl_users(user_id) ON DELETE CASCADE
);

INSERT INTO tbl_categories (name, flow_type) VALUES
('Salary', 'Income'),
('Freelance', 'Income'),
('Food', 'Expense'),
('Rent', 'Expense'),
('Transport', 'Expense'),
('Shopping', 'Expense'),
('Entertainment', 'Expense'),
('Education', 'Expense'),
('Utilities', 'Expense'),
('Healthcare', 'Expense'),
('Other Income', 'Income'),
('Other Expense', 'Expense');