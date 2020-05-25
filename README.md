
## Capstone Project- Build a Data Science CI/CD Pipelines and Microservice

This repository provides the material for the "Capstone project for DevOps Nanodegree".
Jupyter notebooks are an invaluable tool for a data scientist. They are open-source web applications that allow creation of documents that show the output of code written in multiple languages (i.e., Julia, Python, R), and which can be annotated with writing and visualizations. Jupyter notebooks have a wealth of different uses including as a testing ground for development work, a presentation platform, and more.

Containerization can help to package up an analysis. They can include any scripts and code and guaranteed to work on everyone’s machine—no installation required.

### Steps in Completing Your Project
#### Step 1: Propose and Scope the Project
* Plan what your pipeline will look like.
* Decide which options you will include in your Continuous Integration phase. - Use Jenkins.
* Pick a deployment type - either rolling deployment or blue/green deployment.

Blue-green deployment is a technique that reduces downtime and risk by running two identical production environments called Blue and Green.

At any time, only one of the environments is live, with the live environment serving all production traffic. For this example, Blue is currently live and Green is idle.

As you prepare a new version of your software, deployment and the final stage of testing takes place in the environment that is not live: in this example, Green. Once you have deployed and fully tested the software in Green, you switch the router so all incoming requests now go to Green instead of Blue. Green is now live, and Blue is idle.

