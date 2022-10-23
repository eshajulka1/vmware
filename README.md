# vmware
vmware ques
Overview
Create a solution (in either golang or python) designed to run on a Kubernetes Cluster to monitor internet urls and provide Prometheus metrics, once completed please upload your solution to your github.com account.  Please make it public.
 
Requirements
•	A service written in python or golang that queries 2 urls (https://httpstat.us/503 & https://httpstat.us/200)
•	The service will check the external urls (https://httpstat.us/503 & https://httpstat.us/200 ) are up (based on http status code 200) and response time in milliseconds
•	The service will run a simple http service that produces metrics using appropriate Prometheus libraries and outputs on /metrics
•	Expected response format:
o	sample_external_url_up{url="https://httpstat.us/503 "}  = 0
o	sample_external_url_response_ms{url="https://httpstat.us/503 "}  = [value]
o	sample_external_url_up{url="https://httpstat.us/200 "}  = 1
o	sample_external_url_response_ms{url="https://httpstat.us/200 "}  = [value]

In order to prepare for the above problem statement, I started with the python code for the image.
This repository collects Kubernetes manifests, Grafana dashboards, and Prometheus rules combined with documentation and scripts to provide easy to operate end-to-end Kubernetes cluster monitoring with Prometheus.
So, here I would be using 2 types of metrics to fetch the required data from the Kubernetes application.
Counter
A counter is a cumulative metric that represents a single monotonically increasing counter whose value can only increase or be reset to zero on restart. For example, you can use a counter to represent the number of requests served, tasks completed, or errors.
Do not use a counter to expose a value that can decrease. For example, do not use a counter for the number of currently running processes; instead use a gauge.
Histogram
A histogram samples observations (usually things like request durations or response sizes) and counts them in configurable buckets. It also provides a sum of all observed values.
A histogram with a base metric name of <basename> exposes multiple time series during a scrape:
cumulative counters for the observation buckets, exposed as <basename>_bucket{le="<upper inclusive bound>"}
the total sum of all observed values, exposed as <basename>_sum
the count of events that have been observed, exposed as <basename>_count (identical to <basename>_bucket{le="+Inf"} above)
Use the histogram_quantile() function to calculate quantiles from histograms or even aggregations of histograms. A histogram is also suitable to calculate an Apdex score. When operating on buckets, remember that the histogram is cumulative. See histograms and summaries for details of histogram usage and differences to summaries.

Post creation of the python code (server.py), we need to create a docker image for the same.
Here, I used AWS EC2 instances to build my job, so first I tried to install docker post launching the EC2 instance:
![image](https://user-images.githubusercontent.com/107342198/197375426-6e9d81e8-7ae8-4b93-b0fc-7e14c64a0423.png)
Update the packages on your instance
sudo yum update -y
Install Docker
sudo yum install docker -y
Start the Docker Service
sudo service docker start
Add the ec2-user to the docker group so you can execute Docker commands without using sudo.
sudo usermod -a -G docker ec2-user

DockerFile for the python code:

FROM python:3.10.5-alpine3.16 AS build
RUN mkdir /app/
WORKDIR /app/
COPY ./src/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./src/ /app/
ENV FLASK_APP=server.py
EXPOSE 8000
EXPOSE 5000
CMD flask run -h 0.0.0.0 -p 5000

Commands:
# docker build -t server/python:1.0 -f Dockerfile .
Once the command is executed, we can check under : docker images
Pushing Image to DockerHub:
# docker login   (Enter the credentials for the dokerhub)
# docker tag server/python:1.0 eshajulka/mydockerrepo:1.0
# docker push eshajulka/mydockerrepo:1.0   (push to docker hub)
![image](https://user-images.githubusercontent.com/107342198/197375437-8085ae36-f452-4559-97e0-312c5500f7cf.png)

Now we, need to install the kubernetes cluster on the EC2 instance. So for this here I have used k3s (lightweight Kubernetes cluster) installation.
K3S Installation: (The certified Kubernetes distribution built for IoT & Edge computing)

This can be installed on the same EC2 instance with the help of the below command from (K3s).
curl -sfL https://get.k3s.io | sh - 
# Check for Ready node, takes ~30 seconds 
k3s kubectl get node

Post the installation is successful, we can execute the kubectl commands to verify.

Creating deployments in the Kubernetes cluster:

The deployments and the respective services can be created with the help of Yaml manifest files.
![image](https://user-images.githubusercontent.com/107342198/197375447-13be660c-074e-496b-b005-cdc82ab2593c.png)

For application, I have given the below command:
Kubectl create deployment server-python --image=eshajulka/mydockerrepo --replicas=2 and later on added the annotations, which would help the Prometheus to pull the metrics.
Post this I tried accessing the links described in the overview sections:

![image](https://user-images.githubusercontent.com/107342198/197375465-5b242139-5244-4e87-8b76-e5fdc81dc3e8.png)

https://httpstat.us/200

![image](https://user-images.githubusercontent.com/107342198/197375474-caf4a422-36d4-46ce-a748-9634d85ad3ca.png)


https://httpstat.us/503
![image](https://user-images.githubusercontent.com/107342198/197375483-14a33bbe-6a6b-4551-90c1-2dca8ea4e916.png)


