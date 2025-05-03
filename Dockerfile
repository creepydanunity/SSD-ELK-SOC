FROM docker.elastic.co/elasticsearch/elasticsearch:8.9.0

COPY ./config/elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
EXPOSE 9200 9300
CMD ["elasticsearch"]
