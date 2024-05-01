FROM ger-is-registry.caas.intel.com/hpc-middleware/python:3.8-slim-buster
LABEL maintainer="The Swiss Cloud Platform team <hpc.middleware.common.software@intel.com>"

ENV http_proxy=http://proxy-dmz.intel.com:911
ENV https_proxy=http://proxy-dmz.intel.com:912
ENV no_proxy=.intel.com,127.0.0.1,localhost

EXPOSE 8000

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1

RUN chmod 777 /tmp

RUN apt-get update && apt-get -yqq install build-essential bash git tmux curl vim dnsutils krb5-user libpam-krb5 python3-kerberos gcc libkrb5-dev python3-dev libffi-dev libssl-dev libldap2-dev libsasl2-dev && apt-get clean && rm -rf /var/lib/apt/lists/*


RUN curl http://certificates.intel.com/repository/certificates/IntelSHA256RootCA-Base64.crt  > /etc/ssl/certs/ca-certificates.crt

# Remove the old Go package if it exists
# RUN apt-get remove -y golang

# Set the Go version
ENV GO_VERSION 1.17.2

# Download and install the latest Go
RUN curl -LO https://dl.google.com/go/go${GO_VERSION}.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz \
    && rm go${GO_VERSION}.linux-amd64.tar.gz

# Add Go to the PATH
ENV PATH $PATH:/usr/local/go/bin



# create root directory for our project in the container
RUN mkdir /app
RUN chmod 777 /app

# COPY ./docker-entrypoint.sh /
# RUN chmod 755 /docker-entrypoint.sh

# Install any needed packages specified in requirements.txt
RUN set -o vi

# Copying requirements on its own so that it can be cached in builds
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/
RUN cp /app/.tmux.conf /root/.tmux.conf

# RUN cat /tmp/IntelSHA256RootCA.crt > /app/ssl/IntelSHA256RootCA-Base64.crt
# ENV SSL_CERT_FILE /app/ssl/IntelSHA256RootCA-Base64.crt

ENTRYPOINT ["/app/ijira.py"]
# CMD []