ALTER SYSTEM SET listen_addresses = '*' ;
ALTER SYSTEM SET shared_buffers = '512MB' ;
ALTER SYSTEM SET max_connections = 400 ;
ALTER SYSTEM SET log_min_messages = FATAL ;
ALTER SYSTEM SET commit_delay = 5;
ALTER SYSTEM SET commit_siblings = 100;
ALTER SYSTEM SET checkpoint_timeout = 600;