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
    echo "Downloading Telegraf binary and Jolokia JAR..."

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

test_vcenter_connection() {
    soap_request="<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:urn=\"urn:vim25\">
    <soapenv:Header/>
    <soapenv:Body>
        <urn:RetrieveServiceContent>
            <urn:_this type=\"ServiceInstance\">ServiceInstance</urn:_this>
        </urn:RetrieveServiceContent>
    </soapenv:Body>
</soapenv:Envelope>"

    response=$(curl --insecure -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: text/xml" \
        -u "$username:$password" \
        --data "$soap_request" \
        "$vcenter_url")

    if [[ "$response" == "200" ]]; then
        return 0
    else
        return 1
    fi
}

configure_telegraf() {

    while true; do
        read -p "Enter vCenter URL [http://localhost:8989/sdk]: " vcenter_url
        vcenter_url=${vcenter_url:-http://localhost:8989/sdk}

        while true; do
            read -p "Enter username: " username
            if [[ -n "$username" ]]; then
                break
            else
                echo "Username is required. Please try again."
            fi
        done

        while true; do
            read -sp "Enter password: " password
            echo
            if [[ -n "$password" ]]; then
                break
            else
                echo "Password is required. Please try again."
            fi
        done

        if test_vcenter_connection; then
            echo "vCenter connection successful."
            break
        else
            echo "Failed to connect to vCenter. Please check your inputs and try again."
        fi
    done

    telegraf_config=/usr/whatap/infra/conf/telegraf.d
    mkdir -p $telegraf_config

    cat <<EOF > $telegraf_config/vcenter.conf
[[inputs.vsphere]]
  vcenters = [ "$vcenter_url" ]
  username = "$username"
  password = "$password"
  insecure_skip_verify = true

  discover_concurrency = 1
  object_discovery_interval = "3600s"

  host_metric_exclude = ["*"]
  datastore_metric_exclude = ["*"]
  vm_metric_exclude = ["*"]

  ## Clusters
  ## Typical cluster instance metrics (if omitted or empty, all instance metrics are collected)
  cluster_instances = true

  ## Datacenters
  ## Typical datacenter metrics (if omitted or empty, all metrics are collected)
  ## Typical datacenter instance metrics (if omitted or empty, all instance metrics are collected)
  datacenter_instances = true

  ## Specify timeout to access vCenter.
  timeout = "60s"

  ## When set to true, all collected metrics are sent as integers, defaults to false.
  use_int_samples = false

  ## The interval for collecting metrics. Defaults to 20s.
  interval = "60s"

  max_query_metrics = 1

[[inputs.vsphere]]
  vcenters = [ "$vcenter_url" ]
  username = "$username"
  password = "$password"
  insecure_skip_verify = true

  discover_concurrency = 1
  object_discovery_interval = "3600s"
  host_instances = true

  host_metric_include = []
  resource_pool_exclude = ["*"]
  resource_pool_metric_exclude = ["*"]
  datastore_metric_exclude = ["*"]
  vm_metric_exclude = ["*"]
  cluster_metric_exclude = ["*"]
  datacenter_metric_exclude = ["*"]
  
  ## Specify timeout to access vCenter.
  timeout = "60s"

  ## When set to true, all collected metrics are sent as integers, defaults to false.
  use_int_samples = false

  ## The interval for collecting metrics. Defaults to 20s.
  interval = "20s"

  max_query_metrics = 1

[[inputs.vsphere]]
  vcenters = [ "$vcenter_url" ]
  username = "$username"
  password = "$password"
  insecure_skip_verify = true

  discover_concurrency = 1
  object_discovery_interval = "3600s"
  vm_instances = true

  vm_metric_include = []
  resource_pool_exclude = ["*"]
  resource_pool_metric_exclude = ["*"]
  host_metric_exclude = ["*"]
  datastore_metric_exclude = ["*"]
  cluster_metric_exclude = ["*"]
  datacenter_metric_exclude = ["*"]
  
  ## Specify timeout to access vCenter.
  timeout = "60s"

  ## When set to true, all collected metrics are sent as integers, defaults to false.
  use_int_samples = false

  ## The interval for collecting metrics. Defaults to 20s.
  interval = "20s"

  max_query_metrics = 1

[[inputs.exec]]
  commands = ["/usr/whatap/infra/conf/telegraf.d/ds.py"]
  timeout = "120s"
  data_format = "influx"
  interval = "10m"
  

[[aggregators.merge]]
  period = "30s"
  drop_original = true
  grace = "10s"

EOF

    cat <<EOF > $telegraf_config/ds.py
#!/usr/bin/python3
import urllib.request
import urllib.error
import json
import ssl
import base64
 
# vCenter 접속 정보
VCENTER_URL="$vcenter_url".strip('/sdk')
USERNAME="$username"
PASSWORD="$password"

# SSL 인증서 검증 비활성화 (테스트용)
# 프로덕션 환경에서는 적절한 인증서 설정 필요
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
 
def get_session_token(url, username, password):
    endpoint = f"{url}/rest/com/vmware/cis/session"
    req = urllib.request.Request(endpoint, method="POST")
    # Basic Auth 헤더 설정
    credentials = f"{username}:{password}"
    encoded_creds = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    req.add_header("Authorization", f"Basic {encoded_creds}")
 
    # 요청
    try:
        with urllib.request.urlopen(req, context=context) as resp:
            data = resp.read()
            result = json.loads(data)
            return result.get("value")
    except urllib.error.HTTPError as e:
        print(f"세션 토큰 발급 실패: {e}")
        return None
 
def get_datastores(url, session_token):
    endpoint = f"{url}/rest/vcenter/datastore"
    req = urllib.request.Request(endpoint, method="GET")
    req.add_header("vmware-api-session-id", session_token)
 
    try:
        with urllib.request.urlopen(req, context=context) as resp:
            data = resp.read()
            result = json.loads(data)
            return result.get("value", [])
    except urllib.error.HTTPError as e:
        print(f"Datastore 조회 실패: {e}")
        return []
 
def main():
    session_token = get_session_token(VCENTER_URL, USERNAME, PASSWORD)
    if not session_token:
        return
    #print('session token', session_token) 
    datastores = get_datastores(VCENTER_URL, session_token)
    if not datastores:
        print("발견된 Datastore가 없습니다.")
        return
 
    for ds in datastores:
        name = ds.get("name").replace('"','\\"')
        capacity = ds.get("capacity")
        free_space = ds.get("free_space")
 
        if capacity and free_space is not None:
            usage = capacity - free_space
            usage_percent = (usage * 100.0) / capacity if capacity > 0 else 0
            #print(f"Name: {name}")
            #print(f"  Total Capacity: {capacity} byte ")
            #print(f"  Usage: {usage} byte ({usage_percent:.2f}%)\n")
            line = f"datastore_disk_simple,name=\"{name}\" capacity={capacity}i,usage={usage}i,freespace={free_space}i,usage_percent={usage_percent:.2f}" 
            print(line)

if __name__ == "__main__":
    main()
EOF
    chmod +x $telegraf_config/ds.py
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
