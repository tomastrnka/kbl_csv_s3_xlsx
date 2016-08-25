FROM keboola/base

# Initialize 
RUN yum -y install python-pip
RUN yes | pip install pip xlsxwriter
RUN yes | pip install tinys3

WORKDIR /

CMD ["python","code.py"]
