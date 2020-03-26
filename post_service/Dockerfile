FROM python:3

ADD requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN mkdir -p /post_service
ADD . /post_service
WORKDIR /post_service

EXPOSE 7082

CMD ["flask", "run", "--host=0.0.0.0", "--port=7082"]