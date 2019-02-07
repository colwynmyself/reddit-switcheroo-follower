CREATE SEQUENCE links_id_seq;
CREATE TABLE links(
   id INT PRIMARY KEY NOT NULL DEFAULT nextval('links_id_seq'),
   url VARCHAR(500) NOT NULL,
   text VARCHAR(100) NOT NULL,
   depth INT NOT NULL,
   parent_link_id INT REFERENCES links(id)
);
ALTER SEQUENCE links_id_seq OWNED BY links.id;

CREATE SEQUENCE user_id_seq;
CREATE TABLE users(
   id INT PRIMARY KEY NOT NULL DEFAULT nextval('user_id_seq'),
   reddit_id VARCHAR(32) NOT NULL UNIQUE,
   username TEXT NOT NULL
);
ALTER SEQUENCE user_id_seq OWNED BY users.id;
CREATE INDEX user_reddit_id_idx ON users(reddit_id);

CREATE SEQUENCE subreddit_id_seq;
CREATE TABLE subreddits(
   id INT PRIMARY KEY NOT NULL DEFAULT nextval('subreddit_id_seq'),
   reddit_id VARCHAR(32) NOT NULL UNIQUE,
   name VARCHAR(32) NOT NULL
);
ALTER SEQUENCE subreddit_id_seq OWNED BY subreddits.id;
CREATE INDEX subreddit_reddit_id_idx ON subreddits(reddit_id);

CREATE SEQUENCE submission_id_seq;
CREATE TABLE submissions(
   id INT PRIMARY KEY NOT NULL DEFAULT nextval('submission_id_seq'),
   reddit_id VARCHAR(32) NOT NULL UNIQUE,
   title TEXT NOT NULL,
   text TEXT,
   permalink TEXT,
   url TEXT,
   author_id INT NOT NULL REFERENCES users(id),
   subreddit_id INT NOT NULL REFERENCES subreddits(id)
);
ALTER SEQUENCE submission_id_seq OWNED BY submissions.id;
CREATE INDEX submission_reddit_id_idx ON submissions(reddit_id);

CREATE SEQUENCE comment_id_seq;
CREATE TABLE comments(
   id INT PRIMARY KEY NOT NULL DEFAULT nextval('comment_id_seq'),
   reddit_id VARCHAR(32) NOT NULL UNIQUE,
   body TEXT,
   permalink TEXT,
   author_id INT NOT NULL REFERENCES users(id),
   subreddit_id INT NOT NULL REFERENCES subreddits(id),
   submission_id INT REFERENCES submissions(id),
   parent_comment_id INT REFERENCES comments(id)
);
ALTER SEQUENCE comment_id_seq OWNED BY comments.id;
CREATE INDEX comment_reddit_id_idx ON comments(reddit_id);
