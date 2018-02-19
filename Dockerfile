
FROM alpine:3.7

# Adapted from https://github.com/frol/docker-alpine-python3/blob/master/Dockerfile
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

WORKDIR /opt/swd

COPY src /opt/swd
COPY requirements.txt /opt/swd
RUN pip install -r /opt/swd/requirements.txt
RUN chmod +x /opt/swd/fetch_and_set.py

# Define default command.
CMD ["/opt/swd/fetch_and_set.py"]
