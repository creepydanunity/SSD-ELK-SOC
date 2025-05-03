FROM docker.elastic.co/elasticsearch/elasticsearch:7.10.0

RUN apt-get update && \
    apt-get install -y \
    openjdk-11-jdk \
    curl \
    git \
    sudo \
    geoip-database

COPY ./config/elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml

EXPOSE 9200
EXPOSE 9300

CMD ["elasticsearch"]
