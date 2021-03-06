# Readme


## Deployment

- Commit changes to git

(git add, git commit -m "" , git push)

- Login to google server

git pull

 



## Reference links

* https://docs.docker.com/get-started/part2/#build-the-app


## Getting started

### Build the app

```
docker build -t sampleapp .
```

### Check if the image got created

```
Arjuns-MacBook-Pro:slt-umd jyothi$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
sampleapp           latest              9fbc5885b171        2 minutes ago       194 MB
python              2.7-slim            1c7128a655f6        13 days ago         183 MB
```

### Run the docker image (locally)

```
docker run -p 4000:80 sampleapp
```
Navigate to http://127.0.0.1:4000/ to see the app.


### Log into the VM

Open a new terminal window and find the `CONTAINER ID` of the running docker container.
```
Arjuns-MacBook-Pro:slt-umd jyothi$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                  NAMES
be17d4cff42c        sampleapp           "python app.py"     4 seconds ago       Up 3 seconds        0.0.0.0:4000->80/tcp   hardcore_visvesvaraya
```

Copy the `CONTAINER ID` which is `be17d4cff42c` in the above example and submit the following command:
```
docker exec -it be17d4cff42c bash
``` 

### Deploy docker image (on a remote machine)

* Log into the remote box.
* Check if the `simpleapp` container is running
```
docker ps | grep simplaapp
```
* If its running kill it using `docker kill <CONTAINER ID>`
* `git clone` this app or `git pull` to pull down the latest update
* To run the docker image as a deamon.
```
sudo docker run -p 80:80 -d -v /data/logs:/app/logs sampleapp
```


### Cleanup

Cleanup all the dangling and intermediate containers. Note: do this once in a while.

```
docker image prune
```

### Installing Docker on a VM

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04

### UI inputs :

### 303.3,0.03,6.1,0.3,30.3,7.6