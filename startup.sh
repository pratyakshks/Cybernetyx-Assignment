#/bin/bash
cd test
curl -X 'POST' 'http://127.0.0.1:8000/ingest' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@random.txt'
curl -X 'POST' 'http://127.0.0.1:8000/ingest' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@random2.txt'
curl -X 'POST' 'http://127.0.0.1:8000/ingest' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@document.txt'
curl -X 'POST' 'http://127.0.0.1:8000/ingest' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@document1.txt'