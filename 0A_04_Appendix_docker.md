
## Our Datascience Stack
Our goal here is to run Jupyter and Mongo as a Docker Stack via Docker Cloud. 

Docker is a virtualization technology we can use to maintain a reusable data science system for performing the tasks in this text. Docker's ecosystem consists of Containers, Images, Nodes, Services, and Stacks as well as two cloud services we will take advantage of, Docker Hub and Docker Cloud. 

A container is a stripped down Linux operating system. An image is software you provision into a container. A node is container that lives in the cloud (we will use Digital Ocean) where we can host our images. A service is a specific image running in our node, that may or may not be available to other services running on that node. A stack is a collection of services including the links between them. 

Jupyter provides opinionated stacks [@jupyter_stacks] for use in a variety of contexts. We are essentially interested in the `datascience-notebook` with a slight modification. I often like using an ORM to interface with my datasets, in particular, the python `mongoengine` [@mongoengine] library for interfacing with MongoDB [@mongodb]. Jupyter does not include this library with its stack, nor is it easily available using the `conda` tool that is used to install most of the python data science stack. In order to have it included we are going to have to build our own Docker container image. The beauty of docker is that we do not have to start from scratch. We begin with the Jupyter minimal image and add only the additional components we need, in this case, `mongoengine`.

### Dockerfile

In order to build our Docker image, we will use the docker command line interface. We will edit our `Dockerfile` using a standard text editor and then build and run the image via the CLI. In order to facilitate the automated build process as part of our final deployment process, we will maintain the image using git and github. We will ultimately use the image via the automated build process. A completed version of this `Dockerfile` is included at the end of this section.

#### Docker Toolbox

Make sure that you have the Docker Toolbox installed and that you are able to use the Docker command line interface (CLI) to the Docker Engine. On my mac, I need to run the Docker Quickstart Terminal application. This fires up the virtual machine that will serve as the local Docker Host, then opens my terminal application, configures numerous environment variables, finally drawing this nifty picture:

```bash
                        ##         .
                  ## ## ##        ==
               ## ## ## ## ##    ===
           /"""""""""""""""""\___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
           \______ o           __/
             \    \         __/
              \____\_______/

```

Confirm that everything is working properly by listing all currently running containers with 

```bash
$ docker ps
```

If you have none running, likely at this point, you should see the following:

```bash
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```


#### Configure working directory for working with Github

As we will be using Docker's Github integration and its automated build capability to ultimately use our image, we will need to configure and use `git` to interface with Github. 

```bash
$ mkdir docker
$ mkdir docker/datascience
$ cd docker/datascience
$ git init
$ git touch Dockerfile
$ git add Dockerfile
$ git commit -m 'init'
```

On github, create a repo called `datascience`.

```bash
$ git remote add origin git@github.com:#USERNAME#/datascience.git
$ git push -u origin master
```
 
Open `Dockerfile` in your favorite text editor. In order to not completely start from scratch, we will use the `jupyter/minimal-notebook` are the basis for our image. When we build our image, it will first pull and build this image, then build our on top of this one. 

#### Build the image on an existing image
```yaml
# Dockerfile
FROM jupyter/minimal-notebook
```

#### Identity ourselves as maintainer
We add our name as maintainer.

```yaml
# Dockerfile
MAINTAINER Joshua Cook <me@joshuacook.me>
```


#### Operate as a certain User

We will do several rounds of provisioning or installing necessary software on the machine and will need different permission levels while doing so. The `jupyter/minimal-notebook` has a user named `joyvan` that is used to run the jupyter platform. We will also need to install many libraries as `root`. We will do our first round of installs as `root`. We tell this to Docker using the command `USER`. 

```yaml
# Dockerfile
USER root
```


#### Provision the Image

```yaml
# Dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python2.7 \
    python-dev \
    python-pip \
    python3 \
    python3-dev \
    python3-pip \
    fonts-dejavu \
    gfortran \
    gcc && apt-get clean

# libav-tools for matplotlib anim
RUN apt-get update && \
    apt-get install -y --no-install-recommends libav-tools && \
    apt-get clean
```

#### Provision `scipy/numpy`

Next we install our Python libraries. We largely use `conda` to do this. `conda` comes pre-installed with the `jupyter/minimal-notebook` image. We do this as `USER joyvan`.

```yaml
# Dockerfile
USER jovyan

# Install Python 3 packages
RUN conda install --yes \
    'ipywidgets=4.1*' \
    'pandas=0.17*' \
    'matplotlib=1.5*' \
    'scipy=0.17*' \
    'seaborn=0.7*' \
    'scikit-learn=0.17*' \
    'scikit-image=0.11*' \
    'sympy=0.7*' \
    'cython=0.23*' \
    'patsy=0.4*' \
    'statsmodels=0.6*' \
    'cloudpickle=0.1*' \
    'dill=0.2*' \
    'numba=0.23*' \
    'bokeh=0.11*' \
    'h5py=2.5*' \
    && conda clean -tipsy

# Install Python 2 packages
RUN conda create --yes -p $CONDA_DIR/envs/python2 python=2.7 \
    'ipython=4.1*' \
    'ipywidgets=4.1*' \
    'pandas=0.17*' \
    'matplotlib=1.5*' \
    'scipy=0.17*' \
    'seaborn=0.7*' \
    'scikit-learn=0.17*' \
    'scikit-image=0.11*' \
    'sympy=0.7*' \
    'cython=0.23*' \
    'patsy=0.4*' \
    'statsmodels=0.6*' \
    'cloudpickle=0.1*' \
    'dill=0.2*' \
    'numba=0.23*' \
    'bokeh=0.11*' \
    'h5py=2.5*' \
    'pyzmq' \
    && conda clean -tipsy
    
```   

#### Provision `R`

