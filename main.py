from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from github import Github
from github.GithubException import GithubException
from dotenv import load_dotenv
import os, base64

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# GitHub config
g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(f"{os.getenv('REPO_OWNER')}/{os.getenv('REPO_NAME')}")
branch = os.getenv("REPO_BRANCH", "main")


def list_markdown_files(path=""):
    files = []
    contents = repo.get_contents(path, ref=branch)
    for content in contents:
        if content.type == "file" and content.name.endswith(".md"):
            files.append(content.path)
        elif content.type == "dir":
            files.extend(list_markdown_files(content.path))
    return files


@app.get("/", response_class=HTMLResponse)
def show_editor(request: Request, file: str = ""):
    file_list = list_markdown_files()
    content = ""
    error = None

    if file:
        try:
            remote_file = repo.get_contents(file, ref=branch)
            content = base64.b64decode(remote_file.content).decode("utf-8")
        except GithubException as e:
            error = f"Error loading {file}: {e.data.get('message', 'Unknown error')}"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "file": file,
        "file_list": file_list,
        "content": content,
        "error": error
    })


@app.post("/save")
def save_markdown(
    request: Request,
    file: str = Form(...),
    content: str = Form(...)
):
    try:
        existing = repo.get_contents(file, ref=branch)
        repo.update_file(
            path=file,
            message=f"Update {file} from Web UI",
            content=content,
            sha=existing.sha,
            branch=branch
        )
    except GithubException:
        # File doesn't exist, so we create it
        repo.create_file(
            path=file,
            message=f"Create {file} from Web UI",
            content=content,
            branch=branch
        )
    return RedirectResponse(url=f"/?file={file}", status_code=303)
