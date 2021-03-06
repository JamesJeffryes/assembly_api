FROM kbase/kbase:sdkbase2.latest
MAINTAINER KBase Developer
# -----------------------------------------

# RUN sudo apt-get install -y python-dev libffi-dev libssl-dev
# RUN pip install cffi --upgrade
# RUN pip install pyopenssl --upgrade
# RUN pip install --upgrade ndg-httpsclient
# RUN pip install pyasn1 --upgrade
# RUN pip install requests --upgrade && \
#     pip install 'requests[security]' --upgrade
RUN pip install --upgrade 'requests[security]'

RUN mkdir -p /kb/module && \
    cd /kb/module && \
    git clone https://github.com/kbase/data_api -b 0.4.0-dev && \
    mkdir lib/ && \
    cp -a data_api/lib/doekbase lib/

RUN pip install -r //kb/module/data_api/requirements.txt

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod 777 /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
