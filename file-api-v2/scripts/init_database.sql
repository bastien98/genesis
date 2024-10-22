CREATE TABLE users
(
    user_id  INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    CONSTRAINT unique_username UNIQUE (username)
);

CREATE TABLE knowledge_bases
(
    kb_id   INT AUTO_INCREMENT,
    user_id INT          NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (kb_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT unique_user_kb_name UNIQUE (user_id, name),
    INDEX (user_id)
);

CREATE TABLE documents
(
    doc_id         INT AUTO_INCREMENT,
    kb_id          INT          NOT NULL,
    name  VARCHAR(255) NOT NULL,
    source  VARCHAR(255) NOT NULL,
    PRIMARY KEY (doc_id),
    FOREIGN KEY (kb_id) REFERENCES knowledge_bases (kb_id),
    CONSTRAINT unique_kb_doc_name UNIQUE (kb_id, name),
    INDEX (kb_id)
);


# initialize db with one user and an empty knowledge base
INSERT INTO users (username)
VALUES ('Bastien');

INSERT INTO knowledge_bases (kb_id, user_id, name)
VALUES (1, 1, 'kb-test');


select *
from knowledge_bases;
select *
from users;
select *
from documents;
