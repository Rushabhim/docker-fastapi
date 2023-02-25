import pytest
import requests
import gzip

DOCKER_URL = 'http://localhost:800'

def test_file_endpoint():
    data = 'id,name,age\n1,Alice,25\n2,Bob,30\n'
    with open('test.csv', 'w') as f:
        f.write(data)

    with open('test.csv', 'rb') as f_in:
        with gzip.open('test.csv.gz', 'wb') as f_out:
            f_out.write(f_in.read())

    with open('test.csv.gz', 'rb') as f:
        response = requests.post(f'{DOCKER_URL}/file', data=f, headers={'Content-Encoding': 'gzip'})

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/gzip'
    assert response.headers['Content-Disposition'] == 'attachment; filename="test.csv.gz"'

    with gzip.open(response.content, 'rb') as f:
        contents = f.read().decode('utf-8')
    assert contents == data