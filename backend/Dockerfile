FROM python:3.11.5

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

COPY . .

COPY wait-for-it.sh /wait-for-it.sh

RUN chmod +x /wait-for-it.sh

RUN pip install --no-cache-dir -r requirements.txt

# Download VADER lexicon
RUN python -m nltk.downloader vader_lexicon

# Download punkt tokenizer models
RUN python -m nltk.downloader punkt

EXPOSE 8000