import requests, json
import logging


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
        "icon": "nginx",
        "pricingUrl": "https://www.whatap.io/ko/pricing/#server-space",
        "summary": {
            "ko": "Nginx 모니터링을 통해 웹 서버의 성능을 실시간으로 추적하고 분석하세요. 트래픽 패턴을 모니터링하고, 비정상적인 활동을 빠르게 감지하여 서비스 품질을 유지할 수 있습니다. Nginx 대시보드로 웹서버 성능을 한눈에 파악하세요.",
            "ja": "Nginxのモニタリングにより、ウェブサーバーのパフォーマンスをリアルタイムで追跡・分析できます。トラフィックのパターンを監視し、異常なアクティビティを迅速に検知してサービスの品質を維持しましょう。Nginxダッシュボードで、ウェブサーバーのパフォーマンスを一目で把握できます。",
            "en": "With Nginx monitoring, track and analyze your web server's performance in real time. Monitor traffic patterns and quickly detect abnormal activities to maintain service quality. Gain a comprehensive view of your web server's performance through the Nginx dashboard."
        }
    },
    "releaseEnvs": ["DEV", "PREVIEW", "SERVICE"]
    }


    return json.dumps(metadata)

def writeMeta():
    with open('meta.json','w') as f:
        f.write(getMetaJson())
    body = {
        "platform":"INFRA",
        "textKey":"NGINX_RC_ONE",
        "name":"NGINX",
        "description":"NGINX BETA RC 1015",
        "status":"open"
        }
    with open('main.json','w') as f:
        f.write(json.dumps(body))


if __name__ == '__main__':
    writeMeta()
