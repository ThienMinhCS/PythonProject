IF DB_ID('AirlineBookingDB') IS NULL
BEGIN
CREATE DATABASE AirlineBookingDB;
END
GO

USE AirlineBookingDB;
GO

-- USERS

IF OBJECT_ID('Users', 'U') IS NULL
BEGIN
CREATE TABLE Users
(
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    Phone VARCHAR(20),
    Role VARCHAR(20) NOT NULL CHECK (Role IN ('Customer', 'Admin')) DEFAULT 'Customer',
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    UpdatedAt DATETIME NOT NULL DEFAULT GETDATE()
);
END
GO

-- AIRPORTS

IF OBJECT_ID('Airports', 'U') IS NULL
BEGIN
CREATE TABLE Airports
(
    AirportID INT IDENTITY(1,1) PRIMARY KEY,
    AirportCode VARCHAR(10) NOT NULL UNIQUE,
    AirportName NVARCHAR(150) NOT NULL,
    City NVARCHAR(100) NOT NULL,
    Country NVARCHAR(100) NOT NULL
);
END
GO

-- AIRCRAFTS

IF OBJECT_ID('Aircrafts', 'U') IS NULL
BEGIN
CREATE TABLE Aircrafts
(
    AircraftID INT IDENTITY(1,1) PRIMARY KEY,
    AircraftCode VARCHAR(20) NOT NULL UNIQUE,
    Model NVARCHAR(100) NOT NULL,
    Manufacturer NVARCHAR(100),
    TotalSeats INT NOT NULL
);
END
GO

-- FLIGHTS

IF OBJECT_ID('Flights', 'U') IS NULL
BEGIN
CREATE TABLE Flights
(
    FlightID INT IDENTITY(1,1) PRIMARY KEY,
    FlightNumber VARCHAR(20) NOT NULL UNIQUE,
    AircraftID INT NOT NULL,
    DepartureAirportID INT NOT NULL,
    ArrivalAirportID INT NOT NULL,
    DepartureTime DATETIME NOT NULL,
    ArrivalTime DATETIME NOT NULL,
    BasePrice DECIMAL(12,2) NOT NULL,
    Status VARCHAR(30) NOT NULL CHECK (Status IN ('Scheduled', 'Delayed', 'Cancelled','Completed')) DEFAULT 'Scheduled',
    CONSTRAINT FK_Flights_Aircrafts
        FOREIGN KEY (AircraftID)
        REFERENCES Aircrafts(AircraftID),
    CONSTRAINT FK_Flights_DepartureAirport
        FOREIGN KEY (DepartureAirportID)
        REFERENCES Airports(AirportID),
    CONSTRAINT FK_Flights_ArrivalAirport
        FOREIGN KEY (ArrivalAirportID)
        REFERENCES Airports(AirportID)
);
END
GO

-- SEATCLASSES

IF OBJECT_ID('SeatClasses', 'U') IS NULL
BEGIN
CREATE TABLE SeatClasses
(
    ClassID INT IDENTITY(1,1) PRIMARY KEY,
    ClassName NVARCHAR(50) NOT NULL,
    Description NVARCHAR(255)
);
END
GO

-- FLIGHTSEATS

IF OBJECT_ID('FlightSeats', 'U') IS NULL
BEGIN
CREATE TABLE FlightSeats
(
    SeatID INT IDENTITY(1,1) PRIMARY KEY,
    FlightID INT NOT NULL,
    ClassID INT NOT NULL,
    SeatNumber VARCHAR(10) NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'Available',
    CONSTRAINT FK_FlightSeats_Flights
        FOREIGN KEY (FlightID)
        REFERENCES Flights(FlightID),
    CONSTRAINT FK_FlightSeats_SeatClasses
        FOREIGN KEY (ClassID)
        REFERENCES SeatClasses(ClassID)
);
END
GO

-- PROMOTIONS

