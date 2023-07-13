# DRF Log Tester
간단한 DRF를 Docker로 구성하고, APP에서 발생하는 로그를 File로 남깁니다. 또한 이를 Filebeat를 이용하여 Elasticsearch 혹은 Logstash로 전송하여 로그를 확인할 수 있는 실습 예제를 개발하였습니다.

## Requirements

* [Docker Engine](https://docs.docker.com/install/) version **18.06.0** or newer
* [Docker Compose](https://docs.docker.com/compose/install/) version **1.26.0** or newer
* 1.5 GB of RAM

적절한 셋업을 위해 아래의 포트를 사용 중인지 여부를 체크해주시기 바랍니다.

* 5044: Logstash Beats input
* 5000: Logstash TCP input
* 9600: Logstash monitoring API
* 9200: Elasticsearch HTTP
* 9300: Elasticsearch TCP transport
* 5601: Kibana

## Set-Up

### ELK

docker-compose 내에 세팅된 docker network를 셋업해주도록 합니다.
```console
$ ./docker-network.sh
```

Elasticsearch 셋업을 위해 docker-compose를 이용하여 elasticsearch를 구동합니다. 
```console
$ docker-compose -f ./elk/docker-compose.yml up elasticsearch --build
```

이후 셋업 빌드를 진행합니다.
```console
$ docker-compose -f ./elk/docker-compose.yml up setup --build
```

setup 빌드가 완료되었으면 ELK와 filebeat 로그를 재시작해줍니다. 
```console
$ docker-compose -f ./elk/docker-compose.yml stop && docker-compose -f ./elk/docker-compose.yml up -d
```

### APP
테스트를 위한 DRF 웹 앱을 실행하기 위해 다음과 같은 명령어로 docker를 실행시켜줄 수 있습니다.
```console
$ docker-compose -f ./app/docker-compose.yml up -d
```

## Reset
셋업한 Docker를 리셋하기 위해 다음과 같은 작업이 필요합니다.

1. docker-compose 명령어를 이용하여 docker를 종료합니다.
   ```console
   $ docker-compose down -v
   $ docker container prune( or docker rm `container_name`)
   ```
2. ./elk/elasticsearch/nodes
3. app의 database 데이터를 삭제할 경우 ./app/db.sqlite3 데이터를 삭제합니다.

