FROM python:3.6.9-slim

# Copy current requrements.txt
RUN mkdir /opt/app
COPY requirements.txt /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt

EXPOSE 80/tcp
#
 CMD ["python3", "app.py"]
