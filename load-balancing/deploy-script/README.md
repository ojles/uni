# Deploy Script

## Setup
This setup assumes you already have docker-compose, java and maven installed.


1. Build [compute](compute) project:

```
cd compute
mvn clean package
```

2. Start back-end:

```
cd deploy-scripts
docker-compose up -d
```

3. Start [web-client](web-client):

```
cd web-client
npm start
```


## Play
* open web-client at [http://localhost:3000](http://localhost:3000). Create a user, login and create tasks
* open rabbitmq dashboard at [http://localhost](http://localhost)<br>
_Username:_ rabbitmq<br>
_Password:_ rabbitmq
