# trial-rag-chat

# CAUTION
This repository is just for learning purpose.  
Don't deploy app based on current project.

# Advance prepration
1. create .venv in project root
2. install libraries with `pip install -r requirements.txt`
3. install Docker
4. run `docker compose build`

# How to run app locally
Run the commands below in order.   
If you want to run app in windows, replace `/` to `\`.
1. `docker compose up`
2. `fastapi dev ./fastapi_server.py`
3. `streamlit run ./streamlit_app.py`   
