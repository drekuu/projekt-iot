CREATE TABLE Courses (
    CourseID int NOT NULL,
    CourseName varchar(255) NOT NULL,
    PRIMARY KEY(CourseID)
);

CREATE TABLE Stops (
    StopID int NOT NULL,
    StopName varchar(255) NOT NULL,
    PRIMARY KEY(StopID)
);

CREATE TABLE Assignments (
    CourseID int NOT NULL,
    StopID int NOT NULL,
    StopNumber int NOT NULL,
    PRIMARY KEY(CourseID, StopID),
    FOREIGN KEY(CourseID) REFERENCES Courses(CourseID),
    FOREIGN KEY(StopID) REFERENCES Stops(StopID)
);

CREATE TABLE Workers (
    WorkerID int NOT NULL,
    WorkerFirstName varchar(255) NOT NULL,
    WorkerLastName varchar(255) NOT NULL,
    WorkerBalance int NOT NULL,
    WorkerCardID int varchar(255),
    PRIMARY KEY(WorkerID)
);

CREATE TABLE BUSES (
    BusID int NOT NULL,
    CourseID int NULL,
    StopsInAscendingOrder int NULL, --Boolean imitation
    StopID int NULL,
    FOREIGN KEY(StopID) REFERENCES Stops(StopID)
);

CREATE TABLE CurrentRides (
    RideID int NOT NULL,
    WorkerID int NOT NULL,
    StopsTraveled int NOT NULL,
    PRIMARY KEY(RideID, WorkerID),
    FOREIGN KEY(WorkerID) REFERENCES Workers(WorkerID)
);