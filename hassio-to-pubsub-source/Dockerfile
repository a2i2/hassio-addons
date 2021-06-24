ARG BUILD_FROM
FROM $BUILD_FROM

# Install system dependencies.
RUN apk update && \
    apk add --no-cache \
       g++ \
       musl-dev \
       libffi-dev \
       python3-dev \
       py3-pip

# Install Python dependencies.
COPY requirements.txt /
RUN pip3 install --no-cache-dir -r /requirements.txt && \
  rm requirements.txt && \
  apk del \
    g++ \
    musl-dev \
    libffi-dev

# Copy source code.
COPY hass_to_pubsub.py /
COPY entityfilter.py /
COPY run.sh /

# Define entrypoint.
RUN chmod a+x /run.sh
CMD ["/run.sh"]
