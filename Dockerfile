# syntax=docker/dockerfile:1

FROM python:3.11-slim-bookworm

# 1. Install basic networking utilities (curl, ping, netcat, net-tools)
RUN apt-get update && apt-get install -y \
    iputils-ping \
    curl \
    net-tools \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 2. Create a non-privileged user and group
# We use -m to create a home directory and -s to set a non-login shell
RUN groupadd -r securitytest && useradd -r -g securitytest -m -s /sbin/nologin flaskuser

WORKDIR /app

# 3. Add AWS mock credentials as environment variables
ENV AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
    AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
    AWS_DEFAULT_REGION=us-west-2
    
# 4. Copy and install requirements as root (to allow global lib access)
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# 5. Copy application files
COPY . .

# 6. Change ownership of the app directory to our new user
RUN chown -R flaskuser:securitytest /app

# 7. Switch to the non-privileged user
USER flaskuser

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
