ALTER SYSTEM SET listen_addresses = '*' ;
ALTER SYSTEM SET shared_buffers = '512MB' ;
ALTER SYSTEM SET max_connections = 300 ;
ALTER SYSTEM SET log_min_messages = FATAL ;
ALTER SYSTEM SET checkpoint_timeout = 600;