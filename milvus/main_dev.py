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
            "icon": "milvus-standalone",
            "pricingUrl": "https://www.whatap.io/ko/pricing/#server-space",
            "summary": {
                "ko": "와탭 Milvus 모니터링은 Milvus Vector Database의 성능과 상태를 실시간으로 확인할 수 있도록 도와줍니다. 다양한 지표와 대시보드를 통해 빠른 문제 식별과 효율적인 운영이 가능합니다. 다양한 이벤트 기능을 통해 시스템 상태를 사전에 파악하고 장애를 예방할 수 있습니다.",
                "en": "Whatap Milvus monitoring provides real-time insights into the performance and health of the Milvus Vector Database. It offers a wide range of metrics and dashboards for quick issue detection and efficient operations. Versatile event capabilities help you proactively track system health and prevent potential downtime. ",
                "ja": "Whatap Milvus モニタリングは、Milvus Vector Database のパフォーマンスと状態をリアルタイムで把握できます。多彩な指標とダッシュボードにより、迅速な問題の特定と効率的な運用が可能です。多彩なイベント機能を活用して、システムの状態を事前に把握し、障害を未然に防ぐことができます。",
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
    "textKey":"MILVUS_RC_ONE",
    "name":"Milvus",
    "description":"Milvus BETA RC 0806",
    "status":"beta"}
    with open('main.json','w') as f:
        f.write(json.dumps(body))

if __name__ == '__main__':
    writeMeta()

