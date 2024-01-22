INSERT INTO Courses
    (CourseID, CourseName)
VALUES
    (1, "LongCourse"),
    (2, "MediumLengthCourse"),
    (3, "ShortCourse");


INSERT INTO Stops
    (StopID, StopName)
VALUES
    (1, "Church"),
    (2, "University of Economics"),
    (3, "Botanical Garden"),
    (4, "Swimming Pool"),
    (5, "Central Park"),
    (6, "City Hall"),
    (7, "Museum of Art"),
    (8, "Market Square"),
    (9, "Public Library"),
    (10, "Coffee House"),
    (11, "Zoo Entrance"),
    (12, "Our Company"),
    (13, "Shopping Mall"),
    (14, "Amusement Park"),
    (15, "Train Station"),
    (16, "Airport Terminal"),
    (17, "Science Center"),
    (18, "Downtown Plaza"),
    (19, "Ice Cream Parlor"),
    (20, "Tech Hub");


INSERT INTO Assignments
    (CourseID, StopID, StopNumber)
VALUES
    (1, 1, 1),
    (1, 2, 2),
    (1, 3, 3),
    (1, 4, 4),
    (1, 5, 5),
    (1, 6, 6),
    (1, 7, 7),
    (1, 8, 8),
    (1, 9, 9),
    (1, 10, 10),
    (1, 11, 11),
    (1, 12, 12),

    (2, 12, 8),
    (2, 13, 1),
    (2, 14, 2),
    (2, 15, 3),
    (2, 16, 4),
    (2, 17, 5),
    (2, 18, 6),
    (2, 19, 7),

    (3, 12, 1),
    (3, 14, 2),
    (3, 16, 3),
    (3, 18, 4),
    (3, 20, 5);

INSERT INTO Workers
    (WorkerID, WorkerFirstName, WorkerLastName, WorkerBalance, WorkerCardID)
VALUES
    (1, "John", "Smith", 500.00, "25111252110228"),
    (2, "Emily", "Johnson", 700.50, "187121523413");


INSERT INTO BUSES
    (BusID, CourseID, StopNumber)
VALUES
    (0, null, null);
