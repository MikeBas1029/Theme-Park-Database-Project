<h1 align="center" id="title">Theme Park Management</h1>

<p align="center"><img src="https://socialify.git.ci/MikeBas1029/Theme-Park-Database-Project/image?description=1&amp;descriptionEditable=A%20full-stack%20app%20to%20manage%20the%20operations%20of%20a%20theme%20park.&amp;font=Source%20Code%20Pro&amp;language=1&amp;name=1&amp;pattern=Charlie%20Brown&amp;theme=Dark" alt="project-image"></p>

## Table of Contents

-   [Table of Contents](#table-of-contents)
-   [Run Locally](#run-locally)
-   [Usage](#usage)
    -   [Frontend](#frontend)
    -   [Backend](#backend)
-   [Environment Variables](#environment-variables)

## Run Locally

Clone the project

```bash
  git clone https://github.com/MikeBas1029/Theme-Park-Database-Project.git
```

Go to the project directory

```bash
  cd Theme-Park-Database-Project
```

Start the app

```bash
  npm start
```

## Usage

### Frontend

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run start
```

This runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

### Backend

**Windows (Command Prompt)**

Create virtual environment

```cmd
python -m venv venv
```

Activate virtual environment

```cmd
venv\Scripts\activate
```

Install requirements

```cmd
pip install -r backend/requirements.txt
```

Deactivate virtual environment

```cmd
deactivate
```

**Mac Setup**

Create virtual environment

```bash
python3 -m venv venv
```

Activate virtual environment

```bash
source ./venv/bin/activate
```

Install requirements

```bash
pip install -r backend/requirements.txt
```

Deactivate virtual environment

```bash
deactivate
```

To start the backend server, run the following from the root directory:

```bash
fastapi dev backend/src/main.py
```

This runs a local development server at http://127.0.0.1:8000.

More useful, navigate to http://127.0.0.1:8000/docs to see the available endpoints. You can test them out from here.

> [!CAUTION]
> If you test out any of the CRUD endpoints, it will alter the table. Beware of any unintended changes.

## Environment Variables

To run the `backend` directory for this project, you will need to add the environment variables in `.env.example` to a `.env` file in your local root directory

> [!NOTE]
> The `SSL_CERT` environment variable must be set in order to connect to the remote database on Azure.
> Download the certificate from [here](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-connect-tls-ssl#download-the-public-ssl-certificate) and store it in your root directory. Then update the `SSL_CERT` env variable in `.env` to be the path to that certificate. Nothing else is required.

<h2>💻 Built with</h2>
Technologies used in the project:

-   Python
-   FastAPI
-   MySQL
-   Azure
-   React
