FROM python:3.10.6


WORKDIR /Coginizant_project


ADD . /Coginizant_project

RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


CMD [ "python3","run.py" ]



