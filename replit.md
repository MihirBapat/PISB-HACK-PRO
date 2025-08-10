# Multi-Clinic Doctor Appointment System

## Overview

This is a full-stack web application for managing doctor appointments across multiple clinics. The system allows patients to register, select clinics, choose doctors, and book available time slots. It includes separate interfaces for patients, doctors, and administrators, with comprehensive appointment management capabilities.

**Status**: Fully functional and deployed. All core features implemented and tested.

## Recent Changes (July 31, 2025)

✅ **Complete Implementation**: All core functionality built and working
✅ **Authentication System**: Role-based access with separate dashboards
✅ **Booking System**: 3-step booking flow with double-booking prevention  
✅ **Admin Panel**: Full CRUD operations for system management
✅ **Doctor Dashboard**: Schedule and appointment management
✅ **UI/UX**: Professional medical-themed design with Bootstrap
✅ **JavaScript Fixes**: Resolved console errors and form validation
✅ **Database**: PostgreSQL integration with proper relationships
✅ **Local Development**: Complete setup with circular import resolution

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Technology**: Pure HTML, CSS, and JavaScript (no frontend frameworks)
- **UI Framework**: Bootstrap 5.3.0 for responsive design
- **Icons**: Font Awesome 6.4.0 for consistent iconography
- **Communication**: RESTful API calls using fetch/AJAX
- **Templates**: Jinja2 templating engine with Flask

### Backend Architecture
- **Framework**: Flask with modular Blueprint structure
- **Architecture Pattern**: MVC (Model-View-Controller)
- **Blueprints**: Separate blueprints for auth, booking, admin, and doctor functionality
- **Session Management**: Flask sessions for user authentication
- **Password Security**: Werkzeug for password hashing and verification

### Database Architecture
- **Primary Database**: SQLite (with MySQL compatibility)
- **ORM**: SQLAlchemy with DeclarativeBase
- **Connection Pool**: Configured with recycling and pre-ping for reliability
- **Database URL**: Environment-configurable via DATABASE_URL

## Key Components

### Models (models.py)
- **User**: Handles patients, doctors, and admins with role-based access
- **Clinic**: Manages clinic information and relationships
- **Doctor**: Links users to clinics with professional details
- **TimeSlot**: Manages available appointment slots
- **Appointment**: Tracks bookings with status management

### Route Blueprints
1. **Authentication (auth.py)**: Login, registration, and session management
2. **Booking (booking.py)**: Patient appointment booking flow
3. **Admin (admin.py)**: Administrative functions for managing the system
4. **Doctor (doctor.py)**: Doctor dashboard and appointment management

### Frontend Components
- **Base Template**: Consistent navigation and layout structure
- **Dashboard Views**: Role-specific interfaces for different user types
- **Booking Flow**: Multi-step appointment booking process
- **Form Validation**: Client-side and server-side validation

## Data Flow

### Patient Booking Flow
1. Patient selects a clinic from available options
2. System displays doctors associated with selected clinic
3. Patient chooses a doctor to see available time slots
4. Patient selects preferred time slot and confirms booking
5. System prevents double-booking through database constraints

### Authentication Flow
1. Users register with role specification (patient/doctor/admin)
2. Login validates credentials and establishes session
3. Role-based access control redirects to appropriate dashboard
4. Session management maintains user state across requests

### Admin Management Flow
1. Admins can create and manage clinics
2. Doctor accounts can be created and assigned to clinics
3. Time slots can be managed for doctors
4. Appointment oversight and management capabilities

## External Dependencies

### Python Packages
- **Flask**: Web framework and core functionality
- **Flask-SQLAlchemy**: Database ORM and management
- **Werkzeug**: Security utilities and WSGI support
- **ProxyFix**: Production deployment support

### Frontend Libraries
- **Bootstrap 5.3.0**: CSS framework for responsive design
- **Font Awesome 6.4.0**: Icon library for UI elements
- **Custom CSS**: Medical-themed styling with blue/white color scheme

### Database
- **SQLite**: Default database for development
- **MySQL**: Production-ready alternative (configurable)

## Deployment Strategy

### Environment Configuration
- **Session Secret**: Configurable via SESSION_SECRET environment variable
- **Database URL**: Flexible database connection via DATABASE_URL
- **Debug Mode**: Controlled through Flask configuration

### Production Considerations
- **WSGI Support**: ProxyFix middleware for reverse proxy deployment
- **Connection Pooling**: Database connection management with recycling
- **Security**: Secure session management and password hashing

### Development Setup
- **Host**: 0.0.0.0 for container compatibility
- **Port**: 5000 (standard Flask development port)
- **Debug Mode**: Enabled for development with hot reloading

### Key Features
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Role-Based Access**: Separate interfaces for patients, doctors, and admins
- **Booking Protection**: Prevents double-booking of time slots
- **Real-time Validation**: Client-side and server-side form validation
- **Session Management**: Secure user authentication and state management
- **Modular Structure**: Clean separation of concerns with Flask Blueprints