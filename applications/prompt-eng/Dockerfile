FROM dockerhub.containers.mpi-internal.com/python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install system deps separately to get advantage of docker caching layers better,
# we pass md5 hashes of files used as build arg to invalidate docker caches in a change
ARG PIP_CONF_MD5
ARG REQUIREMENTS_TXT_MD5
RUN --mount=type=secret,id=pip.conf,dst=/root/.pip/pip.conf \
    --mount=type=secret,id=requirements.txt,dst=/app/requirements.txt \
    pip --no-cache-dir install -r /app/requirements.txt

# wheel name has a required format, unfortunately it's not possible to use a variable in --mount parameter
# that's why we have cp command as a workaround below:
ARG WHEEL
ARG WHEEL_MD5
RUN --mount=type=secret,id=app.whl,dst=/app.whl \
    cp /app.whl /app/${WHEEL} \
    && pip --no-cache-dir install /app/${WHEEL} \
    && rm /app/${WHEEL}

COPY src/prompt_eng/streamlit_app.py streamlit_app.py
COPY .streamlit .streamlit

RUN pip install streamlit

ENTRYPOINT ["streamlit", "run", "streamlit_app.py"]