This technique can eliminate downtime due to app deployment. In addition, blue-green deployment reduces risk: if something unexpected happens with your new version on Green, you can immediately roll back to the last version by switching back to Blue
[reference](https://docs.cloudfoundry.org/devguide/deploy-apps/blue-green.html).

* For the Docker application you can either use an application which you come up with, or use an open-source application pulled from the Internet, or if you have no idea, you can use an Nginx “Hello World, my name is (student name)” application.


#### Step 2: Use Jenkins, and implement blue/green or rolling deployment.
#### Create your Jenkins master box with either Jenkins and install the plugins you will need.

##### A. AWS Steps
Log in to the AWS management console, as a Root user. Find and select the IAM (Identify and Access Management) service.

###### Click on "Group" menu item from the left sidebar. Create a new group and name it "jenkins", and attach the following policies:
* AmazonEC2FullAccess
* AmazonVPCFullAccess
* AmazonS3FullAccess.

###### Create an IAM user
Click on "Users" menu item from the left sidebar. Create a new IAM User, select "Users" from the left sidebar, then "Add user," and use "jenkins" as the user name. Click on both "programmatic access" and "AWS management console access." The defaults for auto-generated password and "users must create a new password at next sign-in" are OK and should be kept. Hit "Next", and add the "jenkins" user to the "jenkins" group. Hit "next," no need to add "Tags." Review, and accept. Capture the Access Key, Secret Access Key, and the password so that you can log in as IAM user in the next step. (easy to just download the csv file).

Copy the IAM User sign-in link from the IAM Dashboard.

Sign in as the new IAM user in a new browser window.

First, sign out of the AWS console. Then, use the IAM User sign-in link copied from the previous step.

Alternatively, you can login as the root user. Go to IAM dashboard. Click on "Users" menu item from the left sidebar. Select the 'jenkins' user link, and go to the Security credentials tab. Copy the "Console sign-in link". If you haven't copied the IAM User sign-in link, you can generate the URL as follows:

In the following syntax https://<your_aws_account_id>.signin.aws.amazon.com/console/, replace the <your_aws_account_id> with your AWS account number without the hyphens (for example, if your AWS account number is 1234-5678-9012, your AWS account ID is 123456789012)
Create a new key pair for access to your instance(s). Choose EC2 as the service after logging in. Select "Key Pairs" from the sidebar on the left, from the "Network and Security" section. Enter the "pipeline" name when prompted. Save the ".pem" file. If you will use an SSH client on a Mac or Linux computer to connect to your Linux instance, use the following command to set the permissions of your private key file so that only you can read it:

``chmod 400 your_user_name-key-pair-region_name.pem``

Launch the EC2 t3.micro, pick "Ubuntu 18.04 LTS amd64," review, and when hitting "launch" ensure that an existing pair ("pipeline") from before is selected. If you're not using the right key pair, you cannot log in. Now, an Ubuntu 18.04 t2.micro instance is launched in the AWS EC2, that can be accessed via SSH using the PEM file. 

Once launched, create a security group for the vm. In the left sidebar, under Network and Security, select "Security Groups." Under name, use: 'jenkins', description: "basic Jenkins security group," VPC should have the default one used. 

Click Add Rule: 
* SSH: Port Range: 22, Source: MyIp. This allows us to connect to the server via SSH.
* HTTP: Port Range: 80, Source: MyIp. This allows us to connect the EC2 to a website.
* HTTPS: Port Range: 443, Source: MyIp. This allows us to connect the EC2 to a website.
* Custom TCP Rule: Port Range: 2376, MyIp: Anywhere. This allows us to access Docker Hub.
* Custom TCP Rule: Port Range: 8888, MyIp: Anywhere. This allows us the port on which to run Jupyter notebook.
* Custom TCP Rule: Port Range: 8080, MyIp: Anywhere. This allows us the port on which to run Jenkins. 

You can also limit access by entering a custom IP into the source.

Go back to instances, and right-click the running instance, select Networking and change the security groups. Select the Jenkins security group that was created previously.

To connect to your instance using your key pair, follow these steps. Right click your running instance and select "Connect," then follow the instructions to SSH into it. For example, here are the directions that popped up in my AWS console on how to SSH into my machine (your directions will not look exactly like this, since portions of the information, like the full domain address of the instance, will be different):

##### B. Install Jenkins On Ubuntu
Here are the key commands for installation:

``apt update``

``apt upgrade``

``apt install default-jdk``

The Jenkins version you get with the default Ubuntu packages is often not the latest available version you can get from the Jenkins project itself. For the most recent features and fixes, you can use the packages from the Jenkins site to install Jenkins.

First, use wget to add the repo key to the system:

``wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -``

When the key is added, the system returns OK. Next, append the Debian package repo address to the server's sources.list:

``sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'``

When both of these are all set, run update so that apt will use the new repo:

``sudo apt update``

Lastly, install Jenkins and its dependencies:

''sudo apt install jenkins''

Since systemctl doesn't produce output, you can use its status command to confirm that Jenkins began successfully:
sudo systemctl status jenkins

If all went well, the first lines of the output will show that the service is active and configured to start at boot, as shown below:

##### C. Set Up Jenkins
Visit Jenkins on its default port, 8080, with your server IP address or domain name included like this: http://your_server_ip_or_domain:8080.

Next you will see the "Unlock Jenkins" screen, displaying the location of the initial password. In the terminal, use cat to show the password:

``sudo cat /var/lib/jenkins/secrets/initialAdminPassword``

Copy and paste the 32-character alphanumeric password from the terminal into the Admin password field, then Continue.
The next screen gives you the choice of installing recommended plugins, or selecting specific plugins - choose the Install suggested plugins option, which quickly begins the installation process.

When installation is complete, you are prompted to set up the first admin user. Create the admin user and make note of both the user and password to use in the future.

You next see an Instance Configuration page, asking you to confirm the preferred URL for your Jenkins instance. Confirm the address, click save and finish.

##### D. Install Blue Ocean plugin
"Blue Ocean" and other required plugins need to be installed. Logged in as an admin, go to the top left, click 'Jenkins', then 'manage Jenkins', and select 'Manage Plugins'.
Use the "Available" tab, filter by "Blue Ocean," select the first option ("BlueOcean aggregator") and install without a restart.

Filter once again for "pipeline-aws" and install, this time selecting "Download now and install after restart."
Once all plugins are installed, Jenkins will restart. If it hasn't restarted, run the following in the VM:

``sudo systemctl restart jenkins``



Verify everything is working for Blue Ocean by logging in. An "Open Blue Ocean" link should show up in the sidebar. Click it, and it will take you to the "Blue Ocean" screen, where we will have to add a project.

A welcome screen will appear, telling you it is time to create your first pipeline.

Click "create pipeline."

#### Set up your environment to which you will deploy code.

[Create (and activate) a new environment](https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-python3-boto3/), named .devops with Python 3. 

If prompted to proceed with the install (Proceed [y]/n) type y.

`python3 -m venv ~/.devops`

`source ~/.devops/bin/activate`

At this point your command line should look something like: (.devops) 
<User>:project-name<user>$. The (.devops) indicates that your environment has been activated, and you can proceed with further package installations.

Installing dependencies via project Makefile. 

Many of the project dependencies are listed in the file requirements.txt; these can be installed using pip commands in the provided Makefile. While in your project directory, type the following command to install these dependencies.
make install
Now most of the .devops libraries are available to you. There are a couple of other libraries that we'll be using, which can be downloaded as specified, below.

* Run `make install` to install the necessary dependencies

#### Set up a GitHub Repository
Note: A GitHub account is required for the next steps.
Create a new repository in your GitHub account. In the repo, have a "Jenkinsfile" which should look like this:

Commit and push your changes.

Select GitHub from the options available, a token needs to be generated. A link to https://github.com/settings/tokens/new?scopes=repo,read:user,user:email,write:repo_hook needs to be clicked to generate a token for Jenkins to use. You can select the default scopes in the opened link, that defines the access for a personal token for Jenkins.
Authenticate in Github, and add a note for what this token is (easier for later removal): "Jenkins Pipeline."
Make sure you copy the token - there is no way to see it again!

After pasting the token into the form in Jenkins, click "connect", and your account should show up. If your account belongs to multiple organizations, they will be listed - make sure you use your personal account and organization.
Next, search for "static" so that the repo is matched, and click "create pipeline."

The pipeline should show up with a new run.

##### Set up AWS credentials in Jenkins
Credentials need to be created so that they can be used in our pipeline.

Leave the Blue Ocean GUI, and go back to the main Jenkins page. Then click on the “Credentials” link from the sidebar.
Click on "(global)" from the list, and then "Add credentials" from the sidebar.

Choose "AWS Credentials" from the dropdown, add "aws-static" on ID, add a description like "Static HTML publisher in AWS," and fill in the AWS Key and Secret Access Key generated when the IAM role was created.

Click OK, and the credentials should now be available for the rest of the system.

#### Set up Docker

You can install and configure Docker using an install script provided by the Docker team.  Execute this statement:

``curl -sSL https://get.docker.com/ | sh ``

Add the ubuntu user to the docker group to allow the ubuntu
user to issue commands to docker without sudo. Execute this statement:

``sudo usermod -aG docker ubuntu``

Next, reboot to let the changes take effect. Execute this statement:

``sudo reboot``

Reconnect to the system and check the docker version by executing this statement:

``docker -v``

* List all containers (only IDs)

``docker ps -aq``

* Stop all running containers
``docker stop $(docker ps -aq)``

* Remove all containers
`` docker rm $(docker ps -aq) ``

* Remove all images
``docker rmi $(docker images -q)``

* Jenkins needs to be added to the group docker

``sudo usermod -a -G docker jenkins``

Then restart Jenkins


#### Step 3: Pick AWS Kubernetes as a Service, or build your own Kubernetes cluster.
* Use Ansible or CloudFormation to build your “infrastructure”; i.e., the Kubernetes Cluster.
* It should create the EC2 instances (if you are building your own), set the correct networking settings, and deploy software to these instances.
* As a final step, the Kubernetes cluster will need to be initialized. The Kubernetes cluster initialization can either be done by hand, or with Ansible/Cloudformation at the student’s discretion.

Image is available at [dockerhub](https://hub.docker.com/repository/docker/piushvaish/capstone-project-jupyter/general)

run ``sh run_kubernetes.sh``

###### the text from extract is available at : 

* out_kubernetes.txt

#### Step 4: Build your pipeline
* Construct your pipeline in your GitHub repository.
* Set up all the steps that your pipeline will include.
* Configure a deployment pipeline.
* Include your Dockerfile/source code in the Git repository.
* Include with your Linting step both a failed Linting screenshot and a successful Linting screenshot to show the Linter working properly.
![Failed Linting](images/lintfail.png)

![Successful Linting](images/lintingworking.png)


#### Step 5: Test your pipeline
* Perform builds on your pipeline.
* Verify that your pipeline works as you designed it.
* Take a screenshot of the Jenkins pipeline showing deployment and a screenshot of your AWS EC2 page showing the newly created (for blue/green) or modified (for rolling) instances. Make sure you name your instances differently between blue and green deployments.


