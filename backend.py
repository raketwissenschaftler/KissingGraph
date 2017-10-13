from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lqgyyqfljqbqxd:51fc0180ccd4c866433e83da29d4bfae51670195b46b9b1937e75c8cfd4d1aa9@ec2-54-247-177-33.eu-west-1.compute.amazonaws.com:5432/debauug427oq59'
db = SQLAlchemy(app)
admin = Admin(app, name="Zoengraaf", template_mode="bootstrap3")

ALLOWED_USERS = [{"password": "zoengraafwachtwoord", "username": "rick"}]

class Interaction(db.Model):
    __tablename__ = "interactions"
    id = db.Column(db.Integer, primary_key=True)
    interaction_type = db.Column(db.String(100))
    party1id = db.Column(db.Integer, db.ForeignKey("users.id"))
    party2id = db.Column(db.Integer, db.ForeignKey("users.id"))

    party1 = db.relationship("User", backref="interactions1", foreign_keys=[party1id])
    party2 = db.relationship("User", backref="interactions2", foreign_keys=[party2id])


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __str__(self):
        return "<User id:{0} name: {1}>".format(self.id, self.name)


class KissingGraphModelView(ModelView):
    def is_accessible(self):
        for user in ALLOWED_USERS:
            if request.args.get("password") == user["password"] and request.args.get("username") == user["username"]:
                return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect("/")

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Interaction, db.session))


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route("/getInteractions")
def get_kisses():
    users_array = []
    for user in User.query.all():
        users_array.append({"data": {"name": user.name, "id": user.id}})

    interactions_array = []
    for interaction in Interaction.query.all():
        interactions_array.append({"data": {"source": interaction.party1id,
                                            "target": interaction.party2id,
                                            "type": interaction.interaction_type}})
    return jsonify(users_array + interactions_array)


if __name__ == '__main__':
    db.create_all()
    app.run("0.0.0.0", 5050, debug=True)
