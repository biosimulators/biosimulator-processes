# TODO: Use a more specific tag instead of latest for reproducibility
FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive \
    XVFB_RES="1920x1080x24" \
    XVFB_ARGS="" \
    PATH="/app/.venv/bin:$PATH" \
    CONFIG_ENV_FILE="/app/config/config.env" \
    SECRET_ENV_FILE="/app/secret/secret.env" \
    STORAGE_GCS_CREDENTIALS_FILE="/app/secret/gcs_credentials.json" \
    STORAGE_LOCAL_CACHE_DIR="/app/scratch"

WORKDIR /app

# copy and make dirs
COPY ./biosimulator_processes/processes /app/biosimulator_processes
COPY ./notebooks /app/notebooks

# copy files
COPY ./pyproject.toml ./poetry.lock ./data ./scripts/trust-notebooks.sh /app/
COPY ./scripts/xvfb-startup.sh /xvfb-startup.sh

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10  \
    python3-pip  \
    build-essential  \
    libncurses5  \
    cmake  \
    make  \
    libx11-dev  \
    libc6-dev  \
    libx11-6  \
    libc6  \
    gcc  \
    swig \
    pkg-config  \
    curl  \
    tar  \
    libgl1-mesa-glx  \
    libice6  \
    libpython3.10  \
    wget  \
    xvfb \
    && mkdir /tmp/.X11-unix  \
    && chmod 1777 /tmp/.X11-unix  \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip && pip install poetry \
    && poetry config virtualenvs.in-project true \
    && poetry install \
    && chmod +x /app/trust-notebooks.sh \
    && /app/trust-notebook.sh

# RUN useradd -m -s /bin/bash jupyteruser && chown -R jupyteruser:jupyteruser /app

# USER jupyteruser

# RUN chmod +x /app/notebooks

VOLUME /app/data

CMD ["poetry", "run", "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
