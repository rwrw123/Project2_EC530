# Project2_EC530
Sample codes for APIs

1. Data Reading API

Purpose:
To retrieve health metrics and patient data from the system.

Endpoints:
 
  Get Patient Data
 
 '/api/patient/{patientId}'
  Method: GET
  Description: Retrieves patient demographics, health metrics, and historical health data.
  Parameters: patientId (path), fromDate (query, optional), toDate (query, optional)
  Response: Patient demographics, list of health metrics (e.g., heart rate, blood pressure, glucose levels), each with timestamps.
 
  Get Real-Time Health Metrics
  Endpoint: '/api/metrics/realtime/{patientId}'
  Method: GET
  Description: Fetches real-time health metrics for a specific patient.
  Parameters: patientId (path)
  Response: Current health metrics with timestamp.
  
  Get Historical Health Data
  Endpoint: '/api/metrics/history/{patientId}'
  Method: GET
  Description: Retrieves historical health data for analysis and reporting.
  Parameters: patientId (path), metricType (query), fromDate (query), toDate (query)
  Response: Historical health metrics specified by type and date range.

2. Device Interface API
Purpose:
To manage and interact with health monitoring devices.

Endpoints:
Register Device

Endpoint: '/api/device/register'
Method: POST
Description: Registers a new device to the system.
Body: Device type, model, serial number, patientId it's assigned to.
Response: Registration status, device ID.

Update Device Configuration
Endpoint: '/api/device/{deviceId}/configure'
Method: POST
Description: Updates configuration settings for a device.
Parameters: deviceId (path)
Body: Configuration parameters (e.g., measurement intervals, alerts thresholds).
Response: Success or failure status.

Fetch Device Status
Endpoint: '/api/device/{deviceId}/status'
Method: GET
Description: Retrieves the current status and configuration of a device.
Parameters: deviceId (path)
Response: Current status, configuration settings, last active time.

Send Command to Device
Endpoint: '/api/device/{deviceId}/command'
Method: POST
Description: Sends a command to a device (e.g., start/stop measurement, calibrate).
Parameters: deviceId (path)
Body: Command type and parameters.
Response: Command execution status.
