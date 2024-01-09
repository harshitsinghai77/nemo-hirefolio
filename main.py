from contextlib import asynccontextmanager

from deta import Deta
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from constants import JOBS_SCHEMA, JOBS_SCHEMA_SET

templates = Jinja2Templates(directory="templates")  # Specify templates directory

deta = Deta()
db = deta.AsyncBase("jobs_applied")


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Close the database connection on shutdown
    await db.close()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="templates"), name="static")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )  # Pass request object


@app.post("/update-job")
async def receive_data(request: Request):
    try:
        job_details = await request.json()
        filtered_rows = (
            row for row in job_details if row["column"]["id"] in JOBS_SCHEMA_SET
        )
        # print([row["column"]["id"] for row in job_details if row["column"]["id"] in JOBS_SCHEMA_SET])
        filtered_data = {row["column"]["id"]: row["content"] for row in filtered_rows}
        print("filtered_data: ", filtered_data)

        if not filtered_data.get("key"):
            # a new row is created
            del filtered_data["key"]

        new_key = await db.put(filtered_data)
        return {"message": "Data successfully updated", "new_key": new_key["key"]}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@app.get("/get-job")
async def get_all_jobs():
    try:
        res = await db.fetch({})
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
        print(e)
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@app.delete("/delete-job/{key}")
async def delete_job(key: str = None):
    try:
        if not key:
            return {"message": "No key provided"}

        await db.delete(key)
        return {"message": f"Succesfully removed {key}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")
