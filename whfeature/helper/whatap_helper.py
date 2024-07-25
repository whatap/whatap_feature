import requests
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create a file handler for the log file
file_handler = logging.FileHandler('.debug.log')
file_handler.setLevel(logging.DEBUG)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Enable HTTPConnection debug level
logging.getLogger('urllib3').setLevel(logging.DEBUG)
logging.getLogger('urllib3').propagate = True

import requests
from bs4 import BeautifulSoup

import os
cookie_header = None
last_whatap_url = None
def save(username, whatap_url):
    """Save the username, password, and whatap_url to a file named .feature."""
    global last_whatap_url
    with open(".feature", "w") as file:
        file.write(f"username={username}\n")
        file.write(f"whatap_url={whatap_url}\n")
    last_whatap_url = whatap_url

def load():
    """Load the username, password, and whatap_url from a file named .feature."""
    if not os.path.exists(".feature"):
        return None, None
    
    with open(".feature", "r") as file:
        lines = file.readlines()
        properties = {}
        for line in lines:
            key, value = line.strip().split("=", 1)
            properties[key] = value
        
        username = properties.get("username")
        whatap_url = properties.get("whatap_url")
    
    global last_whatap_url
    last_whatap_url = whatap_url
    return username, whatap_url

def login(username, password, whatap_url):
    global cookie_header

    # 로그인 URL 구성
    login_url = whatap_url 
    if not login_url.endswith('/account/login'):
        login_url += '/account/login'
    # 세션 생성
    session = requests.Session()

    # 로그인 페이지 가져오기 (타임아웃 추가)
    response = session.get(login_url, timeout=10)
    response.raise_for_status()  # 오류 발생 시 예외 발생

    # 로그인 페이지 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 로그인 폼 찾기
    login_form = soup.find('form')
    if not login_form:
        raise ValueError("Login form not found")

    # CSRF 토큰 추출
    csrf_token = login_form.find('input', {'id': '_csrf'})
    if not csrf_token:
        raise ValueError("CSRF token not found")
    
    csrf_value = csrf_token['value']

    # 로그인 데이터 구성
    login_data = {
        'email': username,
        'password': password,
        '_csrf': csrf_value,
    }

    # x-www-form-urlencoded 형식으로 POST 요청 보내기
    response = session.post(login_url, data=login_data, timeout=10)
    
    # 응답이 302가 아닌 경우 오류 처리
    
    soup = BeautifulSoup(response.text, 'html.parser')
    error_list = soup.find('ul', {'class': 'errorlist'})
    if error_list:
        error_message = error_list.get_text(strip=True)
        raise Exception(f"Authentication error: {error_message}")
    
    # Set-Cookie 헤더에서 domain이 whatap.io인 쿠키 출력
    # for cookie in session.cookies:
    #     if 'whatap.io' in cookie.domain:
    #         print(f"Cookie value for domain 'whatap.io': {cookie.name}={cookie.value}")
    cookies = session.cookies.get_dict()
    cookie_header = '; '.join([f"{key}={value}" for key, value in cookies.items()])

    # print(f"Cookie header for new request: {cookie_header}")

    try:
        save(username, whatap_url)
    except:
        pass

    return True

def getFeatureAll(url_path = "/admin/api/feature/list"):
    global cookie_header, last_whatap_url

    url_getfeature = "{}{}".format(last_whatap_url, url_path)
    headers={"cookie":cookie_header}
    
    r = requests.get(url_getfeature, headers=headers)

    features = r.json()['data']
    if features:
        for feature in features:
            yield feature

def updateFeatureStatus(tk, status, url_path = "/admin/api/feature/update"):
    features = list(filter(lambda x: x['textKey']==tk, getFeatureAll()))
    if not features:
        raise Exception(f"feature {tk} not found error")

    feature = features[0]
    feature['status'] = status
    feature['document']=[]
    # for k,v in feature.items():
    #     logging.debug(f"feature {k}={v}")
    
    global cookie_header, last_whatap_url

    url_getfeature = "{}{}".format(last_whatap_url, url_path)
    headers={"cookie":cookie_header}
    
    r = requests.post(url_getfeature, headers=headers, json=feature)
    r.raise_for_status()

def uploadFeature(tk, feature):
    global cookie_header, last_whatap_url

    target_feature = dict()
    target_feature.update(feature)
    features = list(filter(lambda x: x['textKey']==tk, getFeatureAll()))
    
    if features:
        logger.debug(f'feature keys:{list(features[0].keys())}')
        source_feature = features[0]
        target_feature['id'] = source_feature['id']
        target_docs = target_feature['document']
        source_docs = source_feature['document']
        processed_document = []
        for doc in target_docs:
            doc_type = doc['type']
            if 'name' in doc:
                doc_name = doc['name']
                source_doc = list(filter(lambda x: x['type'] == doc_type and x['name'] == doc_name, source_docs))
            else:
                source_doc = list(filter(lambda x: x['type'] == doc_type, source_docs))
            if source_doc:
                doc['id'] = source_doc[0]['id']
            processed_document.append(doc)
        target_feature['document'] = processed_document
            
        global cookie_header, last_whatap_url

        url_getfeature = "{}{}".format(last_whatap_url, "/admin/api/feature/update")
        headers={"cookie":cookie_header}
        
        r = requests.post(url_getfeature, headers=headers, json=target_feature)
        r.raise_for_status()
    else:
        url_getfeature = "{}{}".format(last_whatap_url, "/admin/api/feature/create")
        headers={"cookie":cookie_header}
        logger.debug("="*80)
        logger.debug("uploadFeature ")
        for k, v in feature.items():
            if k != 'document':
                logger.debug(f'{k}={v}')
            else:
                for doc in v:
                    logger.debug("-"*20)
                    for key in doc.keys():
                        if key != 'data':
                            logger.debug(f'document {key}={doc[key]}')
                        else:
                            logger.debug(f'{doc[key][:40]} ...')

        r = requests.post(url_getfeature, headers=headers, json=feature)
        r.raise_for_status()

# 사용 예시
if __name__ == "__main__":
    username = "sa@whatap.io"
    password = "Wh@1410X12"
    whatap_url = "https://dev.whatap.io"

    login(username, password, whatap_url)
    for f in getFeatureAll():
        print(f['textKey'])
    