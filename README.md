# Lesoiree Backend API
This is the backend API for the final year project, the Lesoiree website.


## Setup Virtual Environment (Server Environment) 
1. Run the 'script.py' (it will create virtual enviornments in admin_portal and backend_api)
   
2. Open terminal, cd into the backend_api folder and activate virual enviornmen by running:
   ```
   .\env_backend_api\Scripts\actvate
   ```
3. Install dependency libraires/frameworks to the Virtual Environment of backend_api:  
   ```
   pip install -r requirements.txt
   ```
4. Run the backend api on the environment:  
   ```
   uvicorn app:app --reload
   ```
2. Open terminal, cd into the admin_portal folder and activate virual enviornmen by running:
   ```
   .\env_admin_portal\Scripts\actvate
   ```
5. Install dependency libraires/frameworks to the Virtual Environment of admin_portal: 
   ```
   pip install -r requirements.txt
   ```
4. Run the admin portal on the environment:  
   ```
   streamlit run App.py
   ```
6. To Deactivate the Virtual Environments, run the following on the terminals:  
   ```
   deactivate
   ```


