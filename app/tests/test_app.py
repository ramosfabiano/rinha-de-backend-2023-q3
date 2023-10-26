import unittest
from fastapi.testclient import TestClient
from main import app
from models.pessoa import Pessoa
from models import Session


class AppTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = TestClient(app)

    def setUp(self):
        pessoas = [
            Pessoa('snowj','John Snow','1986-12-26',['Python2', 'Flask']),
            Pessoa('dtarg','Daenerys Targaryen','1986-10-23',['Python3', 'Flask', 'C++']),
            Pessoa('tlannister','Tyrion Lannister','1969-05-11',['C++']),
            Pessoa('astark','Arya Stark','1997-04-15',['C++','Java']),
            Pessoa('clannister','Cersei Lannister','1973-10-03',['Java', 'Pascal']),
            Pessoa('bronn','Bronn','1963-03-06', None)
        ]
        session = Session()
        for p in pessoas:
            session.add(p)
        session.commit()
        session.close()

    def tearDown(self):
        session = Session()
        session.query(Pessoa).delete()
        session.commit()
        session.close()

    # todas as pessoas
    def test_get_pessoas_all(self):
        response = self.client.get("/pessoas?t=")
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
        #print(data)

    # self.client.post("/pessoas/", json={"apelido": "jdoe", "nome": "John Doe", "nascimento": "1990-01-01", "stack": None })
    # self.client.get("/pessoas/b74c3498-db60-4e01-a324-0f81c022a9b4")

if __name__ == "__main__":
    unittest.main()


