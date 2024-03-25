# Project2_EC530

## Health Monitoring API

This API provides a comprehensive solution for managing health data, including user registrations, device management, health measurements, appointment scheduling, and messaging services. With MongoDB integration, this API ensures scalable and persistent data storage, making it suitable for production environments.

### Prerequisites
- Python 3.
- Flask
- PyMongo
- MongoDB

### Usage
The Health Monitoring API supports the following endpoints:

POST /users/add: Add a new user.
POST /users/<user_id>/assignRole: Assign roles to a user.
POST /devices/register: Register a new device.
POST /patients/<patient_id>/measurements: Submit a health measurement for a patient.
POST /patients/<patient_id>/appointments/book: Book a new appointment for a patient.
GET /patients/<patient_id>/appointments: View appointments for a patient.
POST /chat/<patient_id>: Post a message to a patient's chat.
GET /chat/<patient_id>: Get the chat history for a patient.


