-- ==========================================================
-- HeritageVerse Database Schema (MySQL)
-- AI-Powered Heritage Preservation Intelligence Platform
-- Pipeline: DETECT -> ANALYSE -> SCORE -> PRIORITIZE -> ALERT -> ACT -> TRACK
-- ==========================================================

CREATE DATABASE IF NOT EXISTS heritageverse CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE heritageverse;

-- 1. Users Table (Citizens, Conservation Officers, Administrators)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_email (email),
    INDEX idx_user_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. States / Regions Table
CREATE TABLE IF NOT EXISTS states (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    map_identifier VARCHAR(10) NOT NULL UNIQUE, -- e.g., RJ, UP, MH, DL
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_state_code (map_identifier)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Monitored Heritage Sites Table
CREATE TABLE IF NOT EXISTS heritage_sites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    historical_period VARCHAR(100),
    heritage_category VARCHAR(100) DEFAULT 'Monuments & Forts',
    description TEXT NOT NULL,
    cultural_significance TEXT,
    architecture TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    preservation_status ENUM('Well Preserved', 'Minor Restoration Required', 'Major Conservation Needed', 'Under Active Restoration', 'Critical') DEFAULT 'Well Preserved',
    current_health_score INT DEFAULT 82, -- 0-100
    risk_level ENUM('Low', 'Moderate', 'High', 'Critical') DEFAULT 'Low',
    carrying_capacity_daily INT DEFAULT 5000,
    image_url VARCHAR(255),
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES states(id) ON DELETE CASCADE,
    INDEX idx_site_state (state_id),
    INDEX idx_site_name (name),
    INDEX idx_site_health (current_health_score),
    INDEX idx_site_risk (risk_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Heritage Images Gallery Table
CREATE TABLE IF NOT EXISTS heritage_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    heritage_site_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    caption VARCHAR(255),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (heritage_site_id) REFERENCES heritage_sites(id) ON DELETE CASCADE,
    INDEX idx_img_site (heritage_site_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Citizen Heritage Watch Reports Table (with AI Preliminary Analysis)
CREATE TABLE IF NOT EXISTS heritage_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_uid VARCHAR(32) NOT NULL UNIQUE, -- e.g., HV-2026-X9Y2Z8
    user_id INT NULL,
    heritage_site_id INT NOT NULL,
    issue_type ENUM(
        'Vandalism',
        'Structural Damage',
        'Encroachment',
        'Illegal Construction',
        'Pollution',
        'Garbage',
        'Fire Damage',
        'Flood/Water Damage',
        'Other'
    ) NOT NULL,
    description TEXT NOT NULL,
    incident_date DATE NOT NULL,
    location VARCHAR(200) NOT NULL,
    severity ENUM('Low', 'Moderate', 'High', 'Critical') DEFAULT 'Moderate',
    status ENUM(
        'Submitted',
        'Under Review',
        'Verified',
        'Action Required',
        'Resolved',
        'Rejected'
    ) DEFAULT 'Submitted',
    admin_remarks TEXT NULL,
    ai_category_detected VARCHAR(100),
    ai_severity_estimated VARCHAR(50),
    ai_confidence_score INT DEFAULT 85,
    ai_damage_signs TEXT,
    ai_urgency VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (heritage_site_id) REFERENCES heritage_sites(id) ON DELETE CASCADE,
    INDEX idx_rep_uid (report_uid),
    INDEX idx_rep_status (status),
    INDEX idx_rep_severity (severity),
    INDEX idx_rep_site (heritage_site_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Report Photographic Evidence Table
CREATE TABLE IF NOT EXISTS report_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    file_size_bytes INT,
    mime_type VARCHAR(50),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES heritage_reports(id) ON DELETE CASCADE,
    INDEX idx_repimg_report (report_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Multi-Hazard Risk Assessments Table
CREATE TABLE IF NOT EXISTS risk_assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    heritage_site_id INT NOT NULL,
    structural_risk ENUM('Low', 'Moderate', 'High', 'Critical') DEFAULT 'Low',
    structural_score INT DEFAULT 85,
    encroachment_risk ENUM('Low', 'Moderate', 'High', 'Critical') DEFAULT 'Low',
    encroachment_score INT DEFAULT 90,
    flood_risk ENUM('Low', 'Moderate', 'High', 'Critical') DEFAULT 'Low',
    fire_risk ENUM('Low', 'Moderate', 'High', 'Critical') DEFAULT 'Low',
    earthquake_risk ENUM('Low', 'Moderate', 'High', 'Critical') DEFAULT 'Low',
    weather_risk ENUM('Low', 'Moderate', 'High', 'Critical') DEFAULT 'Low',
    disaster_score INT DEFAULT 82,
    environmental_score INT DEFAULT 85,
    tourist_pressure_score INT DEFAULT 80,
    overall_health_score INT DEFAULT 84,
    assessed_by VARCHAR(100) DEFAULT 'Preservation Intelligence Engine',
    last_assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (heritage_site_id) REFERENCES heritage_sites(id) ON DELETE CASCADE,
    INDEX idx_risk_site (heritage_site_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Environmental Impact & Sensor Data Table
CREATE TABLE IF NOT EXISTS environmental_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    heritage_site_id INT NOT NULL,
    temperature_c FLOAT DEFAULT 28.5,
    humidity_pct FLOAT DEFAULT 55.0,
    rainfall_mm FLOAT DEFAULT 12.0,
    air_quality_aqi INT DEFAULT 95,
    aqi_category VARCHAR(50) DEFAULT 'Moderate',
    flood_water_level_m FLOAT DEFAULT 0.2,
    exposure_risk_status ENUM('Normal', 'Moderate Risk', 'High Risk', 'Critical Warning') DEFAULT 'Normal',
    data_source ENUM('LIVE_API', 'DEMO_DATA', 'USER_ENTERED') DEFAULT 'DEMO_DATA',
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (heritage_site_id) REFERENCES heritage_sites(id) ON DELETE CASCADE,
    INDEX idx_env_site (heritage_site_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Tourist Carrying Capacity & Crowd Pressure Table
CREATE TABLE IF NOT EXISTS tourist_pressure (
    id INT AUTO_INCREMENT PRIMARY KEY,
    heritage_site_id INT NOT NULL,
    daily_visitors INT DEFAULT 2400,
    monthly_visitors INT DEFAULT 72000,
    carrying_capacity INT DEFAULT 5000,
    occupancy_ratio FLOAT DEFAULT 0.48,
    pressure_level ENUM('Low', 'Moderate', 'High', 'Critical') DEFAULT 'Moderate',
    trend ENUM('Rising', 'Stable', 'Declining') DEFAULT 'Stable',
    recorded_date DATE NOT NULL,
    FOREIGN KEY (heritage_site_id) REFERENCES heritage_sites(id) ON DELETE CASCADE,
    INDEX idx_tourist_site (heritage_site_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. Encroachment & Protected Buffer Zone Observations Table
CREATE TABLE IF NOT EXISTS encroachment_observations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    heritage_site_id INT NOT NULL,
    monitored_zone VARCHAR(150) NOT NULL,
    baseline_image_url VARCHAR(255),
    baseline_date DATE NOT NULL,
    latest_image_url VARCHAR(255),
    latest_date DATE NOT NULL,
    detected_change TEXT NOT NULL,
    change_area_sqm FLOAT DEFAULT 120.0,
    risk_level ENUM('Low', 'Moderate', 'High', 'Critical') DEFAULT 'Moderate',
    confidence_pct INT DEFAULT 88,
    verified_by_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (heritage_site_id) REFERENCES heritage_sites(id) ON DELETE CASCADE,
    INDEX idx_enc_site (heritage_site_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. Historical Condition Timeline Table
CREATE TABLE IF NOT EXISTS condition_timeline (
    id INT AUTO_INCREMENT PRIMARY KEY,
    heritage_site_id INT NOT NULL,
    year INT NOT NULL,
    period_label VARCHAR(50),
    condition_status ENUM('Good', 'Attention Required', 'High Risk', 'Critical') DEFAULT 'Good',
    health_score INT DEFAULT 85,
    event_type ENUM(
        'Report Logged',
        'Damage Verified',
        'Environmental Alert',
        'Encroachment Detected',
        'Disaster Event',
        'Admin Action',
        'Restoration Completed'
    ) NOT NULL,
    summary TEXT NOT NULL,
    action_taken TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (heritage_site_id) REFERENCES heritage_sites(id) ON DELETE CASCADE,
    INDEX idx_timeline_site (heritage_site_id),
    INDEX idx_timeline_year (year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 12. Early Warning Alert Engine Table
CREATE TABLE IF NOT EXISTS alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alert_uid VARCHAR(32) NOT NULL UNIQUE,
    heritage_site_id INT NOT NULL,
    alert_type ENUM(
        'Structural Alert',
        'Citizen Surge Alert',
        'Encroachment Alert',
        'Disaster Risk Alert',
        'Environmental Warning',
        'Health Score Drop'
    ) NOT NULL,
    priority ENUM('LOW', 'MODERATE', 'HIGH', 'CRITICAL') DEFAULT 'MODERATE',
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    trigger_reason TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    status ENUM('Active', 'Acknowledged', 'Assigned', 'Resolved') DEFAULT 'Active',
    assigned_to VARCHAR(150),
    action_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    FOREIGN KEY (heritage_site_id) REFERENCES heritage_sites(id) ON DELETE CASCADE,
    INDEX idx_alert_site (heritage_site_id),
    INDEX idx_alert_priority (priority),
    INDEX idx_alert_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 13. Admin Preservation Action Audit Log
CREATE TABLE IF NOT EXISTS admin_actions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action_type VARCHAR(100) NOT NULL,
    target_entity VARCHAR(50) NOT NULL,
    target_id INT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
