echo "Installing required modules"
pip install pyats==20.12 genie==20.12.2 requests==2.25.1
ansible-galaxy collection install cisco.nso

echo "Creating nso_cicd directory"
mkdir -p ${HOME}/nso_cicd
cp -r lab_repo/* ${HOME}/nso_cicd

echo "Creating local Docker image with Ansible for use with GitLab Runner"
docker build -t ansible_local:latest ./docker

echo "Spinning up GitLab-CE"
cwd=$(pwd)
cd gitlab
make
cd ${cwd}

echo "Performing initial device sync to NSO and create definition files in vars directory"
cd ${HOME}/nso_cicd
ansible-playbook pb_get_configs.yaml