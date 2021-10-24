from flask import Flask, jsonify
import docker

app = Flask(__name__)
client = docker.from_env()

@app.route('/')
def return_containers():
    containers_data = client.containers.list()
    running_containers = [
        {"name": container.name,
        "image": container.image.tags[0].split(":")[0],
        "id": container.short_id,
        "status": container.status}
        for container in containers_data]
    return jsonify(running_containers)