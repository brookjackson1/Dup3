-- Database Schema for Animal Adoption Site
-- Run this file to create the required database structure

-- Create animals table
CREATE TABLE animals (
    animal_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(50) NOT NULL,
    breed VARCHAR(100),
    age INT NOT NULL,
    gender ENUM('Male', 'Female') NOT NULL,
    size ENUM('Small', 'Medium', 'Large') NOT NULL,
    color VARCHAR(50),
    description TEXT,
    adoption_status ENUM('Available', 'Pending', 'Adopted') DEFAULT 'Available',
    medical_notes TEXT,
    arrival_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Add indexes for common queries
CREATE INDEX idx_animals_species ON animals (species);
CREATE INDEX idx_animals_status ON animals (adoption_status);
CREATE INDEX idx_animals_size ON animals (size);