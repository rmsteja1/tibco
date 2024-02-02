from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from http_client import HttpClient

app = FastAPI()


class CodeRequest(BaseModel):
    prompt: str


@app.post("/tibco_to_nlp")
def create_mule_project(request: CodeRequest):
    try:
        print(request.prompt)
        client = HttpClient()
        content = client.post(request.prompt)
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)
