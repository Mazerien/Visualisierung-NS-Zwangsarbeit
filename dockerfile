# Creates the Docker image from scratch.
# Alpine has a much smaller OS size; more space for CRUD operations.
FROM python

RUN apt-get -q -y update
RUN apt-get install -y gdal-bin libgdal-dev
# don't use dev in prod!

ENV USERNAME=db
ENV WORKING_DIR=/home/app
WORKDIR ${WORKING_DIR}

COPY app app
COPY requirements.txt .
COPY script.sh .
COPY .env .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd ${USERNAME} && useradd -g ${USERNAME} ${USERNAME}
RUN chown -R ${USERNAME}:${USERNAME} ${WORKING_DIR}
RUN chmod -R u=rwx,g=rwx ${WORKING_DIR}

USER ${USERNAME}
ENV PATH "$PATH:/home/${USERNAME}/.local/bin"

EXPOSE 5000
ENTRYPOINT [ "./script.sh" ]