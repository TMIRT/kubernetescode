# syntax=docker/dockerfile:1

FROM python:3.11-slim-bookworm

# 1. Install basic networking utilities (curl, ping, netcat, net-tools)
RUN apt-get update && apt-get install -y \
    curl \
    iputils-ping \
    net-tools \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 2. Create a non-privileged user and group
# We use -m to create a home directory and -s to set a non-login shell
RUN groupadd -r securitytest && useradd -r -g securitytest -m -s /sbin/nologin flaskuser

WORKDIR /app

# 3. Copy and install requirements as root (to allow global lib access)
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# 4. Copy application files
COPY . .

# 5. Change ownership of the app directory to our new user
RUN chown -R flaskuser:securitytest /app

# 6. Switch to the non-privileged user
USER flaskuser

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
