Simple playground app for [pact-python](https://github.com/pact-foundation/pact-python/) contract testing.

1. Run pact broker:
```
>> docker-compose up
```

2. Go into postgres container and create pact user role:
```psql
CREATE USER pactbrokeruser WITH PASSWORD 'pactbrokeruser';
CREATE DATABASE pactbroker WITH OWNER pactbrokeruser;
GRANT ALL PRIVILEGES ON DATABASE pactbroker TO pactbrokeruser;
```

3. Now you can enter `http://myuser:mypassword@localhost` to see pact admin page.

4. In `consumer` location run with unique consumer `version_num`:
```
>> pytest --publish-pact <version_num>
```
In these step pact file will be generated and send to broker. Our consumer would be tested
against mocked service.

5. In `provider` location run with unique provider `version_num`:
```
>> pytest --publish-version <version_num>:
```
It would verify our provider against latest pact stored within broker.

6. Checking whether can deploy component (provider / consumer):
```
http://localhost/can-i-deploy?pacticipant=<provider>&version=<version_num>
```
