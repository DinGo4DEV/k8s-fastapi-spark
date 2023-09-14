FROM apache/spark-py

ARG VERSION=latest
ARG ARTIFACT=apache/spark-py
ARG HOST="docker.io"
ARG WORKDIR=/src

FROM --platform=linux/amd64 $HOST/$ARTIFACT:$VERSION 
EXPOSE 8080
EXPOSE 4040

USER 0

RUN rm -f /etc/localtime \
&& ln -sv /usr/share/zoneinfo/Hongkong /etc/localtime \
&& echo "Hongkong" > /etc/timezone

RUN alias python=python3 && alias pip=pip3

WORKDIR $WORKDIR

COPY pyproject.toml pdm.lock $WORKDIR/

RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable

ENV PATH="$PATH:/__pypackages__/3.11/Scripts"

COPY . .
RUN chgrp -R 0 $WORKDIR && chmod -R g=u $WORKDIR
USER 1001

ENV root_path="/"

CMD ["sh","-c","pdm run start_server --host 0.0.0.0 --port 8080 --workers 2 --root-path $root_path"]