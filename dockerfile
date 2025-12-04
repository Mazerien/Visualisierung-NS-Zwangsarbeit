# Creates the Docker image from scratch.
FROM python

RUN apt -q -y update
RUN apt upgrade
RUN apt install -y libgdal-dev
# don't use dev in prod!

ENV USERNAME=app
ENV WORKING_DIR=/home/app
WORKDIR ${WORKING_DIR}

COPY app app
COPY requirements.txt .
#COPY script.sh .
COPY .env .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN groupadd ${USERNAME} && useradd -g ${USERNAME} ${USERNAME}
RUN mkdir -p ${WORKING_DIR}
RUN chown -R ${USERNAME}:${USERNAME} ${WORKING_DIR}
RUN chmod -R u=rwx,g=rwx ${WORKING_DIR}

USER ${USERNAME}
#ENV PATH "$PATH:/home/${USERNAME}/.local/bin"

EXPOSE 5000
CMD ["python", "app/main.py"]
#ENTRYPOINT [ "./script.sh" ]