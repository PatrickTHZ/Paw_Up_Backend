-- User table
CREATE TABLE "User" (
  UserID SERIAL PRIMARY KEY,
  F_Name VARCHAR(50),
  L_Name VARCHAR(50),
  Street VARCHAR(100),
  Suburb VARCHAR(50),
  Postcode VARCHAR(10),
  State VARCHAR(50),
  Phone VARCHAR(20),
  Email VARCHAR(100) UNIQUE,
  DOB DATE,
  Registration_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Authentication table
CREATE TABLE Authentication (
  UserID INT PRIMARY KEY,
  Email VARCHAR(100) UNIQUE NOT NULL,
  Password VARCHAR(255) NOT NULL,
  FOREIGN KEY (UserID) REFERENCES "User" (UserID) ON DELETE CASCADE
);

-- PetType table
CREATE TABLE PetType (
  PetTypeID SERIAL PRIMARY KEY,
  PetType VARCHAR(50)
);

-- Gender table
CREATE TABLE Gender (
  GenderID SERIAL PRIMARY KEY,
  Gender VARCHAR(20)
);

-- Insurance Provider table
CREATE TABLE InsuranceProvider (
  CompanyID SERIAL PRIMARY KEY,
  Company_Name VARCHAR(100)
);

-- Insurance table
CREATE TABLE Insurance (
  InsuranceID SERIAL PRIMARY KEY,
  CompanyID INT,
  Insurance_Type VARCHAR(50),
  Product_Name VARCHAR(100),
  isActive BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (CompanyID) REFERENCES InsuranceProvider (CompanyID)
);

-- Pet table
CREATE TABLE Pet (
  PetID SERIAL PRIMARY KEY,
  UserID INT,
  InsuranceID INT,
  GenderID INT,
  PetTypeID INT,
  Pet_Name VARCHAR(50),
  Age INT,
  withInsurance BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (UserID) REFERENCES "User" (UserID) ON DELETE SET NULL,
  FOREIGN KEY (InsuranceID) REFERENCES Insurance (InsuranceID) ON DELETE SET NULL,
  FOREIGN KEY (GenderID) REFERENCES Gender (GenderID),
  FOREIGN KEY (PetTypeID) REFERENCES PetType (PetTypeID)
);

-- Chat table
CREATE TABLE Chat (
  chatID SERIAL PRIMARY KEY,
  UserID INT,
  Topic VARCHAR(255),
  createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (UserID) REFERENCES "User" (UserID) ON DELETE CASCADE
);

-- Message table
CREATE TABLE Message (
  messageID SERIAL PRIMARY KEY,
  ChatID INT,
  Message_Text TEXT,
  Role VARCHAR(10) CHECK (Role IN ('user', 'assistant')),
  timeSent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (ChatID) REFERENCES Chat (chatID) ON DELETE CASCADE
);
