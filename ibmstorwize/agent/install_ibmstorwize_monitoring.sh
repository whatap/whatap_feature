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

test_connection() {
    
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        "$test_url")

    if [[ "$response" == "200" ]]; then
        return 0
    else
        return 1
    fi
}

configure_telegraf() {
    telegraf_config=/usr/whatap/infra/conf/telegraf.d
    mkdir -p $telegraf_config
    cat <<EOF > $telegraf_config/ibmstorewiz.conf
[[inputs.IBMStorwizeMetrics]]
  endpoint = "https://IBM_URL:IBM_PORT/rest/v1"
  auth_username = "USERNAME"
  auth_password = "PASSWORD"
  insecure_skip_verify = true
  # Example of an endpoint with the mapptings from the response to tags and fields
  [[inputs.IBMStorwizeMetrics.metrics]]
    endpoint = "/lsnodestats"
    tags = ["node_id", "node_name"]
    fields = ["stat_current", "stat_name", "stat_peak", "stat_peak_time"]
  [[inputs.IBMStorwizeMetrics.metrics]]
    endpoint = "/lsvdisk"
    tags = ["name", "volume_name"]
    fields = ["capacity", "is_snapshot"]
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