Use `conda` to configure `R`.

``` 
# Dockerfile 
# R packages including IRKernel which gets installed globally.
RUN conda config --add channels r
RUN conda install --yes \
    'rpy2=2.7*' \
    'r-base=3.2*' \
    'r-irkernel=0.5*' \
    'r-plyr=1.8*' \
    'r-devtools=1.9*' \
    'r-dplyr=0.4*' \
    'r-ggplot2=1.0*' \
    'r-tidyr=0.3*' \
    'r-shiny=0.12*' \
    'r-rmarkdown=0.8*' \
    'r-forecast=5.8*' \
    'r-stringr=0.6*' \
    'r-rsqlite=1.0*' \
    'r-reshape2=1.4*' \
    'r-nycflights13=0.1*' \
    'r-caret=6.0*' \
    'r-rcurl=1.95*' \
    'r-randomforest=4.6*' && conda clean -tipsy
    
```

#### Include a Repo of Jupyter Notebooks

The next command gives us the opportunity to include a repo of notebooks that we has been previously created. We can use jupyter to back this repo up to github and thus maintain our work across docker instances and in the case in which we need to reboot our docker image.     

```yaml
# Dockerfile
# Add local content, starting with notebooks and datasets which are the largest
# so that later, smaller file changes do not cause a complete recopy during
# build

COPY jupyter_notebooks/ /home/jovyan/work/
```

Note that you will need to add this folder to git repo as well. 

```bash
$ git add jupyter_notebooks
$ git commit -m 'add folder of notebooks'
$ git push
```

#### Provision `mongoengine`

We need to install `mongoengine` as `root`.

```yaml
# Dockerfile
USER root

# Install MongoEngine python 3 wants mongoengine installed as root
RUN pip install mongoengine
RUN pip3 install mongoengine
```

#### Configure Python 2 kernel
```yaml
# Dockerfile
# Install Python 2 kernel spec globally to avoid permission problems when NB_UID
# switching at runtime.
RUN $CONDA_DIR/envs/python2/bin/python \
    $CONDA_DIR/envs/python2/bin/ipython \
    kernelspec install-self
```

#### Switch back to `USER joyvan`

We complete our container in the role of `joyvan`.

```yaml  
# Dockerfile
# Switch back to jovyan to avoid accidental container runs as root
USER jovyan
```


### Local Development

Though we will ultimately be using this image via an automated build process, it is easiest to develop the image via a local build process. We have found the following commands to be most helpful in this process. 


#### Build Image Locally
```bash
$ docker build -t joshuacook/datascience .
```

This command will start a build process locally. Upon completion you will be able to run the image locally on your Docker Container. 

#### Run Image Locally

```bash
$ docker run joshuacook/datascience
```

This will run the image on your local container. If the build was successful, you will be able to use Jupyter by visiting http://localhost:8888 in your browser.

#### Interface With Image via `bash`

```bash
$ docker run -it joshuacook/base bash
```

If the image is not compiling correctly, it may be helpful to interface with the image via a `bash` shell. This command will run the image and then open a shell to the image. 

To interface with the image as `USER root` run the following variation.

```bash
$ docker run -it --user root joshuacook/datascience bash
```


### Automated Build 

As stated we will be using this image via Docker Hub's automated build service. Log into to Docker Hub in order to configure this service at http://hub.docker.com. Select 'Create Automated Build'. Given an option between Github and BitBucket, choose Github. After authenticating your Github account, you should be shown a list of available repositories on your Github account. Choose the previously created repo, `datascience`. 

Docker will automatically name the build after the associated repo. Your image will have the name `#DOCKERUSER#/datascience`. Give the image a short description such as "Image for use in computational chemistry." Click 'Create'. Upon this, the automated build should be created and you will be taken to the page on Docker Hub for your image. 

The last step is to initiate an automated build. 

In the local repo, stage, commit, and push the changes to your `Dockerfile` to Github. 

```bash
$ git add Dockerfile
$ git commit -m 'initial build of Docker Image'
$ git push
```

#### Check Build Details

Upon completing this push to Github, return to your image's page at Docker Hub. Click the link Build Details. You should see that a build has been initiated. In less than a half hour, the build should complete. Your image will now be available for cloud deployment. 


### DockerCloud


#### Link to a Cloud Provider

Having built our image, we are now ready to deploy our image via Docker Cloud. After setting up a Docker Cloud account and a Digital Ocean account, we will begin by linking the two. This can be done via Account Info under the tab Cloud Providers. Simply click the link 'Add Credentials' and complete the linking process. 

#### Deploy a Node

Visit the Node tab and click 'Launch new node cluster'. Define the essential information for the node. Since we have built our stack using Docker, we can always change this information later if we need more or less cpu power or disk space. For now, a basic 2 GB[2 CPU/2 GB RAM] should be sufficient.  


### Stackfile

To deploy our computational stack we will not be working with individual services. Rather we will use Docker's `Stackfile` format to define our stack. This is much more straightforward then the `Dockerfile` can be entered directly into the browser. Visit the Stacks tab and click 'Create Stack'. Give the stack a name such as `datascience` and enter the following:

```yaml
# Stackfile

datascience:
  image: '#USERNAME#/datascience:latest'
  environment:
    - 'PASSWORD=#PASSWORD#'
  links:
    - mongo
  ports:
    - '80:8888'
mongo:
  image: 'mongo:latest'
  expose:
    - '27017'
```

Note, that we have included MongoDB's image with no additional modifications, exposed the mongo image/service on the default port `27017`, and then linked `mongo` to our `datascience` stack using 

```yaml
links:
  - mongo
```

Note that we have link port `8888` on our datascience image/service to port `80` on our node which means that our `datascience` image/service will be available in a browser by visiting the ip or dns associated with our node. 
