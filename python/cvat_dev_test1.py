from cvat_sdk import make_client, models
from cvat_sdk.core.proxies.tasks import ResourceType, Task

# Create a Client instance bound to a local server and authenticate using basic auth
with make_client(host="localhost", credentials=('user', 'password')) as client:
    # Let's create a new task.

    # Fill in task parameters first.
    # Models are used the same way as in the layer 1.
    task_spec = {
        "name": "example task",
        "labels": [
            {
                "name": "car",
                "color": "#ff00ff",
                "attributes": [
                    {
                        "name": "a",
                        "mutable": True,
                        "input_type": "number",
                        "default_value": "5",
                        "values": ["4", "5", "6"],
                    }
                ],
            }
        ],
    }

    # Now we can create a task using a task repository method.
    # Repositories can be accessed as the Client class members.
    # In this case we use 2 local images as the task data.
    task = client.tasks.create_from_data(
        spec=task_spec,
        resource_type=ResourceType.LOCAL,
        resources=['image1.jpg', 'image2.png'],
    )

    # The returned task object is already up-to-date with its server counterpart.
    # Now we can access task fields. The fields are read-only and can be optional.
    # Let's check that we have 2 images in the task data.
    assert task.size == 2

    # If an object is modified on the server, the local object is not updated automatically.
    # To reflect the latest changes, the local object needs to be fetch()-ed.
    task.fetch()

    # Let's obtain another task. Again, it can be done via the task repository.
    # Suppose we have already created the task earlier and know the task id.
    task2 = client.tasks.retrieve(42)

    # The task object fields can be update()-d. Note that the set of fields that can be
    # modified can be different from what is available for reading.
    task2.update({'name': 'my task'})

    # And the task can also be remove()-d from the server. The local copy will remain
    # untouched.
    task2.remove()
