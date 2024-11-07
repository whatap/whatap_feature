#!/bin/bash
# Check if at least two arguments are not provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <license> <whatap.server.host>"
    exit 1
fi
# Assign arguments to variables
LICENSE=$1
WHATAP_SERVER_HOST=$2

# Function for Ubuntu
install_ubuntu() {
    echo "Installing for Ubuntu..."
    wget https://repo.whatap.io/debian/release.gpg -O - |  apt-key add -
    
    wget https://repo.whatap.io/debian/whatap-repo_1.0_all.deb -O whatap-repo_1.0_all.deb
     dpkg -i whatap-repo_1.0_all.deb
    if [[ $? -ne 0 ]]; then
        echo "Failed to add whatap respoistory. check your permissions."
        exit 1
    fi
     apt-get update
     apt-get install whatap-infra
}

# Function for CentOS/RedHat/Rocky
install_centos_redhat_rocky() {
    echo "Installing for CentOS/RedHat/Rocky..."
     rpm --import https://repo.whatap.io/centos/release.gpg
     rpm -Uvh https://repo.whatap.io/centos/5/noarch/whatap-repo-1.0-1.noarch.rpm
     if [[ $? -ne 0 ]]; then
        echo "Failed to add whatap respoistory. check your permissions."
        exit 1
    fi
     yum install whatap-infra
}

# Function for Amazon Linux
install_amazon_linux() {
    echo "Installing for Amazon Linux..."
    rpm --import https://repo.whatap.io/centos/release.gpg
    
    echo "[whatap]" |  tee /etc/yum.repos.d/whatap.repo > /dev/null
    echo "name=whatap packages for enterprise linux" |  tee -a /etc/yum.repos.d/whatap.repo > /dev/null
    echo "baseurl=https://repo.whatap.io/centos/latest/\$basearch" |  tee -a /etc/yum.repos.d/whatap.repo > /dev/null
    echo "enabled=1" |  tee -a /etc/yum.repos.d/whatap.repo > /dev/null
    echo "gpgcheck=0" |  tee -a /etc/yum.repos.d/whatap.repo > /dev/null
    if [[ $? -ne 0 ]]; then
        echo "Failed to add whatap respoistory. check your permissions."
        exit 1
    fi
    yum install whatap-infra

}


create_license(){

    cat <<EOF > /usr/whatap/infra/TELEGRAF_MIT_LICENSE.txt
The MIT License (MIT)

Copyright (c) 2015-2024 InfluxData Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

}

# Download Telegraf binary and Jolokia JAR
download_dependencies() {
    echo "Downloading Telegraf binary..."

    # Determine OS architecture
    ARCH=$(uname -m)
    case $ARCH in
        arm64|aarch64)
            TELEGRAF_URL="http://repo.whatap.io/telegraf/latest/arm64/telegraf"
            ;;
        amd64|x86_64)
            TELEGRAF_URL="http://repo.whatap.io/telegraf/latest/amd64/telegraf"
            ;;
        *)
            echo "Unsupported architecture: $ARCH"
            exit 1
            ;;
    esac

    feature_prefix=/usr/whatap/infra/feature
    mkdir -p $feature_prefix
    # Download Telegraf
    wget $TELEGRAF_URL -O $feature_prefix/telegraf
    chmod +x $feature_prefix/telegraf
    
}

test_nginx_status() {
    response=$(curl -s -o /dev/null -w "%{http_code}" -X GET -H "Content-Type: text/xml" \
        "$nginx_status_url")

    if [[ "$response" == "200" ]]; then
        return 0
    else
        return 1
    fi
}

