import requests
import jwt
import os
from dynaconf import Dynaconf

# Server URL
SERVER_URL = "http://localhost:8080/generate_report"

# JWT secret key (must match the server's SECRET_KEY)
SECRET_KEY = "your_secret_key"


# Generate a JWT token
def generate_token(username, password):
    payload = {"user": username, "password": password, "role": "admin"}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


# Make a GET request to the server
def make_request(username, password):
    token = generate_token(username, password)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(SERVER_URL, headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Error:", response.status_code, response.json())
    except Exception as e:
        print("An error occurred:", str(e))


# Add functionality to download the report.pdf
def download_report(username, password):
    token = generate_token(username, password)
    headers = {"Authorization": f"Bearer {token}"}
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(downloads_dir, exist_ok=True)
    file_path = os.path.join(downloads_dir, "report.pdf")
    try:
        response = requests.get(
            f"{SERVER_URL}/../download_report", headers=headers, stream=True
        )
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Report downloaded successfully as '{file_path}'.")
        else:
            print("Error:", response.status_code, response.json())
    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":

    # Load credentials from .secrets.toml
    settings = Dynaconf(
        settings_files=[".secrets.toml"], environments=True, env="default"
    )
    print("Loaded settings:", settings.as_dict())

    username = settings.username
    password = settings.password

    print("1. Generate Report")
    print("2. Download Report")
    choice = input("Enter your choice: ")

    if choice == "1":
        make_request(username, password)
    elif choice == "2":
        download_report(username, password)
    else:
        print("Invalid choice.")
