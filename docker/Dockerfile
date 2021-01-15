FROM python:3.6

RUN pip install ansible==2.10.5 && \
    pip install pyats==20.12 && \
    ansible-galaxy collection install cisco.nso  && \
    apt-get update && \
    apt-get install telnet


