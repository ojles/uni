FROM openjdk:8-jdk-alpine
VOLUME /tmp
ARG JAR_FILE
COPY target/${JAR_FILE} compute.jar
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.5.0/wait /wait
RUN chmod +x /wait
ENTRYPOINT /wait && java -Djava.security.egd=file:/dev/./urandom -jar /compute.jar \
