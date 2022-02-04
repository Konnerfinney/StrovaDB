import os
# from dotenv import load_dotenv

# load_dotenv()
c = {
  "type": "service_account",
  "project_id": "strovacoaching",
  "private_key_id": os.environ.get("private_key_id"),
  "private_key": os.environ.get("private_key").replace('\\n','\n'),
  "client_email": "strovacoaching@strovacoaching.iam.gserviceaccount.com",
  "client_id": os.environ.get("client_id"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/strovacoaching%40strovacoaching.iam.gserviceaccount.com"
}
