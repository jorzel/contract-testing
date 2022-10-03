Simple playoground app for pact python contract testing.

1.
```
>> docker-compose up
```

2. Go into postgres container
```psql
CREATE USER pactbrokeruser WITH PASSWORD 'pactbrokeruser';
CREATE DATABASE pactbroker WITH OWNER pactbrokeruser;
GRANT ALL PRIVILEGES ON DATABASE pactbroker TO pactbrokeruser;
```

3. Enter `http://myuser:mypassword@localhost` to see pact admin page
