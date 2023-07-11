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

docker-compose 내에 세팅된 docker network를 셋업해주도록 합니다.
```console
$ ./docker-network.sh
```

Elasticsearch 셋업을 위해 docker-compose를 이용하여 elasticsearch를 구동합니다. 
```console
$ docker-compose up elasticsearch
```

이후 셋업 빌드를 진행합니다.
```console
$ docker-compose up setup
```

셋업 완료 후 elasticsearch 내의 비밀번호를 수정해줘야 합니다. 이를 위해 다음 명령어를 실행하여 적절한 비밀번호를 생성해줍니다.
```console
$ docker-compose exec -T elasticsearch bin/elasticsearch-setup-passwords auto --batch

[ Output example ]
Changed password for user apm_system
PASSWORD apm_system = 7cFNjNwjQ0cRgGdeTqAw

Changed password for user kibana_system
PASSWORD kibana_system = l9iaccl0uUexUt0kCfy6

Changed password for user kibana
PASSWORD kibana = l9iaccl0uUexUt0kCfy6

Changed password for user logstash_system
PASSWORD logstash_system = bHCsOGLUWxKz63MbgXC4

Changed password for user beats_system
PASSWORD beats_system = 2IAzlFoyUGFVxz009Quj

Changed password for user remote_monitoring_user
PASSWORD remote_monitoring_user = jCK1xWmnjv9TDP97Ww52

Changed password for user elastic
PASSWORD elastic = o1naYvKFM8WtGGADGPFA
```

위 데이터를 `.env` 파일 내의 PASSWORD와 교체해주도록 합니다.

```console
docker-compose down && docker-compose up -d
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

