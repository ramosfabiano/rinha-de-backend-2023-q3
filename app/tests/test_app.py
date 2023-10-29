import unittest
from fastapi.testclient import TestClient
from main import app
from main import cache_id, cache_apelido
from models.pessoa import Pessoa
from models import Session


class AppTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = TestClient(app)

    def setUp(self):
        self.pessoas_dict = {}
        pessoas_list = [
            Pessoa('snowj','John Snow','1986-12-26',['Python2', 'Flask']),
            Pessoa('dtarg','Daenerys Targaryen','1986-10-23',['Python3', 'Flask', 'C++']),
            Pessoa('tlannister','Tyrion Lannister','1969-05-11',['C++']),
            Pessoa('astark','Arya Stark','1997-04-15',['C++','Java']),
            Pessoa('clannister','Cersei Lannister','1973-10-03',['Java', 'Pascal']),
            Pessoa('bronn','Bronn','1963-03-06', None)
        ]
        session = Session()
        for p in pessoas_list:
            session.add(p)
            self.pessoas_dict[p.apelido]=p.id
        session.commit()
        session.close()

    def tearDown(self):
        session = Session()
        session.query(Pessoa).delete()
        session.commit()
        session.close()
        cache_id.clear()
        cache_apelido.clear()

    def test_cria_pessoas_201(self):
        response = self.client.post('/pessoas/', json={'apelido': 'jdoe', 'nome': 'John Doe', 'nascimento': '1990-01-01', 'stack': ['C++', 'Java']})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.headers['location']), len('/pessoas/7be83736-3638-4bdf-94df-b7bbffc17305'))
        data = response.json()
        self.assertEqual(data['apelido'], 'jdoe')
        self.assertEqual(data['nome'], 'John Doe')
        self.assertEqual(data['nascimento'], '1990-01-01')
        self.assertEqual(len(data['stack']), 2)
        self.assertEqual(data['stack'][0], 'C++')
        self.assertEqual(data['stack'][1], 'Java')
        # verifica a inclusão
        session = Session()
        self.assertEqual(session.query(Pessoa).count(), len(self.pessoas_dict)+1)
        session.close()

    def test_cria_pessoas_201_filtra_stack_entries_vazias(self):
        response = self.client.post('/pessoas/', json={'apelido': 'jdoe', 'nome': 'John Doe', 'nascimento': '1990-01-01', 'stack': ['', 'C++', '', 'Java', '']})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.headers['location']), len('/pessoas/7be83736-3638-4bdf-94df-b7bbffc17305'))
        data = response.json()
        self.assertEqual(data['apelido'], 'jdoe')
        self.assertEqual(data['nome'], 'John Doe')
        self.assertEqual(data['nascimento'], '1990-01-01')
        self.assertEqual(len(data['stack']), 2)
        self.assertEqual(data['stack'][0], 'C++')
        self.assertEqual(data['stack'][1], 'Java')
        # verifica a inclusão
        session = Session()
        self.assertEqual(session.query(Pessoa).count(), len(self.pessoas_dict)+1)
        session.close()

    def test_cria_pessoas_201_empty_stack_v1(self):
        response = self.client.post('/pessoas/', json={'apelido': 'jdoe2', 'nome': 'John Doe 2', 'nascimento': '2000-02-02', 'stack': None})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.headers['location']), len('/pessoas/7be83736-3638-4bdf-94df-b7bbffc17305'))
        data = response.json()
        self.assertEqual(data['apelido'], 'jdoe2')
        self.assertEqual(data['nome'], 'John Doe 2')
        self.assertEqual(data['nascimento'], '2000-02-02')
        self.assertEqual(data['stack'], None)

    def test_cria_pessoas_201_empty_stack_v2(self):
        response = self.client.post('/pessoas/', json={'apelido': 'jdoe2', 'nome': 'John Doe 2', 'nascimento': '2000-02-02', 'stack': []})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.headers['location']), len('/pessoas/7be83736-3638-4bdf-94df-b7bbffc17305'))
        data = response.json()
        self.assertEqual(data['apelido'], 'jdoe2')
        self.assertEqual(data['nome'], 'John Doe 2')
        self.assertEqual(data['nascimento'], '2000-02-02')
        self.assertEqual(data['stack'], None)

    def test_cria_pessoas_422(self):
        # apelido existente
        response = self.client.post('/pessoas/', json={'apelido': 'astark', 'nome': 'John Doe 2', 'nascimento': '2000-02-02', 'stack': None})
        self.assertEqual(response.status_code, 422)
        # apelido nulo
        response = self.client.post('/pessoas/', json={'apelido': None, 'nome': 'John Doe', 'nascimento': '1990-01-01', 'stack': ['C++', 'Java']})
        self.assertEqual(response.status_code, 422)
        # nome nulo
        response = self.client.post('/pessoas/', json={'apelido': 'jdoe', 'nome': None, 'nascimento': '1990-01-01', 'stack': ['C++', 'Java']})
        self.assertEqual(response.status_code, 422)        
        # nascimento nulo
        response = self.client.post('/pessoas/', json={'apelido': 'jdoe', 'nome': 'John Doe', 'nascimento': None, 'stack': ['C++', 'Java']})
        self.assertEqual(response.status_code, 422)

    def test_cria_pessoas_400(self):
        # data inválida
        response = self.client.post('/pessoas/', json={'apelido': 'jdoe2', 'nome': 'John Doe 2', 'nascimento': '2000-02-02-invalid-date', 'stack': None})
        self.assertEqual(response.status_code, 400)
        # nome inválido
        response = self.client.post('/pessoas/', json={'apelido': 'jdoe2', 'nome': 12345, 'nascimento': '2000-02-02', 'stack': None})
        self.assertEqual(response.status_code, 400)
        # apelido inválido
        response = self.client.post('/pessoas/', json={'apelido': 12345, 'nome': 'John Doe 2', 'nascimento': '2000-02-02', 'stack': None})
        self.assertEqual(response.status_code, 400)
        # stack inválido 1
        response = self.client.post('/pessoas/', json={'apelido': 'jdoe2', 'nome': 'John Doe 2', 'nascimento': '2000-02-02', 'stack': 1})
        self.assertEqual(response.status_code, 400)
        # stack inválido 2
        response = self.client.post('/pessoas/', json={'apelido': 'jdoe', 'nome': 'John Doe 2', 'nascimento': '1990-01-01', 'stack': [0, 'C++', 'Java']})
        self.assertEqual(response.status_code, 400)
        # stack inválido 3
        response = self.client.post('/pessoas/', json={'apelido': 'jdoe', 'nome': 'John Doe 2', 'nascimento': '1990-01-01', 'stack': 'java'})
        self.assertEqual(response.status_code, 400)

    def test_detalhe_pessoas_200(self):
        for apelido, id in self.pessoas_dict.items():
            response = self.client.get(f'/pessoas/{id}')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['apelido'], apelido)

    def test_detalhe_pessoas_404(self):
        response = self.client.get('/pessoas/b74c3498-db60-4e01-a324-0f81c022a9b4')
        self.assertEqual(response.status_code, 404)

    def test_busca_pessoas_todas(self):
        response = self.client.get('/pessoas?t=')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data),6)
        self.assertEqual(data[0]['apelido'],'snowj')
        self.assertEqual(data[1]['apelido'],'dtarg')
        self.assertEqual(data[2]['apelido'],'tlannister')
        self.assertEqual(data[3]['apelido'],'astark')
        self.assertEqual(data[4]['apelido'],'clannister')
        self.assertEqual(data[5]['apelido'],'bronn')
        self.assertEqual(len(data[0]['stack']),2)
        self.assertEqual(len(data[1]['stack']),3)
        self.assertEqual(len(data[2]['stack']),1)
        self.assertEqual(len(data[3]['stack']),2)
        self.assertEqual(len(data[4]['stack']),2)
        self.assertEqual(data[5]['stack'],None)

    def test_busca_pessoas_nenhuma(self):
        response = self.client.get('/pessoas?t=abcde')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data),0)

    def test_busca_pessoas_python(self):
        response = self.client.get('/pessoas?t=python')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data),2)
        self.assertEqual(data[0]['apelido'],'snowj')
        self.assertEqual(data[1]['apelido'],'dtarg')

    def test_busca_pessoas_lannister(self):
        response = self.client.get('/pessoas?t=Lannister')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data),2)
        self.assertEqual(data[0]['apelido'],'tlannister')
        self.assertEqual(data[1]['apelido'],'clannister')

    def test_contagem_pessoas(self):
        response = self.client.get('/contagem-pessoas')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 6)

    def test_caching_after_read(self):        
        for apelido, id in self.pessoas_dict.items():
            response = self.client.get(f'/pessoas/{id}')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['apelido'], apelido)
            self.assertEqual('cached' in data, False)
        for apelido, id in self.pessoas_dict.items():
            response = self.client.get(f'/pessoas/{id}')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['apelido'], apelido)
            self.assertGreater(len(data['cached']), 0)

    def test_caching_after_write(self):
        response = self.client.post('/pessoas/', json={'apelido': 'jdoe', 'nome': 'John Doe', 'nascimento': '1990-01-01', 'stack': ['C++', 'Java']})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual('cached' in data, False)
        id = data['id']
        response = self.client.get(f'/pessoas/{id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data['cached']), 0)

if __name__ == "__main__":
    unittest.main()


