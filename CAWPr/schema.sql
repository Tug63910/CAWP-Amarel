DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS post;

CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE post (
	id SERIAL PRIMARY KEY,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	url TEXT NOT NULL,
    party TEXT ,
	state TEXT ,
	level TEXT ,
	office TEXT ,
	profession TEXT ,
	text TEXT 
);

