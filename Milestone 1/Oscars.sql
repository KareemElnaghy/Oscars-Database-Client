CREATE DATABASE Oscars;

USE Oscars;

CREATE TABLE movie (
    movieTitle VARCHAR(80) NOT NULL,
    releaseDate DATE NOT NULL,
    language VARCHAR(20),
    runtime INT,
    budget DECIMAL(15, 2),
    boxOffice DECIMAL(15, 2),
    PRIMARY KEY (movieTitle, releaseDate)
);

CREATE TABLE production_company (
    movieTitle VARCHAR(80) NOT NULL,
    releaseDate DATE NOT NULL,
    companyName VARCHAR(80),
    PRIMARY KEY (movieTitle, releaseDate, companyName)
    FOREIGN KEY (movieTitle, releaseDate) REFERENCES movie (movieTitle, releaseDate),
);

CREATE TABLE person (
    firstName VARCHAR(20) NOT NULL,
    lastName VARCHAR(25) NOT NULL,
    DOB DATE NOT NULL,
    birthCountry VARCHAR(40),
    deathDate DATE,
    PRIMARY KEY (firstName, lastName, DOB)
);

CREATE TABLE role (
    roleType VARCHAR(40) NOT NULL PRIMARY KEY
);

CREATE TABLE nomination (
    movieTitle VARCHAR(80),
    releaseDate DATE,
    categoryName VARCHAR(100),
    nominationYear YEAR,
    isWinner BOOLEAN,
    PRIMARY KEY (movieTitle, releaseDate, categoryName, nominationYear),
    FOREIGN KEY (movieTitle, releaseDate) REFERENCES movie (movieTitle, releaseDate)
);

CREATE TABLE user (
    email VARCHAR(100) NOT NULL PRIMARY KEY,
    username VARCHAR(50),
    birthDate DATE,
    gender CHAR(1),
    country VARCHAR(100)
);

CREATE TABLE person_role (
    firstName VARCHAR(20) NOT NULL,
    lastName VARCHAR(25) NOT NULL,
    DOB DATE NOT NULL,
    roleType VARCHAR(40) NOT NULL,
    careerStart YEAR,
    careerEnd YEAR,
    PRIMARY KEY (firstName, lastName, DOB, roleType),
    FOREIGN KEY (firstName, lastName, DOB) REFERENCES person (firstName, lastName, DOB),
    FOREIGN KEY (roleType) REFERENCES role (roleType)
);

CREATE TABLE person_movie (
    firstName VARCHAR(20),
    lastName VARCHAR(25),
    DOB DATE,
    movieTitle VARCHAR(80),
    releaseDate DATE,
    PRIMARY KEY (firstName, lastName, DOB, movieTitle, releaseDate),
    FOREIGN KEY (firstName, lastName, DOB) REFERENCES person (firstName, lastName, DOB),
    FOREIGN KEY (movieTitle, releaseDate) REFERENCES movie (movieTitle, releaseDate)
);

CREATE TABLE person_nomination (
    firstName VARCHAR(20) NOT NULL,
    lastName VARCHAR(25) NOT NULL,
    DOB DATE NOT NULL,
    categoryName VARCHAR(100) NOT NULL,
    nominationYear YEAR NOT NULL,
    movieTitle VARCHAR(80),
    releaseDate DATE,
    PRIMARY KEY (firstName, lastName, DOB, categoryName, nominationYear, movieTitle, releaseDate),
    FOREIGN KEY (firstName, lastName, DOB) REFERENCES person (firstName, lastName, DOB),
    FOREIGN KEY (movieTitle, releaseDate, categoryName, nominationYear) REFERENCES nomination (movieTitle, releaseDate, categoryName, nominationYear),
    FOREIGN KEY (movieTitle, releaseDate) REFERENCES movie (movieTitle, releaseDate)
);

CREATE TABLE user_nomination (
    movieTitle VARCHAR(80),
    releaseDate DATE,
    firstName VARCHAR(20),
    lastName VARCHAR(25),
    DOB DATE,
    email VARCHAR(100),
    categoryName VARCHAR(100),
    nominationYear YEAR,
    PRIMARY KEY (movieTitle, releaseDate, firstName, lastName, DOB, email, categoryName, nominationYear),
    FOREIGN KEY (movieTitle, releaseDate) REFERENCES movie (movieTitle, releaseDate),
    FOREIGN KEY (firstName, lastName, DOB) REFERENCES person (firstName, lastName, DOB),
    FOREIGN KEY (movieTitle, releaseDate, categoryName, nominationYear) REFERENCES nomination (movieTitle, releaseDate, categoryName, nominationYear),
    FOREIGN KEY (email) REFERENCES user (email)
);
