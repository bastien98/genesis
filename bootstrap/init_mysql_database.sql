-- Drop existing database if it exists and create a new one
DROP DATABASE IF EXISTS genesis;
CREATE DATABASE genesis;
USE genesis;

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

-- Insert initial data: one user and two knowledge bases
INSERT INTO users (username) VALUES ('bastien');

INSERT INTO knowledge_bases (user_id, name) VALUES (1, 'kb-test');
INSERT INTO knowledge_bases (user_id, name) VALUES (1, 'kb-test-2');

-- Query data to verify insertion
SELECT * FROM users;
SELECT * FROM knowledge_bases;
SELECT * FROM documents;

-- Dev query
DELETE FROM documents
WHERE doc_id = 7;

-------------------------------------------------------
-- Chat App Tables
-------------------------------------------------------

-- Create threads table for chat threads
CREATE TABLE threads
(
    thread_id   INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    thread_title VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX (user_id)
);

-- Create messages table for chat messages
CREATE TABLE messages
(
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    thread_id  INT NOT NULL,
    user_id    INT NOT NULL,
    message    TEXT NOT NULL,
    FOREIGN KEY (thread_id) REFERENCES threads(thread_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX (thread_id, user_id)
);
