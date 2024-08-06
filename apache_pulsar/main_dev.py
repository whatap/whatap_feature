import requests, json
import logging

# Enable debug logging for requests

from http.client import HTTPConnection, HTTPSConnection
HTTPConnection.debuglevel = 1
HTTPSConnection.debuglevel = 1


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error reading file: {e}"

def getMetaJson():
    metadata = {
        "desc": {
            "icon": "pulsar",
            "pricingUrl": "https://www.whatap.io/ko/pricing/#server-space",
            "summary": {
                "ko": "Apache Pulsar 모니터링 제품은 Pulsar 클러스터의 성능과 상태를 실시간으로 추적할 수 있게 해줍니다. 메트릭, 로그, 트레이스를 수집하고 시각화하여 문제를 빠르게 식별하고 대응할 수 있습니다. 주요 메트릭에는 메시지 게시 및 소비 속도, 구독 백로그, 스토리지 사용량 등이 포함됩니다. 와탭 Apache Pulsar 모니터링을 통해 효율적인 모니터링과 경고 설정이 가능합니다.",
                "en": "Apache Pulsar monitoring products enable real-time tracking of the performance and health of Pulsar clusters. They collect and visualize metrics, logs, and traces to quickly identify and respond to issues. Key metrics include message publish and consume rates, subscription backlogs, and storage usage. Efficient monitoring and alerting can be achieved through integrated tools like Whatap Apache Pulsar Monitoring."
            }
        },
        "releaseEnvs": ["DEV", "PREVIEW", "SERVICE"]
        #"releaseEnvs": ["DEV"]
    }

    return json.dumps(metadata)

def writeMeta():
    with open('meta.json','w') as f:
        f.write(getMetaJson())
    body = {
    "platform":"INFRA",
    "textKey":"APACHEPULSAR_DEV_ONE",
    "name":"ApachePulsar",
    "description":"ApachePulsar BETA RC 0806",
    "status":"beta"}
    with open('main.json','w') as f:
        f.write(json.dumps(body))

if __name__ == '__main__':
    writeMeta()

