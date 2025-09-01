import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"


def test_create_task():
    new_task_data = {
        "title": "Nova tarefa",
        "description": "Descrição",
        "completed": False
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Tarefa criada" in data["message"]


def test_get_all_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "tasks" in data["message"]

    tasks = data["message"]["tasks"]
    assert isinstance(tasks, list)
    if tasks:
        assert "id" in tasks[0]
        assert "title" in tasks[0]
        assert "description" in tasks[0]
        assert "completed" in tasks[0]


def test_get_task_by_id():
    # cria uma tarefa nova
    new_task_data = {
        "title": "Tarefa específica",
        "description": "Teste GET by ID",
        "completed": False
    }
    post_response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert post_response.status_code == 200

    # pega o id do último item da lista
    all_tasks = requests.get(f"{BASE_URL}/tasks").json()
    tasks = all_tasks["message"]["tasks"]
    task_id = tasks[-1]["id"]

    # busca pelo ID
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200

    task = response.json()
    assert task["id"] == task_id
    assert task["title"] == "Tarefa específica"
    assert task["description"] == "Teste GET by ID"


def test_update_task():
    # cria tarefa
    new_task_data = {
        "title": "Tarefa para atualizar",
        "description": "Descrição antiga",
        "completed": False
    }
    requests.post(f"{BASE_URL}/tasks", json=new_task_data)

    # pega o id do último item
    all_tasks = requests.get(f"{BASE_URL}/tasks").json()
    task_id = all_tasks["message"]["tasks"][-1]["id"]

    # atualiza
    update_data = {
        "title": "Tarefa atualizada",
        "description": "Descrição nova",
        "completed": True
    }
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "atualizada" in data["message"]


def test_delete_task():
    # cria tarefa
    new_task_data = {
        "title": "Tarefa para deletar",
        "description": "Será removida",
        "completed": False
    }
    requests.post(f"{BASE_URL}/tasks", json=new_task_data)

    # pega o id do último item
    all_tasks = requests.get(f"{BASE_URL}/tasks").json()
    task_id = all_tasks["message"]["tasks"][-1]["id"]

    # deleta
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "removida" in data["message"]

    # garantir que não existe mais
    get_response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert get_response.status_code == 404
