# --- Build ---
FROM python:3.6 AS base
WORKDIR /GitDiaryBot
COPY . /GitDiaryBot
RUN pip install wheel
RUN python setup.py bdist_wheel

# --- Run ---
FROM python:3.6 AS release  
WORKDIR /GitDiaryBot

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED true

RUN apt-get -qqy update                 \
    && apt-get -y install               \
       git                              \
    && apt-get clean                    \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=base /GitDiaryBot/dist/*.whl ./

RUN python3.6 -m pip install --no-cache-dir *.whl

ENTRYPOINT ["GitDiaryBot"]
