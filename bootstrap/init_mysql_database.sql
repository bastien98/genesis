-- Drop existing database if it exists and create a new one
DROP DATABASE IF EXISTS super_rag;
CREATE DATABASE super_rag;
USE super_rag;

-- Create users table
CREATE TABLE users
(
    user_id  INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    CONSTRAINT unique_username UNIQUE (username)
);

-- Create knowledge_bases table
CREATE TABLE knowledge_bases
(
    kb_id   INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    name    VARCHAR(255) NOT NULL,
    PRIMARY KEY (kb_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT unique_user_kb_name UNIQUE (user_id, name),
    INDEX (user_id)
);

-- Create documents table
CREATE TABLE documents
(
    doc_id  INT AUTO_INCREMENT,
    kb_id   INT NOT NULL,
    name    VARCHAR(255) NOT NULL,
    source  VARCHAR(255) NOT NULL,
    PRIMARY KEY (doc_id),
    FOREIGN KEY (kb_id) REFERENCES knowledge_bases (kb_id),
    CONSTRAINT unique_kb_doc_name UNIQUE (kb_id, name),
    INDEX (kb_id)
);

-- Insert initial data: one user and one knowledge base
INSERT INTO users (username) VALUES ('bastien');

INSERT INTO knowledge_bases (user_id, name) VALUES (1, 'kb-test');

-- Query data to verify insertion
SELECT * FROM users;
SELECT * FROM knowledge_bases;
SELECT * FROM documents;

-- dev queries
DELETE FROM documents
WHERE doc_id = 7;