FROM resin/rpi-raspbian:buster AS base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# start cross build
RUN [ "cross-build-start" ]

# system deps:
RUN apt-get update -qq -y \
    && apt-get install sudo \
    curl \
    git \
    python \
    python-pip \
    python-dev \
    python-all-dev \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-opencv \
    python3-dev \
    pigpio \
    pipenv \
    virtualenv \
    gcc \
    make \
    musl-dev \
    libevent-dev \
    libatlas-base-dev \
    libhdf5-dev \
    libhdf5-serial-dev \
    libjasper-dev \
    libqtgui4 \
    libqt4-test \
    libilmbase-dev \
    libopenexr-dev \
    libgstreamer1.0-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libwebp-dev \
    && python3 -m pip install --upgrade pip setuptools wheel \
    && git clone git://github.com/yyuu/pyenv.git ~/.pyenv 

COPY Pipfile .
COPY Pipfile.lock .
RUN READTHEDOCS=True \
    PIPENV_VENV_IN_PROJECT=1 \
    pipenv install --dev --deploy --ignore-pipfile

RUN [ "cross-build-end" ]


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$HOME/.local/bin:$HOME/.venv/bin:$PATH

# Create and switch to a new user

# Install application into container
COPY . .

# project initialization 
RUN sudo pigpiod

# Run the application
EXPOSE 8000
ENTRYPOINT ['python3', 'aidriv/app.py']
