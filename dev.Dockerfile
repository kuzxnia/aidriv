FROM resin/rpi-raspbian:buster

ENV DEBIAN_FRONTEND noninteractive

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
    pipenv -qq -y \
    make \
    gcc \
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


ENV HOME /home/app
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$HOME/.local/bin:$PATH

# copy and change working directory
WORKDIR /home/app
COPY . $HOME

# project initialization 
RUN READTHEDOCS=True pipenv install --dev --deploy --ignore-pipfile \
        && sudo pigpiod

RUN [ "cross-build-end" ]

EXPOSE 8000
CMD ['pipenv', 'run', 'python3', 'aidriv/app.py']
