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

test_apache_status() {
    response=$(curl -s -o /dev/null -w "%{http_code}" -X GET -H "Content-Type: text/xml" \
        "$server_status_url")

    if [[ "$response" == "200" ]]; then
        return 0
    else
        return 1
    fi
}

configure_apache(){
# 기본 Apache 설정 디렉토리
DEFAULT_PREFIX="/etc/httpd"

# 사용자에게 Apache 설정 파일 경로 입력 받기
read -p "Enter Apache configuration prefix [${DEFAULT_PREFIX}]: " APACHE_PREFIX
APACHE_PREFIX=${APACHE_PREFIX:-$DEFAULT_PREFIX}

# Apache 상태 설정 추가
STATUS_CONFIG=$(cat <<EOF
LoadModule status_module modules/mod_status.so

# 서버 상태를 보여주기 위한 설정 추가
<IfModule mod_status.c>
    <Location /server-status>
        SetHandler server-status
        Require local    # 로컬 액세스만 허용
    </Location>
    
    # ExtendedStatus를 활성화하면 더 많은 정보를 얻을 수 있습니다
    ExtendedStatus On
</IfModule>

LogFormat "%h %l %u [%{%d/%b/%Y:%H:%M:%S %z}t] \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %v %A %D" whatap_format
CustomLog /var/log/httpd/whatap.log whatap_format
EOF
)

# apache2.conf 파일 경로 설정
WHATAP_CONF="${APACHE_PREFIX}/conf.d/whatap.conf"
echo "$STATUS_CONFIG" > "$WHATAP_CONF"

echo "Configuration file ${WHATAP_CONF} created successfully."

# Apache 재시작 안내
read -p "Restart Apache and Press[ENTER]: " CONFIRM

}

configure_telegraf() {
    configure_apache
    
    while true; do
        read -p "Enter server status url[http://localhost/server-status]: " server_status_url
        server_status_url=${server_status_url:-http://localhost/server-status}
        
        if test_apache_status; then
            echo "Apache status successful."
            break
        else
            echo "Failed to connect to Apache status. Please check your inputs and try again."
            
        fi        
    done

    telegraf_config=/usr/whatap/infra/conf/telegraf.d
    mkdir -p $telegraf_config

    cat <<EOF > $telegraf_config/apache.conf
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

[[inputs.apache]]
  name_override = "apache"
  ## An array of Nginx Plus status URIs to gather stats.
  urls = ["http://localhost/server-status?auto"]

[[aggregators.basicstats]]
  period = "20s"

  stats = ["diff"]
  namepass = ["apache"]
  fieldpass = ["TotalAccesses", "TotalDuration", "TotalkBytes"]


[[inputs.tail]]
  name_override = "apachelog"
  files = ["/var/log/httpd/whatap.log"]
  from_beginning = false
  pipe = false
  data_format = "grok"
  grok_patterns = ["%{APACHE_LOG_FORMAT}"]
  grok_custom_patterns = '''
      APACHE_LOG_FORMAT %{COMMON_LOG_FORMAT} %{QS:referrer} %{QS:agent} %{NOTSPACE:domain} %{NOTSPACE:upstream} %{NUMBER:latency:float}
      COMMON_LOG_FORMAT %{IPORHOST:client_ip} %{USER:ident} %{USER:auth} \[%{HTTPDATE:timestamp}\] "(?:%{WORD:verb} %{NOTSPACE:request}(?: HTTP/%{NUMBER:httpversion})?|%{DATA:rawrequest})" %{NUMBER:response} (?:%{NUMBER:bytes:int}|-)
  '''

[[processors.converter]]
  namepass = ["aapchelog"]

  ## 필드를 태그로 변환
  [processors.converter.fields]
    tag = ["domain"]

[[aggregators.valuecounter]]
  namepass = ["apachelog"]
  fields = ["response", "verb"]
  drop_original = true

  tagpass = ["domain", "upstream"]

[[inputs.tail]]
  name_override = "apachelog_throughput"
  files = ["/var/log/httpd/whatap.log"]
  from_beginning = false
  pipe = false
  data_format = "grok"
  grok_patterns = ["%{APACHE_LOG_FORMAT}"]
  grok_custom_patterns = '''
      APACHE_LOG_FORMAT %{COMMON_LOG_FORMAT} %{QS:referrer} %{QS:agent} %{NOTSPACE:domain} %{NOTSPACE:upstream} %{NUMBER:latency:float}
      COMMON_LOG_FORMAT %{IPORHOST:client_ip} %{USER:ident} %{USER:auth} \[%{HTTPDATE:timestamp}\] "(?:%{WORD:verb} %{NOTSPACE:request}(?: HTTP/%{NUMBER:httpversion})?|%{DATA:rawrequest})" %{NUMBER:response} (?:%{NUMBER:bytes:int}|-)
  '''

[[processors.converter]]
  namepass = ["apachelog_throughput"]

  ## 필드를 태그로 변환
  [processors.converter.fields]
   tag = ["domain"]

[[aggregators.basicstats]]
  period = "10s"
  drop_original = true
  stats = ["sum","mean"]
  namepass = ["apachelog_throughput"]
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