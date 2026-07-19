"""
Vehicle Service Management API

1. Request-Response Cycle

Browser Request:
GET /api/vehicles/

Request Flow:

Browser
   ↓
URL Router
   ↓
View Function
   ↓
Model (Database Query)
   ↓
Response
   ↓
Browser

Example:

User requests:

GET /api/vehicles/

1. Django URL router receives the request.
2. Router identifies the matching URL pattern.
3. The request is forwarded to a view.
4. The view interacts with the model.
5. The model queries MySQL/SQLite database.
6. Data is returned to the view.
7. The view sends HttpResponse or JSON response.
8. Browser displays the result.

------------------------------------------------

2. Middleware Position

Browser
   ↓
Middleware
   ↓
URL Router
   ↓
View
   ↓
Response
   ↓
Middleware
   ↓
Browser

Examples of Django Middleware:

SecurityMiddleware
- Provides security enhancements.
- Protects against vulnerabilities.

SessionMiddleware
- Manages user sessions.
- Stores session data.

------------------------------------------------

3. WSGI vs ASGI

WSGI:
- Handles synchronous requests.
- Processes one request at a time.
- Suitable for traditional web applications.

ASGI:
- Handles asynchronous requests.
- Supports WebSockets and real-time communication.
- Suitable for chat applications and live notifications.

Django uses WSGI by default.

Switch to ASGI when:
- Building chat applications.
- Using WebSockets.
- Handling high concurrency.

------------------------------------------------

4. MVC vs MVT

MVC

Model      -> Data Layer
View       -> User Interface
Controller -> Business Logic

Django MVT

Model      -> Model
View       -> Controller
Template   -> View

Django View acts like the Controller in MVC.
"""