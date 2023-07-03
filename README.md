# Bro-bot 

An interactive and friendly AI chatbot who can answer your questions from your uploaded documents. 

| Version Info | [![Python](https://img.shields.io/badge/python-v3.10.0-green)](https://www.python.org/downloads/release/python-3913/) [![Platform](https://img.shields.io/badge/Platforms-Ubuntu%2022.04.1%20LTS%2C%20win--64-orange)](https://releases.ubuntu.com/20.04/) |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

# Installation 

1. Fork and Clone this repository 

    ```
    git clone https://github.com/asif-mahmud-am/Bro-bot
    ```

2. Go to your cmd and enter the repository

    ```
    cd Bro-bot
    ```
3. Install the requirements 

    ```
    pip install -r requirements.txt
    ```
4. Create an OPENAI account and get OPENAI API key and put it in .env file 

    ```
    OPENAI_API_KEY = YOUR KEY
    ```

# Document Storing 

You can create your own embedded document store or knowledge base by creating a dataset with rows containing questions and answers related to your desired topic and then use this [script](https://github.com/asif-mahmud-am/Bro-bot/blob/main/document_store.py) for creating your embedded document store from which your model will do semantic search to answer your questions. 

# RUN 

- Run the script ```main.py``` using this command

    ```
    uvicorn main:app --host 0.0.0.0 --port 8081
    ``` 

Your chatbot is now running!! Ask questions and see the magic! 

# Run using Docker 

1. Install docker on your computer 

2. Run the docker container using this command: 

    ```
    docker compose up --build
    ```