# Creates the Docker image from scratch.
# Alpine has a much smaller OS size; more space for CRUD operations.
FROM python:3-alpine

RUN apk update
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-dev

ENV USERNAME=db
ENV WORKING_DIR=/home/app
WORKDIR ${WORKING_DIR}

COPY app app
COPY requirements.txt .
COPY script.sh .

RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup -S ${USERNAME} && adduser -S -G ${USERNAME} ${USERNAME}
RUN chown -R ${USERNAME}:${USERNAME} ${WORKING_DIR}
RUN chmod -R ug+rwx ${WORKING_DIR}

USER ${USERNAME}
ENV PATH "$PATH:/home/${USERNAME}/.local/bin"

EXPOSE 5000
ENTRYPOINT [ "./script.sh" ]