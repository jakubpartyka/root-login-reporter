FROM python:slim

COPY ./reporter.py /reporter.py

RUN apt-get update && \
    apt-get upgrade -y;

# setup monitor script
RUN pip install requests;
RUN chmod +x /reporter.py

# setup ufw
# RUN apt-get install ufw -y;

CMD ["python","-u","/reporter.py","/auth.log"]