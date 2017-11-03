## HOW INTO DOCKER WITH DATASCIENCE PACKAGES:
Here is a brief overview about using docker for our project when using ubuntu:


1. Install docker following instructions on this site: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#docker-ee-customers  
2. Create work folder somewhere on your PC and run this command in terminal:
`sudo chown 1000 /some/host/folder/for/work`  
3. Run this command in your terminal:
`sudo docker run -it --rm -e NB_UID=1000 -p 8888:8888 -v /some/host/folder/for/work:/home/jovyan/work lampo/tetrisennimage`  
4. If everything went well you should have a message like this in the terminal:  
`Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://localhost:8888/?token=075c81a1c81baefbc34c7958aec8fd8db65d43f10acfc319
`  
Use this link to connect for the first time with jupyter server.  
5. You can now work with Jupyter Notebooks using docker container. Every file that is saved in your `/some/host/folder/for/work` will be mirrored
by your `/home/jovyan/work` folder in docker container.  
6. If you want to use bash in your docker container first get your container id using `sudo docker ps` and then use command `sudo docker exec -it CONTAINER_ID /bin/bash`
