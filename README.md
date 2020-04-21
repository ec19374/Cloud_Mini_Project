About TASTY!
-

This README file contains the description of the Mini-Project for the Cloud Computing module.

The project supports an application that was developed in Flask, using the Python language. It was deployed on a Docker container. The data extracted from the application API has been stored in a Cassandra database.

The project implements an API that retrieves the recipe for given list of ingredients or recipe name itself. The JSON response, from the source, converts to a human-readable HTML format. The information of interest that is produced for the user is: recipe name, ingredients searched, the url address for that recipe. 'Recipe' was chosen as the unique PRIMARY KEY for the Cassandra database. The project assumes that a table already exists in the database ( The table 'recipe.stats' is created in 'KEYSPACE recipe' using CQL)

The main application file name is 'app.py', which firstly imports all the required libraries for this mini-project, namely, 'Cluster' (imported from 'cassandra.cluster' to communicate with a cassandra database), 'Flask', 'Request', 'Render_template' and 'Forms'. 

Running the application:
-
How To Install and Run the Project : Install the Dependencies using pip install -r requirements.txt.

Run the project using python3 app.py.
-
Cassandra
-
Apache Cassandra is a database management system that replicates large amounts of data across many servers, avoiding a single point of failure and reducing latency.

To build the image:
-
sudo docker build . --tag=cassandrarest:v1
To run it as a service, exposing the deployment to get an external IP:

sudo docker run -p 80:80 cassandrarest:v1

Creating RESTful Services
-
Please note: this REST API uses a self signed certificate for SSL encryption. The curl command doesn't like self signed certificates and will not allow any requests to be made. Therefore, in order be able to make a request run all the below commands using sudo and the command parameter -k.

To implement methods like GET,POST,PUT,DELETE.

GET method
-
The GET method is for retrieving information. Within the browser, add '/recipes' to the URL, and it will show the queries made.

Request
-
curl -k -i https://ec2-18-234-180-253.compute-1.amazonaws.com/recipes

Response
-

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 184
Server: Werkzeug/1.0.1 Python/3.7.7
Date: Sun, 19 Apr 2020 01:01:51 GMT
{
'chicken pot pie', 'Chicken pot pie', 'past', 'curry'
}

POST method
-
To add one entry of new recipe information.

Request
-
curl -k -i -H "Content-Type: application/json" -X POST -d '{"recipe":"Burger","ingredients":"beef"}' https://ec2-18-234-180-253.compute-1.amazonaws.com/recipes

Response
-
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 45
Server: Werkzeug/1.0.1 Python/3.7.7
Date: Sun, 19 Apr 2020 00:30:24 GMT
{
  "message": "created: /recipes/Burger"
}

PUT method
-
To update a certain recipe's information.

Request
-
curl -k -i -H "Content-Type: application/json" -X PUT -d '{"name":"Burger","ingredients:"chicken"}' https://ec2-18-234-180-253.compute-1.amazonaws.com/recipes

Response
-
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 45
Server: Werkzeug/1.0.1 Python/3.7.7
Date: Sun, 19 Apr 2020 00:33:04 GMT

{
  "message": "updated: /recipes/Burger"
}

DELETE method
-
To delete a certain recipe.

Request
-
curl -k -i -H "Content-Type: application/json" -X DELETE -d '{"name":"Burger"}' https://ec2-18-234-180-253.compute-1.amazonaws.com/recipes

Response
-
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 45
Server: Werkzeug/1.0.1 Python/3.7.7
Date: Sun, 19 Apr 2020 00:33:32 GMT

{
  "message": "deleted: /recipes/Burger"
}

Creating a Home page
-
Flask looks for template files inside the 'templates' folder, hence, the 'index.html' file has been created inside 'templates'. In order to view the HTML file created, import 'render_template()' from the Flask framework.

Running Flask Application Over HTTPS
-
Self signed certificates are generated in the command line.

openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

Generating a 4096 bit RSA private key... writing new private key to 'key.pem'
-
A form will become available to enter information that will be incorporated into the certificate request. This is called a Distinguished Name or a DN. There are quite a few fields which can be left blank. For some fields there will be a default value, enter '.', the field will be left blank.

Country Name (2 letter code) [AU]:UK
State or Province Name (full name) [Some-State]:London
Locality Name (eg, city) []:Ilford
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Cloud Computing Mini Project
Organizational Unit Name (eg, section) []:QMUL
Common Name (e.g. server FQDN or YOUR name) []:localhost
Email Address []:a.a.quraishi@se19.qmul.ac.uk

This command writes a new certificate in cert.pem with its corresponding private key in key.pem, with a validity period of 365 days. To use this new self-signed certificate in Flask application,ssl_context argument in app.run() is set with a tuple consisting of the certificate and private key files along with port=443.

Kuberenetes Load Balancing Implementation
-
To create an External Load Balancer, the following steps are required:

Install Kubernetes
-
sudo snap install microk8s --classic

1.cassandra-image need to be build and push to registry
-
sudo microk8s enable registry #To install registry

sudo docker build . -t localhost:32000/cassandra-test:registry #To build and tag

sudo docker push localhost:32000/cassandra-test # To push it to the registry

2.The new configuration should be loaded with a Docker daemon restart and restart cassandra-image again
-
sudo systemctl restart docker 

sudo docker start cassandra-test

3.Configure the deployment.yaml file
-
4.Deploy docker container image present in the registry
-
sudo microk8s.kubectl apply -f ./deployment.yaml # To deploy

sudo microk8s kubectl expose deployment app-deployment --type=LoadBalancer --port=443 --target-port=443
Notes:

To see the pods and services created
-
sudo microk8s.kubectl get all

To delete
-
sudo microk8s.kubectl delete deployment app-deployment
sudo microk8s.kubectl delete services app-deployment

