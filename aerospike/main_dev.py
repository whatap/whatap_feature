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
            "icon": "aerospike",
            "pricingUrl": "https://www.whatap.io/ko/pricing/#server-space",
            "summary": {
                "ko": "Aerospike 모니터링 에이전트는 NoSql 데이터베이스 성능과 안정성을 실시간으로 추적하고 분석할 수 있도록 도와줍니다. 이 에이전트는 주요 지표를 수집하고 시각화하여 문제를 신속하게 감지하고 해결할 수 있게 합니다. 다양한 알림 설정을 통해 시스템 이상 발생 시 즉각적인 조치가 가능합니다. 또한, 사용자는 에이전트를 통해 리소스 사용량을 최적화하고 시스템 효율성을 극대화할 수 있습니다. Aerospike 모니터링 에이전트는 기업의 데이터 인프라 관리에 필수적인 도구입니다.",
                "en": "Aerospike is a high-performance NoSQL database known for ultra-fast performance and high scalability. The Aerospike agents monitor key metrics to ensure reliable operation. By tracing the CPU, memory, and storage usage in real time, they prevent overload and errors, and monitor the numbers of read and write operations to detect performance bottlenecks early as possible. They manage the network traffic to prevent traffic issues from happening, and allow you to take immediate actions when system failures occur through various notification settings. With those features, maximize the Aerospike's performance and ensure operational stability.",
                "ja": "Aerospikeは、超高速性能と高い拡張性が特徴の高性能NoSQLデータベースです。Aerospikeエージェントは、安定した運用のために主なメトリクスをモニタリングします。 CPU、メモリ、ストレージの使用量をリアルタイムで追跡して過負荷とエラーを防止し、読み取りと書き込みの作業数をモニタリングしてパフォーマンスのボトルネックを早期に発見します。 ネットワークトラフィックを管理してトラフィックの問題を予防し、様々な通知設定により、システムに異常が発生した場合、直ちに措置を取れます。Aerospikeの性能を最大化し、運用の安定性を確保してください。",
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
    "textKey":"AEROSPIKE_RC_ONE",
    "name":"Aerospike",
    "description":"Aerospike BETA RC 0604",
    "status":"beta"}
    with open('main.json','w') as f:
        f.write(json.dumps(body))

if __name__ == '__main__':
    writeMeta()

