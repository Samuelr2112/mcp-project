MCP Project

Checkpoint #2: CRUD working with FastAPI, PostgreSQL, and Claude

This repository marks the second checkpoint of my MCP project. At this stage, the backend API has been fully extended with CRUD functionality for managing appointments, and it now works seamlessly through Claude thanks to Model Context Protocol (MCP) integration.

✅ What I accomplished
Backend with FastAPI

Implemented a complete CRUD API for appointments:

POST /create_appointment → create a new appointment

GET /list_appointments → list all appointments

PUT /update_appointment/{id} → update an existing appointment

DELETE /delete_appointment/{id} → delete an appointment

Added flexible date parsing so the API accepts ISO 8601 date strings.

Ensured consistent output formatting for appointment dates.

Database with PostgreSQL

PostgreSQL container is fully set up via Docker Compose.

FastAPI correctly creates and persists appointment records.

Database is stable and works across container restarts.

MCP integration with Claude

Updated manifest.json so Claude understands required parameters (customer_name, date, appointment_id).

Verified that Claude can now:

Create appointments by natural language prompts.

List, update, and delete appointments with simple commands.

Tested natural language requests successfully (e.g., “Add an appointment for Emily Gist on September 25th at 11:30 AM”).

Version control

All changes tracked in Git.

Checkpoint #2 commit includes CRUD logic, error handling, and integration with Claude.

🔥 Natural Language Examples

Claude can now interpret natural language and convert it into valid API requests automatically.

Create

“Add an appointment for [Name] on [Date] at [Time]”

“Create an appointment for [Name] on [Date] at [Time]”

List

“Show me all appointments”

“List my scheduled appointments”

“What appointments do I have?”

Update

“Edit the appointment with ID [ID] and change the name to [NewName]”

“Change the appointment ID [ID] to [Date] at [Time]”

“Update appointment ID [ID] so the client is [NewName] and the date is [Date] at [Time]”

Delete

“Delete the appointment with ID [ID]”

“Remove appointment number [ID]”

“Cancel the appointment with ID [ID]”

🌐 Current Status

API runs locally at http://localhost:8000.

PostgreSQL container is connected and persists data.

MCP proxy integration allows Claude to call the API endpoints.

Natural language requests to Claude now create, list, update, and delete appointments successfully.

🚀 Next Steps

Add validation for overlapping appointments.

Expand appointment details (duration, notes, contact info).

Write automated tests with pytest.

Build a simple frontend to manage appointments visually.

Continue refining Claude’s natural language integration with MCP.

✍️ Checkpoint #2 complete.