IF OBJECT_ID('Promotions', 'U') IS NULL
BEGIN
CREATE TABLE Promotions
(
    PromotionID INT IDENTITY(1,1) PRIMARY KEY,
    Code VARCHAR(50) NOT NULL UNIQUE,
    Description NVARCHAR(255),
    DiscountPercent DECIMAL(5,2),
    StartDate DATETIME,
    EndDate DATETIME,
    Quantity INT DEFAULT 0,
    Status VARCHAR(20) CHECK (Status IN ('Active', 'Inactive')) DEFAULT 'Active'
);
END
GO

-- BOOKINGS

IF OBJECT_ID('Bookings', 'U') IS NULL
BEGIN
CREATE TABLE Bookings
(
    BookingID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL,
    PromotionID INT NULL,
    BookingDate DATETIME NOT NULL DEFAULT GETDATE(),
    TotalAmount DECIMAL(12,2) NOT NULL,
    Status VARCHAR(20) NOT NULL CHECK (Status IN ('Pending', 'Confirmed', 'Cancelled')) DEFAULT 'Pending',
    CONSTRAINT FK_Bookings_Users
        FOREIGN KEY (UserID)
        REFERENCES Users(UserID),
    CONSTRAINT FK_Bookings_Promotions
        FOREIGN KEY (PromotionID)
        REFERENCES Promotions(PromotionID)
);
END
GO

-- PASSENGERS

IF OBJECT_ID('Passengers', 'U') IS NULL
BEGIN
CREATE TABLE Passengers
(
PassengerID INT IDENTITY(1,1) PRIMARY KEY,
    BookingID INT NOT NULL,
    FullName NVARCHAR(100) NOT NULL,
    DateOfBirth DATE,
    Gender NVARCHAR(10),
    Nationality NVARCHAR(100),
    DocumentType VARCHAR(20),
    DocumentNumber VARCHAR(50),
    DocumentExpiryDate DATE,
    CONSTRAINT FK_Passengers_Bookings
        FOREIGN KEY (BookingID)
        REFERENCES Bookings(BookingID)
);
END
GO

-- PASSENGERBAGGAGES

IF OBJECT_ID('PassengerBaggages', 'U') IS NULL
BEGIN
CREATE TABLE PassengerBaggages
(
PassengerBaggageID INT IDENTITY(1,1) PRIMARY KEY,
    PassengerID INT NOT NULL,
    Weight INT NOT NULL,
    Price DECIMAL(12,2) NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_PassengerBaggages_Passengers
        FOREIGN KEY (PassengerID)
        REFERENCES Passengers(PassengerID)
);
END
GO

-- PAYMENTS

IF OBJECT_ID('Payments', 'U') IS NULL
BEGIN
CREATE TABLE Payments
(
PaymentID INT IDENTITY(1,1) PRIMARY KEY,
    BookingID INT NOT NULL,
    Amount DECIMAL(12,2) NOT NULL,
    PaymentMethod VARCHAR(50),
    PaymentStatus VARCHAR(20) NOT NULL DEFAULT 'Pending',
    PaidAt DATETIME,
    CONSTRAINT FK_Payments_Bookings
        FOREIGN KEY (BookingID)
        REFERENCES Bookings(BookingID)
);
END
GO

-- TICKETS

IF OBJECT_ID('Tickets', 'U') IS NULL
BEGIN
CREATE TABLE Tickets
(
    TicketID INT IDENTITY(1,1) PRIMARY KEY,
    BookingID INT NOT NULL,
    PassengerID INT NOT NULL,
    FlightID INT NOT NULL,
    SeatID INT NOT NULL,
    Price DECIMAL(12,2) NOT NULL,
    TicketStatus VARCHAR(20) NOT NULL DEFAULT 'Active',
    CONSTRAINT FK_Tickets_Bookings
        FOREIGN KEY (BookingID)
        REFERENCES Bookings(BookingID),
    CONSTRAINT FK_Tickets_Passengers
        FOREIGN KEY (PassengerID)
        REFERENCES Passengers(PassengerID),
    CONSTRAINT FK_Tickets_Flights
        FOREIGN KEY (FlightID)
        REFERENCES Flights(FlightID),
    CONSTRAINT FK_Tickets_FlightSeats
        FOREIGN KEY (SeatID)
        REFERENCES FlightSeats(SeatID)
);
END
GO