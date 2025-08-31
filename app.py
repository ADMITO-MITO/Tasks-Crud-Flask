from email import message
from flask import Flask, request, jsonify
from models.Tasks import Task
from itertools import count
# "__name__" == "__main__"
app = Flask(__name__)

tasks = []
id_counter = count(1)

@app.route('/tasks', methods=['POST'])

def create_task():
    data = request.get_json()
    new_task = Task(id=next(id_counter), title=data['title'], description=data.get("description", ""))
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Tarefa criada com sucesso"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
            "tasks":task_list,
            "total tasks": len(task_list)
    }
    return jsonify({"message": output})
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())

    return jsonify({"message": "Não foi possivel encontrar a atividade"}), 404

"""@app.route('/tasks', methods=['PUT'])
def update_task(id):

    """
if __name__ == "__main__":
    app.run(debug=True)
