FROM python:3.10

# For persisting bash history
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" && echo $SNIPPET >> "/root/.bashrc"

# Poetry
ENV POETRY_VERSION 1.1.13
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/${POETRY_VERSION}/get-poetry.py | python
ENV PATH /root/.poetry/bin:${PATH}

# Is this a good way to add stuff on load?
# Not sure, but it's working
COPY profile.sh /root/profile.sh
RUN echo ". profile.sh" >> "/root/.bashrc"

COPY poetry.* ./
COPY pyproject.toml ./
RUN poetry install
