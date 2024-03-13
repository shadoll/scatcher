# SCATCHER - HTTP Request Catcher

Scatcher is a service designed to intercept and store HTTP requests for debugging and testing purposes. It operates as a middleware that captures incoming HTTP requests, including their method, headers, data, and timestamp.

This service is particularly useful for developers who want to inspect the exact requests being sent to their applications, especially when debugging complex issues related to request handling. It can be easily deployed using Docker, making it a convenient tool for development environments.

## Documentations
Once the service is running, you can navigate to `/doc` or `/redoc` in your web browser to access the full documentation for all supported requests.

## Quick usage examples
The main entry point of the service is the `/` endpoint, which is designed to catch and store all incoming HTTP requests, regardless of the method used (GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD). This allows you to inspect the details of any request sent to this endpoint.

Here's an example of how to make a POST request with JSON data to the service:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://localhost:8000/
```

To retrieve the last caught request, send a GET request to the `/api/__last_request` endpoint.
```bash
curl -X GET http://localhost:8000/api/__last_request
```

If you want to view the history of the last 10 caught requests, send a GET request to the `/api/__history` endpoint. This will return a list of the most recent requests that have been sent to the service.
```bash
curl -X GET http://localhost:8000/api/__history
```

To view a specific request from the history, append the request number to the `/api/__history/` endpoint. For example, to view the 3rd request in the history, you would send a GET request to `/api/__history/3`. Here's how you would do this with curl:
```bash
curl -X GET http://localhost:8000/api/__history/3
```

To clear the history of caught requests, send a GET request to the `/api/__clear` endpoint. This will remove all entries from the history.
```bash
curl -X GET http://localhost:8000/api/__clear
```

## Namespace
The service also supports the use of "namespaces" in your requests. This feature allows you to separate and categorize your request streams. Simply include the namespace in your endpoint path when sending requests. For example, to catch a request under the namespace `test`, you would send your request to `/test`. Similarly, to retrieve the last request or view the history under the test namespace, you would send a GET request to `/api/__last_request/test` or `/api/__history/test`, respectively. This allows for more organized tracking and debugging of different request streams.

For more detailed information and usage instructions, please refer to the full documentation available at the /doc or /redoc endpoints when the service is running.
