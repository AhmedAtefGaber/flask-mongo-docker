# flask-mongo-docker
# Our task is to create two docker containers:
##### container1 - should be able to accept a string through http
##### container2 - hosts a simple mongodb database
---
Once container1 receives a string (e.g. “foo”), it will append something to it (e.g. “bar”), and will then send the original string as well as the modified one (“foo” + “foobar”) to container2. 
Both strings are then saved in the database of container2 together with a timestamp.
Ideally the two containers are not on the same host, but are instead linked through a private network which they use for communication.
---
### So, Please follow the below steps:
1. Let's create a Swarm cluster of the two docker hosts docker-1 and docker-2. 
so, to Initialize a swarm and make docker-1 as the master node.
```
$ docker swarm init
```
<img src="images/swarm-init.png width=" >

2. Copy the join command and run it on docker-2. So, it will join swarm as a worker node.
```
$ docker swarm join --token SWMTKN-1-4f9o5i2dopwjzazup7f6iwtpqkcx0ijgzpc1xgra32au384cuf-9y4opeqgjo4w20f5hksf8duej 172.31.0.212:2377
```
3. We need to add a tag for each node : 
```
$ docker node update --label-add stage=app docker-1
$ docker node update --label-add stage=db docker-2
```
4. Create an Overlay docker Network to span over the two nodes: 
```
$ docker network create -d overlay overnet
```
5. build the web application docker image: 
```
$ docker build -t app-py .
```
<img src="images/docker-build-app.png" >

6. Push this image to your docker registry on [Docker hub](https://hub.docker.com). So, the docker images can be accessed from both nodes not locally only.
* first, we need to login to our Docker registry
```
$ docker login -u ahmedatefosman
```
* Then, create a repository on [Docker hub](https://hub.docker.com) called flask-mongo-docker.
you can make it a private repository if you don't want to make it publicly accessible.
* Then, tag our application image with our docker hub repository.
```
$ docker tag  app-py:latest ahmedatefosman/flask-mongo-docker/app-py
```
* Then push it to docker hub.
```
$ docker push ahmedatefosman/flask-mongo-docker:app-py
```
7. Now, Let's Run a docker service from this image on docker-1 node: 
```
$ docker service create --name app-svc --network overnet --constraint 'node.labels.stage==app'  --replicas 1 -p 80:5000  ahmedatefosman/flask-mongo-docker:app-py
```
8. Moving to the mongodb part, Let's build the mongodb docker image: 
```
$ docker build -t app-db .
```
9. Push this image to the docker registry, same as app-py.
```
$ docker tag  app-py:latest ahmedatefosman/flask-mongo-docker/app-db
$ docker push ahmedatefosman/flask-mongo-docker:app-db
```
10. Run a mongodb docker service from this image on docker-2 node:  
```
$ docker service create --name db-svc --network overnet  --replicas 1 --constraint 'node.labels.stage==db'  ahmedatefosman/flask-mongo-docker:app-db
```
11. Let's curl on the web application or from your browser: 
```
$ curl "http://3.110.37.81/?str1=foo&str2=bar"
```
12. Open a bash terminal on mongodb container on docker-2 node:  
```
$ docker exec -it db-svc.1.sdtbrk2ofl5zlwawfm29zs1qi bash
```
13. Open a connection to the mongodb and view the data: 
```
$ mongo mongodb://mongo:jPG1KhkyMP@localhost:27017/?authSource=admin
```
