# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

# 1. Create a non-privileged user and group
# We use -m to create a home directory and -s to set a non-login shell
RUN groupadd -r securitytest && useradd -r -g securitytest -m -s /sbin/nologin flaskuser

WORKDIR /app

# 2. Copy and install requirements as root (to allow global lib access)
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# 3. Copy application files
COPY . .

# 4. Change ownership of the app directory to our new user
RUN chown -R flaskuser:securitytest /app

# 5. Switch to the non-privileged user
USER flaskuser

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