configure_nginx(){
# 기본 Nginx 설정 디렉토리
DEFAULT_PREFIX="/etc/nginx"
DEFAULT_PORT=30080

# 사용자에게 Nginx 설정 파일 경로 입력 받기
read -p "Enter Nginx configuration prefix [${DEFAULT_PREFIX}]: " NGINX_PREFIX
NGINX_PREFIX=${NGINX_PREFIX:-$DEFAULT_PREFIX}

# 사용자에게 Nginx status 포트 입력 받기
read -p "Enter port for Nginx status page [${DEFAULT_PORT}]: " NGINX_STATUS_PORT
NGINX_STATUS_PORT=${NGINX_STATUS_PORT:-$DEFAULT_PORT}

# Nginx 상태 설정 추가
STATUS_CONFIG=$(cat <<EOF
    server {
        listen ${NGINX_STATUS_PORT};
        server_name localhost;

        location /nginx_status {
            stub_status;
            allow 127.0.0.1;   # Allow local access
            deny all;          # Deny all other access
        }
    }
EOF
)

# 분석용 로그 설정 추가
LOG_CONFIG=$(cat <<'EOF'
    log_format whatap_format '$remote_addr - $remote_user [$time_local] ' 
                             '"$request" $status $body_bytes_sent ' 
                             '"$http_referer" "$http_user_agent" ' 
                             '"$server_name" $upstream_addr ' 
                             '$request_time';

    access_log /var/log/nginx/whatap.log whatap_format;
EOF
)

# nginx.conf 파일 경로 설정
NGINX_CONF="${NGINX_PREFIX}/nginx.conf"

# 백업 파일 만들기 (현재 날짜와 시간을 파일명에 추가)
BACKUP_FILE="${NGINX_CONF}_backup_$(date +%Y%m%d_%H%M%S)"
echo "Backing up the current configuration to ${BACKUP_FILE}..."
cp "$NGINX_CONF" "$BACKUP_FILE"

# nginx.conf.whatap 파일 작성
WHATAP_CONF="${NGINX_CONF}.whatap"
echo "Creating new configuration file: ${WHATAP_CONF}"

# 임시 파일 사용해서 설정 추가하기
{
    while IFS= read -r line; do
        echo "$line"
        if [[ "$line" == *"http {"* ]]; then
            # http 블록 안에 필요한 설정 추가
            if ! grep -q "stub_status" "$NGINX_CONF"; then
                echo "$STATUS_CONFIG"
            fi
            if ! grep -q "whatap_format" "$NGINX_CONF"; then
                echo "$LOG_CONFIG"
            fi
        fi
    done < "$NGINX_CONF"
} > "$WHATAP_CONF"

echo "Configuration file ${WHATAP_CONF} created successfully."

# Nginx 재시작 안내
read -p "Replace the original ${NGINX_PREFIX}/nginx.conf with ${NGINX_PREFIX}/nginx.conf.whatap and restart nginx.[ENTER]: " CONFIRM

}

