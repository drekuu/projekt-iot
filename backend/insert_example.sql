INSERT INTO Courses
    (CourseID, CourseName)
VALUES
    (1, "LongCourse"),
    (2, "MediumLengthCourse"),
    (2, "ShortCourse");


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
    (1, "John", "Smith", 500.00, "W12345"),
    (2, "Emily", "Johnson", 700.50, "W67890"),
    (3, "Daniel", "Davis", 450.25, "W23456"),
    (4, "Jessica", "Williams", 600.75, "W78901"),
    (5, "Michael", "Jones", 550.20, "W34567"),
    (6, "Olivia", "Brown", 800.00, "W89012"),
    (7, "William", "Miller", 350.30, "W45678"),
    (8, "Sophia", "Anderson", 900.50, "W90123"),
    (9, "Christopher", "Taylor", 480.90, "W56789"),
    (10, "Ava", "Martinez", 620.40, "W01234"),
    (11, "Ryan", "Garcia", 550.75, "W12340"),
    (12, "Emma", "Lopez", 720.60, "W23450"),
    (13, "Matthew", "Perez", 420.25, "W34560"),
    (14, "Isabella", "Hill", 670.80, "W45670"),
    (15, "Andrew", "Turner", 580.30, "W56780"),
    (16, "Mia", "Clark", 750.90, "W67890"),
    (17, "Ethan", "Ward", 400.50, "W78901"),
    (18, "Amelia", "Fisher", 530.40, "W89012"),
    (19, "Logan", "Baker", 680.25, "W90123"),
    (20, "Grace", "Cooper", 510.70, "W01234");

INSERT INTO BUSES
    (BusID, CourseID, StopsInAscendingOrder, StopNumber)
VALUES
    (1, 1, 1, 3),
    (2, 2, 1, 4),
    (3, 1, 0, 5),
    (4, null, null, null),
    (5, 3, 1, 4),
    (6, 3, 1, 8),
    (7, 2, 0, 1),
    (8, 3, 0, 11),
    (9, 2, 0, 7),
    (10, 3, 0, 2);

-- INSERT INTO CurrentRides
--     (RideID, WorkerID, StopsTraveled)
-- VALUES
--     ();