# MCP Project  
**Checkpoint #2: CRUD working with FastAPI & PostgreSQL (Claude MCP on hold)**  

This repository marks the second checkpoint of my MCP project. At this stage, the backend API has been fully extended with CRUD functionality for managing appointments, running with FastAPI and PostgreSQL via Docker Compose.  

The original plan included Model Context Protocol (MCP) integration with Claude, but since MCP is still very new and documentation is limited, that part of the project is currently **on hold**. The backend is fully functional and can be tested with `curl`, Postman, or the built-in Swagger UI.  

---

## ✅ What I accomplished  

### Backend with FastAPI  
- Implemented a complete CRUD API for appointments:  
  - `POST /create_appointment` → create a new appointment  
  - `POST /list_appointments` → list all appointments  
  - `POST /update_appointment` → update an existing appointment  
  - `POST /delete_appointment` → delete an appointment  
- Added flexible date parsing so the API accepts ISO 8601 date strings.  
- Ensured consistent output formatting for appointment dates.  

### Database with PostgreSQL  
- PostgreSQL container is fully set up via Docker Compose.  
- FastAPI correctly creates and persists appointment records.  
- Database is stable and works across container restarts.  

### MCP (On Hold)  
- Built an initial `/mcp/tools` endpoint and tested basic MCP compatibility.  
- Integration with Claude was attempted, but this part is paused due to lack of stable documentation and support.  

### Version Control  
- All changes tracked in Git.  
- Checkpoint #2 commit includes CRUD logic, error handling, and Docker integration.  
