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
            "icon": "apache-pulsar",
            "pricingUrl": "https://www.whatap.io/ko/pricing/#server-space",
            "summary": {
                "ko": "Apache Pulsar 모니터링 제품은 Pulsar 클러스터의 성능과 상태를 실시간으로 추적할 수 있게 해줍니다. 메트릭, 로그, 트레이스를 수집하고 시각화하여 문제를 빠르게 식별하고 대응할 수 있습니다. 주요 메트릭에는 메시지 게시 및 소비 속도, 구독 백로그, 스토리지 사용량 등이 포함됩니다. 와탭 Apache Pulsar 모니터링을 통해 효율적인 모니터링과 경고 설정이 가능합니다.",
                "en": "Apache Pulsar is an open source messaging and streaming platform that supports high performance, scalability, and multi-tenancy. The Pulsar agents trace the cluster status, metrics for each messaging and node, major topics, and backlogs in real time. By monitoring the key resource usage figures, they allow you to prevent resource overload and errors, and manage message rates and backlogs to detect performance bottlenecks early as possible. By monitoring the key resource usage figures, they allow you to prevent resource overload and errors, and manage message rates and backlogs to detect performance bottlenecks early as possible. You can optimize the Pulsar environment and keep the data flow smooth.",
                "ja": "Apache Pulsarは、高性能、拡張可能、マルチテナントをサポートするオープンソースメッセージングおよびストリーミングプラットフォームです。 Pulsarエージェントは、クラスターの状況、メッセージングおよびノード別のメトリクス、主なトピックおよびバックログをリアルタイムで追跡します。 主ななリソースの使用量をモニタリングしてリソースの過負荷とエラーを防止でき、メッセージの速度とバックログを管理してパフォーマンスのボトルネックを早期に発見します。 様々な通知設定により、システムに異常が発生した場合、直ちに措置を取れます。Pulsar環境を最適化し、データの流れを円滑に維持してください。",
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
    "textKey":"APACHEPULSAR_RC_ONE",
    "name":"ApachePulsar",
    "description":"ApachePulsar BETA RC 0806",
    "status":"beta"}
    with open('main.json','w') as f:
        f.write(json.dumps(body))

if __name__ == '__main__':
    writeMeta()

