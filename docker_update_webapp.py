import docker
from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)
client = docker.from_env()

TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Docker Update Checker</title>
    <style>
        table { border-collapse: collapse; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        th { background-color: #f0f0f0; }
    </style>
</head>
<body>
    <h1>Docker Containers</h1>
    <table>
        <tr><th>Name</th><th>Image</th><th>Status</th><th>Action</th></tr>
        {% for c in containers %}
        <tr>
            <td>{{ c.name }}</td>
            <td>{{ c.image }}</td>
            <td>{% if c.up_to_date %}Up to date{% else %}Update available{% endif %}</td>
            <td>
                {% if not c.up_to_date %}
                <form action="{{ url_for('update_container', cid=c.id) }}" method="post">
                    <button type="submit">Update</button>
                </form>
                {% else %}-{% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""


def image_up_to_date(container):
    tags = container.image.tags
    if not tags:
        return True
    tag = tags[0]
    pulled = client.images.pull(tag)
    return pulled.id == container.image.id


@app.route('/')
def index():
    containers = []
    for c in client.containers.list(all=True):
        containers.append({
            'id': c.id,
            'name': c.name,
            'image': c.image.tags[0] if c.image.tags else c.image.short_id,
            'up_to_date': image_up_to_date(c)
        })
    return render_template_string(TEMPLATE, containers=containers)


@app.route('/update/<cid>', methods=['POST'])
def update_container(cid):
    container = client.containers.get(cid)
    if container.image.tags:
        tag = container.image.tags[0]
        client.images.pull(tag)
        container.stop()
        container.remove()
        client.containers.run(tag, detach=True, name=container.name)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
