"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.app_context().push()
connect_db(app)


@app.route("/")
def root():
    """show homepage"""

    return render_template("index.html")
    

@app.route("/api/cupcakes")
def list_cupcakes():
    """get data about cupcakes; respond in JSON"""

    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = cupcakes)


@app.route("/api/cupcakes", methods= ["POST"])
def create_cupcake():
    """create a cupcake with flavor, size, rating and image data from request"""

    data = request.json

    cupcake = Cupcake(
    flavor = request.json["flavor"],
    size = request.json["size"],
    rating = request.json["rating"],
    image = request.json["image"] or None)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake = cupcake.to_dict()),201)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """get data about single cupcake, response in JSON"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake=cupcake.to_dict())



@app.route('/api/cupcakes/<int:cupcake_id>', methods = ["PATCH"])
def update_cupcake(cupcake_id):
    """update cupcake using id; response in JSON"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake = cupcake.to_dict())


@app.route('/api/cupcakes/<int:cupcake_id>', methods = ["DELETE"])
def delete_cupcake(cupcake_id):
    """delete cupcake by id"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")


