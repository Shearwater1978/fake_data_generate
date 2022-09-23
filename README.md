# fake_data_generate
Short how-to

1. git clone
2. docker build -f Dockerfile -t generatefakedatacsv:latest .
3. docker run -it --rm -v /tmp/:/tmp/ -e PERSON_COUNT=25 -e LOCALE=ru_RU generatefakedatacsv:latest
4. cat /tmp/persons.csv