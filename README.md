
## Introduction

The tool's purpose is to enforce that only a given list of containers will be allowed to run in your local Docker host

## Usage

As a prerequisite, you need to have Docker Desktop or another Docker engine installed on your host.

Start by running a few containers prior to starting the application. 
For example:
```
docker run -it -d ubuntu
```

Start the application by running the following command from the project's root folder
```
docker-compose up --build
```


Once started, the application will create a `status_state_list` list with all the containers running locally.

Now you can delete the containers you started at the beginning and the tool will start them again maintaining the original containers running.

Similarly, you can start new containers and they will be stopped and deleted in order to preserve the original list.


## Description

I have opted for Python and Flask because of their provided flexibility and easiness to develop the application in the given context. 
Another viable option would have been Node.js for the API server.

In order to manage the containers, I used the docker-py package.



## Kubernetes deployment

#### Strategy
As a deployment strategy, I would choose to deploy the application tool to AWS on EC2 instances.
Another viable option would be Amazon EKS as it would make the deployment easier but we would have less control over the cluster.

For tooling we would need:  
**kubeadm** to manage the clusters. An alternative to this would be **minikube**.  
**kubelet** is useful for starting and running the pods and containers  
**kubectl** is a command-line tool that allows you to run commands against Kubernetes clusters  
**AWS Console** in order to launch the instances.



#### Steps:
- Launch 2 instances on EC2. One instance will be the Master server and one will be the Worker server
- Add them to the same security group to allow them to communicate with each other
- Install Docker and Kubernetes on each server
- Once the Kubernetes and Docker are installed we would need to allow bridging between servers by using iptables
- The Kubernetes cluster needs to be initialized on the Master server
- We would need a CNI plugin for the network configuration. We could use Flannel, Calico or Romana
- The last step would be to deploy the containers' images to the cluster

#### Monitoring
For monitoring purposes I would use tools such as Prometheus to collect data and metrics from the cluster and Grafana to display the data 




