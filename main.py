from contextlib import asynccontextmanager

from deta import Deta
from fastapi import FastAPI, Request, HTTPException, Header, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.param_functions import Depends

from constants import JOBS_SCHEMA, JOBS_SCHEMA_SET
from utils.helpers import hash_password, create_access_token, get_current_user, authenticate_user

templates = Jinja2Templates(directory="templates")  # Specify templates directory

deta = Deta()
db = deta.AsyncBase("jobs_applied")
db_user = deta.AsyncBase("users")

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Close the database connection on shutdown
    await db.close()
    await db_user.close()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="templates"), name="static")

def current_user(x_auth_token: str = Header(None)):
    """Get current user based on x_auth_token"""
    if x_auth_token is None or x_auth_token == "null" :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="x-auth-token header missing."
        )
    
    user = get_current_user(x_auth_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found from the token. Invalid x-auth-token.",
        )
    return user

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )  # Pass request object

@app.get("/signup")
async def root(request: Request):
    return templates.TemplateResponse(
        "signup.html", {"request": request}
    )  # Pass request object

@app.get("/login")
async def root(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request}
    )  # Pass request object


@app.post("/update-job")
async def receive_data(request: Request, user=Depends(current_user)):
    try:
        job_details = await request.json()
        filtered_rows = (
            row for row in job_details if row["column"]["id"] in JOBS_SCHEMA_SET
        )
        filtered_data = {row["column"]["id"]: row["content"] for row in filtered_rows}
        filtered_data['user_email'] = user['email']

        if not filtered_data.get("key"):
            # if key doesn't exists, that means a new row is added
            del filtered_data["key"]

        new_key = await db.put(filtered_data)
        return {"message": "Data successfully updated", "new_key": new_key["key"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@app.get("/get-job")
async def get_all_jobs(user=Depends(current_user)):
    try:
        res = await db.fetch({'user_email': user['email']})
        all_jobs = res.items

        # fetch until last is 'None'
        while res.last:
            res = db.fetch(last=res.last)
            all_jobs += res.items
            
        all_jobs_data = (
            (job.get(schema["id"]) for schema in JOBS_SCHEMA) for job in all_jobs
        )
        return {"data": all_jobs_data, "columns": JOBS_SCHEMA}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@app.delete("/delete-job/{key}")
async def delete_job(key: str = None, user=Depends(current_user)):
    try:
        if not key:
            return {"message": "No key provided"}

        await db.delete(key)
        return {"message": f"Succesfully removed {key}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")
    
async def check_if_user_exists(email, username=None):
    if not (email or username):
        return False
    
    # check for email first, if email is found, return the user
    user = await db_user.get(email)
    if user: 
        return user
    
    response = await db_user.fetch({"username": email})
    if response.items:
        return response.items[0]

@app.post("/signup")
async def signup_user(request: Request):
    """
    Stores user information, including:

    - firstName (str): The user's first name.
    - lastName (str): The user's last name.
    - username (str): The user's unique username for login.
    - email (str): The user's email address.
    - password (str): The hashed password using a secure algorithm.
    """
    try:
        user_details = await request.json()
        user_exists = await check_if_user_exists(user_details.get('email'), user_details.get('username'))
        if user_exists:
            return {"message": "Email already exists", "status": False}
        
        user_details['password'] = hash_password(user_details['password'])
        new_user = await db_user.put(user_details, key=user_details['email'])
        access_token = create_access_token(new_user)
        return {"message": "user successfully created", "status": True, 'access_token': access_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")
    
@app.post("/login")
async def login_user(request: Request):
    """
    Validates user information, including:

    - usernameOrEmail (str): The user's username or email address.
    - password (str): The user's password.
    """
    try:
        user_details = await request.json()
        user_entered_password = user_details['password']
        user = await check_if_user_exists(user_details.get('usernameOrEmail'))
        if not user:
            return {"message": "user does not exists", "status": False}
        
        if authenticate_user(user=user, user_entered_password=user_entered_password):
            access_token = create_access_token(user)
            return {"message": "user successfully created", "status": True, 'access_token': access_token}
    
        return {"message": "Invalid username or password", "status": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")