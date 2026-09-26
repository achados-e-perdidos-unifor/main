"""Integration tests for Achados e Perdidos API.

These tests run against a live Flask application + PostgreSQL database
(via docker-compose) and validate end-to-end functionality.
"""


class TestHealth:
    """Health check endpoint tests."""

    def test_health_endpoint_returns_200(self, http_client):
        """Health endpoint should return 200 OK."""
        response = http_client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestObjetosPerdidos:
    """Tests for Lost Objects (Objetos Perdidos) CRUD operations."""

    def test_create_objeto_perdido(self, http_client, clean_database):
        """Should create a lost object."""
        payload = {
            "nome_objeto": "Carteira marrom",
            "cor": "Marrom",
            "data_perdido": "20/09/2026"
        }

        response = http_client.post("/inserir_objeto", json=payload)
        assert response.status_code == 200

    def test_list_objetos_perdidos(self, http_client, clean_database):
        """Should list all lost objects."""
        payload = {
            "nome_objeto": "Chaves",
            "cor": "Prata",
            "data_perdido": "19/09/2026"
        }
        http_client.post("/inserir_objeto", json=payload)

        response = http_client.get("/listar_objetos")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

    def test_list_objeto_by_id(self, http_client, clean_database):
        """Should retrieve a lost object by ID."""
        payload = {
            "nome_objeto": "Relógio",
            "cor": "Dourado",
            "data_perdido": "18/09/2026"
        }
        http_client.post("/inserir_objeto", json=payload)

        list_response = http_client.get("/listar_objetos")
        assert len(list_response.json()) > 0
        obj_id = list_response.json()[0]["id_objeto"]

        response = http_client.get(f"/listar_objeto/{obj_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["Objeto-perdido"]["nome_objeto"] == "Relógio"

    def test_update_objeto_perdido(self, http_client, clean_database):
        """Should update a lost object."""
        insert_payload = {
            "nome_objeto": "Mochila preta",
            "cor": "Preta",
            "data_perdido": "17/09/2026"
        }
        http_client.post("/inserir_objeto", json=insert_payload)

        list_response = http_client.get("/listar_objetos")
        obj_id = list_response.json()[0]["id_objeto"]

        update_payload = {
            "id_objeto": obj_id,
            "nome_objeto": "Mochila preta (grande)",
            "cor": "Preta",
            "data_perdido": "17/09/2026"
        }
        response = http_client.put("/atualizar_objeto", json=update_payload)
        assert response.status_code == 200

        verify_response = http_client.get(f"/listar_objeto/{obj_id}")
        assert verify_response.json()["Objeto-perdido"]["nome_objeto"] == "Mochila preta (grande)"

    def test_delete_objeto_perdido(self, http_client, clean_database):
        """Should delete a lost object."""
        insert_payload = {
            "nome_objeto": "Óculos de sol",
            "cor": "Preto",
            "data_perdido": "16/09/2026"
        }
        http_client.post("/inserir_objeto", json=insert_payload)

        list_response = http_client.get("/listar_objetos")
        obj_id = list_response.json()[0]["id_objeto"]

        response = http_client.delete(f"/deletar_objeto/{obj_id}")
        assert response.status_code == 200

        verify_response = http_client.get("/listar_objetos")
        assert len(verify_response.json()) == 0


class TestObjetosAchados:
    """Tests for Found Objects (Objetos Achados) CRUD operations."""

    def test_create_objeto_achado(self, http_client, clean_database):
        """Should create a found object record."""
        lost_payload = {
            "nome_objeto": "Guarda-chuva",
            "cor": "Vermelho",
            "data_perdido": "15/09/2026"
        }
        http_client.post("/inserir_objeto", json=lost_payload)

        list_response = http_client.get("/listar_objetos")
        obj_id = list_response.json()[0]["id_objeto"]

        found_payload = {
            "id_objeto": obj_id,
            "nome_objeto_achado": "Guarda-chuva",
            "cor_achado": "Vermelho",
            "nome_pessoa": "Maria Silva",
            "cpf": "123.456.789-10",
            "contato": "maria@email.com"
        }
        response = http_client.post("/inserir_objetoA", json=found_payload)
        assert response.status_code == 200

    def test_list_objetos_achados(self, http_client, clean_database):
        """Should list all found objects."""
        lost_payload = {
            "nome_objeto": "Livro",
            "cor": "Azul",
            "data_perdido": "14/09/2026"
        }
        http_client.post("/inserir_objeto", json=lost_payload)

        list_response = http_client.get("/listar_objetos")
        obj_id = list_response.json()[0]["id_objeto"]

        found_payload = {
            "id_objeto": obj_id,
            "nome_objeto_achado": "Livro",
            "cor_achado": "Azul",
            "nome_pessoa": "João Santos",
            "cpf": "987.654.321-00",
            "contato": "joao@email.com"
        }
        http_client.post("/inserir_objetoA", json=found_payload)

        response = http_client.get("/listar_objetosA")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

    def test_delete_objeto_achado(self, http_client, clean_database):
        """Should delete a found object record."""
        lost_payload = {
            "nome_objeto": "Celular",
            "cor": "Branco",
            "data_perdido": "13/09/2026"
        }
        http_client.post("/inserir_objeto", json=lost_payload)

        list_response = http_client.get("/listar_objetos")
        obj_id = list_response.json()[0]["id_objeto"]

        found_payload = {
            "id_objeto": obj_id,
            "nome_objeto_achado": "Celular",
            "cor_achado": "Branco",
            "nome_pessoa": "Ana Costa",
            "cpf": "456.789.123-45",
            "contato": "ana@email.com"
        }
        http_client.post("/inserir_objetoA", json=found_payload)

        found_list = http_client.get("/listar_objetosA")
        found_id = found_list.json()[0]["id_objetoA"]

        response = http_client.delete(f"/deletar_objetoA/{found_id}")
        assert response.status_code == 200

        verify_response = http_client.get("/listar_objetosA")
        assert len(verify_response.json()) == 0
