--DROP IF Exists all tables
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS critics;
DROP TABLE IF EXISTS publications;
DROP TABLE IF EXISTS writes_for;


--

--
-- Name: movie; Type: TABLE; Schema:  Owner: Sean Grogg?; Tablespace: 
--

CREATE TABLE movies (
    movie_id integer PRIMARY KEY AUTOINCREMENT,
    movie_name varchar(100) NOT NULL,
    year_released smallint,
    budget smallint,
    gross integer,
    genre varchar(20)
);

--
-- Name: reviews; Type: TABLE; Schema:  Owner: Sean Grogg?; Tablespace: 
--

CREATE TABLE reviews(
    review_id integer PRIMARY KEY AUTOINCREMENT,
    review_text varchar(1000),
    movie_id integer,
    critic_id integer,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
    ON UPDATE CASCADE 
    ON DELETE CASCADE,
    FOREIGN KEY (critic_id) REFERENCES critics(critic_id)
    ON UPDATE CASCADE 
    ON DELETE CASCADE
);

--
-- Name: critics; Type: TABLE; Schema:  Owner: Sean Grogg?; Tablespace: 
--

CREATE TABLE critics(
    critic_id integer PRIMARY KEY AUTOINCREMENT,
    critic_name varchar(50)
);


