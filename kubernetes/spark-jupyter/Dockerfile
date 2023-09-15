FROM python:3.11.5

ARG SPARK_VER=3.4.0

WORKDIR /root

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    apt-get clean && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Install a base time build environment
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	apt-utils \
	build-essential \
	curl \
	git \
	libpng-dev \
	libfreetype6-dev \
	pkg-config \
	software-properties-common \
	sudo \
	tar \
	unzip \
	wget \
	vim && \
    apt-get clean && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*


# Install python3 infrastructure
COPY requirements.txt .
RUN pip3 --no-cache-dir install -r requirements.txt && rm -f requirements.txt

# Install Spark dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	openjdk-17-jre \
	scala && \
	apt-get clean && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Install Spark
RUN wget -q -O spark.tgz http://mirror.olnevhost.net/pub/apache/spark/spark-${SPARK_VER}/spark-${SPARK_VER}-bin-hadoop3.tgz && \
	mkdir -p /usr/local && tar -xf spark.tgz -C /usr/local && \
	mv /usr/local/spark*${SPARK_VER}* /usr/local/spark && \
    	pip3 install --upgrade pyspark

RUN cd /usr/local/spark/jars \
 && wget "https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar

RUN cd /usr/local/spark/jars \
 && wget "https://repo1.maven.org/maven2/com/arangodb/arangodb-spark-datasource-3.4_2.13/1.5.0/arangodb-spark-datasource-3.4_2.13-1.5.0.jar"

RUN cd /usr/local/spark/jars \
 && wget "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.6/hadoop-aws-3.3.6.jar"


# Clean up
RUN rm -rf /root/* && chmod 755 /root

RUN jupyter notebook --generate-config
RUN sed -i -E 's,^#\s*c.NotebookApp.terminado_settings.*,c.NotebookApp.terminado_settings = {"shell_command" : ["\/bin\/bash"]},g' ~/.jupyter/jupyter_notebook_config.py

# Setup password authentication so we don't have to remember tokens (password: "jupyter")
RUN echo "{ \"NotebookApp\": { \"password\": \"sha1:ad16e87de314:a02efac10ccd7ead24e845f438b2b87fe8bc2d0f\" } }" >> ~/.jupyter/jupyter_notebook_config.json
RUN mkdir -p ~/.ipython/profile_default
RUN echo "c.TerminalInteractiveShell.editing_mode = 'vi'" >> ~/.ipython/profile_default/ipython_config.py

# Required spark configuration for local user access
ENV SPARK_HOME=/usr/local/spark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
ENV PYTHONPATH=/usr/local/spark/python:/usr/local/spark/python/lib/py4j-0.10.7-src.zip
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/spark/bin

EXPOSE 4040 4041 8080 8888 2222

CMD ["notebook", "--no-browser", "--allow-root", "--ip=0.0.0.0", "--port=8888"]
ENTRYPOINT ["/usr/local/bin/jupyter"]