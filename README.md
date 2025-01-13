# SA Connect: Student Assistant Recruitment System
This is the SA Connect application, designed to streamline the student assistant (SA) recruitment process for the WPI Computer Science Department. 
It allows students to apply for available SA positions, and enables faculty to create positions and review applications.

# Installation Instructions
To set up this application on your local machine, follow these steps:

### 1. Clone the repository:
- git clone https://github.com/<your-username>/sa-connect.git
- cd sa-connect

### 2. Set up a virtual environment (Optional but recommended): If you're using Python 3, create and activate a virtual environment:
- python -m venv venv
- venv\Scripts\activate

### 3. Install the dependencies:
- pip install -r requirements.txt

### 4. Set up your .env file:
Create a .env file in the root of the project directory and add the following configurations:

- Microsoft Authentication Configurations
  - AUTHORITY=https://login.microsoftonline.com/<tenant-id>
  - CLIENT_ID=<your-client-id>    
CLIENT_ID=<your-client-id>    

- Database Connection Configurations
  - AWS EC2 (Production)
      - AWS_EC2=postgresql+psycopg2://<username>:<password>@<aws-rds-endpoint>/<database-name>

  - Local Database (Development)
      - DATABASE_URL=postgresql://<username>:<password>@localhost:5432/sa_connect

- Microsoft Graph API Endpoint
  - ENDPOINT=https://graph.microsoft.com/v1.0/me

- Microsoft Authentication Configurations: These values are necessary for integrating Microsoft Authentication (e.g., login) using Azure AD.
- AWS EC2 Database (Production): If deploying on AWS EC2 with AWS RDS, set the AWS_EC2 value to the connection string for your PostgreSQL RDS instance.
- Local Database (Development): If running the app locally, the DATABASE_URL will be used to connect to your local PostgreSQL database.
- Microsoft Graph API Endpoint: The ENDPOINT is used for fetching user details from Microsoft Graph API.

### 5. Database Setup:
The application is configured to work with AWS RDS for production environments and SQLite for local development.

- AWS RDS:
  - If you plan to deploy the app on AWS EC2 and use AWS RDS, you will need to create an RDS instance (e.g., MySQL or PostgreSQL) and update the config.py file with the corresponding RDS connection string.
  - Example configuration for RDS (MySQL):
    - SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<username>:<password>@<hostname>:<port>/<database>'

- Local Database:
  - For local development, the app will connect to a local PostgreSQL database using the DATABASE_URL from the .env file.

### 6. Docker Setup:
The application can be easily deployed using Docker for both development and production environments.

Steps to run the application using Docker:
1. Build the Docker image: Run the following command to build the Docker image
- docker build -t sa_connect .
2. Run the Docker container: Use the following command to run the application in a Docker container:
- docker run -p 5000:5000 sa_connect

This will start the application inside a Docker container, and you can access it at http://localhost:5000.
Note: Make sure that your AWS RDS connection is properly configured when running in Docker for production environments

### 7. AWS EC2 Deployment:
To deploy the application to AWS EC2:
- Set up an EC2 instance (e.g., Ubuntu-based instance).
- SSH into the EC2 instance and clone the repository:
- If you're using AWS RDS, make sure to configure the config.py file with the appropriate RDS connection string.
- Start the Flask application for production use.

# Running the Application
To start the application locally, run:
- flask run

This will start the server on http://localhost:5000. You can now access the application in your web browser.
