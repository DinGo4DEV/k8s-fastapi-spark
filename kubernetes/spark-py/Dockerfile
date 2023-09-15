FROM apache/spark-py:v3.4.0
USER 0
COPY *.jar /opt/spark/jars/
RUN rm /opt/spark/jars/kubernetes-*-6.4.1.jar
