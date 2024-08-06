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
test_aerospike_connection() {
    aerospike_host=$(echo "$aerospike_url" | cut -d':' -f1)
    aerospike_port=$(echo "$aerospike_url" | cut -d':' -f2)

    nc -z -w5 "$aerospike_host" "$aerospike_port"
    if [[ $? -eq 0 ]]; then
        return 0
    else
        return 1
    fi
}
configure_telegraf() {
    while true; do
        read -p "Enter aerospike API URL [localhost:3000]: " aerospike_url
        aerospike_url=${aerospike_url:-localhost:3000}

        read -p "Is security enabled on the Aerospike server? (yes/no): " security_enabled

        if [[ "$security_enabled" == "yes" ]]; then
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
        fi

        if test_aerospike_connection; then
            echo "Aerospike connection successful."
            break
        else
            echo "Failed to connect to Aerospike. Please check your inputs and try again."
        fi
    done

    telegraf_config=/usr/whatap/infra/conf/telegraf.d
    mkdir -p $telegraf_config

    if [[ "$security_enabled" == "yes" ]]; then
        cat <<EOF > $telegraf_config/aerospike.conf
[[inputs.aerospike]]
  ## Aerospike servers to connect to (with port)
  ## This plugin will query all namespaces the aerospike
  ## server has configured and get stats for them.
  servers = [ "$aerospike_url" ]
  username = "$username"
  password = "$password"
EOF
    else
        cat <<EOF > $telegraf_config/aerospike.conf
[[inputs.aerospike]]
  ## Aerospike servers to connect to (with port)
  ## This plugin will query all namespaces the aerospike
  ## server has configured and get stats for them.
  servers = [ "$aerospike_url" ]

[[processors.starlark]]
  source = '''
# Dictionary to hold the state for each field
state = {}

def apply(metric):
    for field_name, field_value in metric.fields.items():
        # Only process numeric fields
        field_type = type(field_value)
        if field_type == "int" or field_type == "float":
            key = metric.name + "." + field_name
            if key not in state:
                state[key] = []

            state[key].append(field_value)

            # Maintain a fixed window size of the last 5 values
            if len(state[key]) > 180:
                state[key].pop(0)

            # Calculate the sum manually
            total = 0
            for value in state[key]:
                total += value

            avg = total / len(state[key])
            # Store the moving average in a new field
            metric.fields[field_name + "_moving_avg"] = avg

    return metric
'''
EOF
    fi
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