configure_telegraf() {
    configure_nginx
    
    while true; do
        read -p "Enter nginx status url[http://localhost:$NGINX_STATUS_PORT/nginx_status]: " nginx_status_url
        nginx_status_url=${nginx_status_url:-http://localhost:$NGINX_STATUS_PORT/nginx_status}
        
        if test_nginx_status; then
            echo "nginx status successful."
            break
        else
            echo "Failed to connect to nginx status. Please check your inputs and try again."
            
        fi        
    done

    telegraf_config=/usr/whatap/infra/conf/telegraf.d
    mkdir -p $telegraf_config

    cat <<EOF > $telegraf_config/nginx.conf
[global_tags]
[agent]
interval = "10s"
round_interval = true
metric_batch_size = 10000
metric_buffer_limit = 100000
collection_jitter = "0s"
flush_interval = "10s"
flush_jitter = "0s"
logtarget = "stderr"
omit_hostname = true

[[inputs.nginx]]
  ## An array of Nginx Plus status URIs to gather stats.
  urls = ["$nginx_status_url"]

[[aggregators.basicstats]]
  period = "10s"

  stats = ["diff"]
  namepass = ["nginx"]


[[inputs.tail]]
  name_override = "nginxlog"
  files = ["/var/log/nginx/whatap.log"]
  from_beginning = false
  pipe = false
  data_format = "grok"
  grok_patterns = ["%{NGINX_LOG_FORMAT}"]
  grok_custom_patterns = '''
      NGINX_LOG_FORMAT %{COMMON_LOG_FORMAT} %{QS:referrer} %{QS:agent} %{NOTSPACE:domain} %{NOTSPACE:upstream} %{NUMBER:latency:float}
      COMMON_LOG_FORMAT %{IPORHOST:client_ip} %{USER:ident} %{USER:auth} \[%{HTTPDATE:timestamp}\] "(?:%{WORD:verb} %{NOTSPACE:request}(?: HTTP/%{NUMBER:httpversion})?|%{DATA:rawrequest})" %{NUMBER:response} (?:%{NUMBER:bytes:int}|-)
  '''

[[processors.converter]]
  namepass = ["nginxlog"]

  ## 필드를 태그로 변환
  [processors.converter.fields]
    tag = ["domain", "upstream"]

[[aggregators.valuecounter]]
  namepass = ["nginxlog"]
  fields = ["response", "verb"]
  drop_original = true

  tagpass = ["domain", "upstream"]

[[inputs.tail]]
  name_override = "nginxlog_throughput"
  files = ["/var/log/nginx/whatap.log"]
  from_beginning = false
  pipe = false
  data_format = "grok"
  grok_patterns = ["%{NGINX_LOG_FORMAT}"]
  grok_custom_patterns = '''
      NGINX_LOG_FORMAT %{COMMON_LOG_FORMAT} %{QS:referrer} %{QS:agent} %{NOTSPACE:domain} %{NOTSPACE:upstream} %{NUMBER:latency:float}
      COMMON_LOG_FORMAT %{IPORHOST:client_ip} %{USER:ident} %{USER:auth} \[%{HTTPDATE:timestamp}\] "(?:%{WORD:verb} %{NOTSPACE:request}(?: HTTP/%{NUMBER:httpversion})?|%{DATA:rawrequest})" %{NUMBER:response} (?:%{NUMBER:bytes:int}|-)
  '''

[[processors.converter]]
  namepass = ["nginxlog_throughput"]

  ## 필드를 태그로 변환
  [processors.converter.fields]
   tag = ["domain", "upstream"]

[[aggregators.basicstats]]
  period = "10s"
  drop_original = true
  stats = ["sum","mean"]
  namepass = ["nginxlog_throughput"]
  fieldpass = ["bytes", "latency"]

EOF
}


# Common configuration for all distributions
configure_agent() {
    echo "Configuring Whatap Agent..."
    echo "license=$LICENSE" | tee /usr/whatap/infra/conf/whatap.conf
    echo "whatap.server.host=$WHATAP_SERVER_HOST" | tee -a /usr/whatap/infra/conf/whatap.conf
    echo "createdtime=`date +%s%N`" |  tee -a /usr/whatap/infra/conf/whatap.conf

    echo "internal.forwarder.enabled=true" |  tee -a /usr/whatap/infra/conf/whatap.conf
    echo "telegraf.sidecar.enabled=true" |  tee -a /usr/whatap/infra/conf/whatap.conf
    echo "telegraf.sidecar.executable=$feature_prefix/telegraf" |  tee -a /usr/whatap/infra/conf/whatap.conf

    service whatap-infra restart
}



# Detect the distribution
. /etc/os-release
echo "os ID: $ID"
case $ID in
    ubuntu)
        install_ubuntu
        ;;
    centos|rhel|rocky)
        install_centos_redhat_rocky
        ;;
    amzn)
        install_amazon_linux
        ;;
    *)
        echo "Unsupported Linux distribution."
        exit 1
        ;;
esac


create_license
download_dependencies
configure_telegraf
configure_agent