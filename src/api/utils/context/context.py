from contextvars import ContextVar

# Define a ContextVar for the request_id
request_id_var = ContextVar("request_id", default=None)