# MCP Project
**Checkpoint #2: CRUD Operations with FastAPI & PostgreSQL (Claude MCP on hold)**

This repository represents the second checkpoint of my MCP project. At this stage, the backend API has been fully developed with comprehensive CRUD functionality for appointment management, utilizing FastAPI and PostgreSQL through Docker Compose.

The original plan included Model Context Protocol (MCP) integration with Claude, but due to MCP being in early development with limited documentation, that component is currently **on hold**. The backend is fully operational and can be tested using curl, Postman, or the built-in Swagger UI.

---

## Accomplished Features

### Backend with FastAPI
- Implemented complete CRUD API for appointment management:
  - `POST /create_appointment` - Create a new appointment
  - `GET /list_appointments` - Retrieve all appointments
  - `PUT /update_appointment` - Update an existing appointment
  - `DELETE /delete_appointment` - Delete an appointment
- Added flexible date parsing supporting ISO 8601 date strings
- Ensured consistent output formatting for appointment dates
- Professional error handling and response formatting

### Database with PostgreSQL
- PostgreSQL container fully configured via Docker Compose
- FastAPI correctly creates and persists appointment records
- Database maintains stability across container restarts

### MCP Integration (On Hold)
- Built initial `/mcp/tools` endpoint and tested basic MCP compatibility
- Claude integration was attempted but paused due to insufficient stable documentation and support

### Version Control
- All changes tracked in Git
- Checkpoint #2 commit includes CRUD logic, error handling, and Docker integration

## Getting Started

wsl -d Ubuntu
cd ~/mcp-project
docker-compose up --build -d
docker-compose ps
curl http://localhost:8000/list_appointments
python3 mcp_server.py

## API Endpoints

- **Create Appointment**: `POST /create_appointment`
- **List Appointments**: `GET /list_appointments`
- **Update Appointment**: `PUT /update_appointment`
- **Delete Appointment**: `DELETE /delete_appointment`