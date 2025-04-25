from flask import Flask, jsonify
from neo4j import GraphDatabase
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许前端跨域访问

driver = GraphDatabase.driver("bolt://123.56.47.51:7687", auth=("neo4j", "jike2201!"))


def fetch_graph_data():
    with driver.session() as session:
        result = session.run("""
            MATCH (n)-[r]->(m)
            RETURN n, r, m
        """)
        nodes = {}
        links = []
        for record in result:
            n, m, r = record["n"], record["m"], record["r"]
            for node in [n, m]:
                if node.element_id not in nodes:
                    props = dict(node.items())
                    nodes[node.element_id] = {
                        "id": node.element_id,
                        "label": list(node.labels)[0] if node.labels else "Node",
                        "name": props.get("name", "未命名"),
                        "properties": props
                    }
            links.append({
                "source": n.element_id,
                "target": m.element_id,
                "type": r.type,
                "label": r.type
            })
        return {"nodes": list(nodes.values()), "links": links}


@app.route("/graph-data")
def graph_data():
    return jsonify(fetch_graph_data())


if __name__ == "__main__":
    app.run(debug=True)
