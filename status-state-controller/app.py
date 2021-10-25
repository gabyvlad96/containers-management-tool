import requests
import time
import json
import docker

client = docker.from_env()
start_time = time.time()

def load_status_state_list():
    # return the current running containers
    try:
        r = requests.get("http://status-state-api:8080")
        return json.loads(r.text)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

def delete_new_containers(new_containers):
    for i in range(len(new_containers)):
        container = client.containers.get(new_containers[i]["id"])
        container.stop()
        container.remove()
        print("Stopped and removed container " + str(container.short_id))

def restart_old_containers(stopped_containers):
    for i in range(len(stopped_containers)):
        container = client.containers.get(stopped_containers[i]["id"])
        container.restart()
        print("Restarted container " + str(container.short_id))

def check_containers_status(status_state_list):
    # get the updated containers list
    try:
        r = requests.get("http://status-state-api:8080")
        updated_containers_list = json.loads(r.text.replace("\'", "\""))
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
    # detect and delete containers not found in status_state_list
    new_containers = [container for container in updated_containers_list if container not in status_state_list]
    if len(new_containers) > 0:
        delete_new_containers(new_containers)

    # detect and restart the stopped containers in status_state_list
    stopped_containers = [container for container in status_state_list if container not in updated_containers_list]
    if len(stopped_containers) > 0:
        restart_old_containers(stopped_containers)

def main():
    status_state_list = load_status_state_list()
    while True:
        check_containers_status(status_state_list)
        time.sleep(30.0 - ((time.time() - start_time) % 30.0))

if __name__ == "__main__":
    main()