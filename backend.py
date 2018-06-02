from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lqgyyqfljqbqxd:51fc0180ccd4c866433e83da29d4bfae51670195b46b9b1937e75c8cfd4d1aa9@ec2-54-247-177-33.eu-west-1.compute.amazonaws.com:5432/debauug427oq59'
app.config['SECRET_KEY'] = "JE_MOEDER"
app.config['SECURITY_PASSWORD_SALT'] = "jemoeder"
app.config['SECURITY_REGISTERABLE'] = True
db = SQLAlchemy(app)
admin = Admin(app, name="Zoengraaf", template_mode="bootstrap3")

roles_users = db.Table('roles_users',
        db.Column('visitor_id', db.Integer(), db.ForeignKey('visitor.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


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


class Visitor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db, Visitor, Role)
security = Security(app, user_datastore)


class KissingGraphModelView(ModelView):
    def is_accessible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect("/")


admin.add_view(KissingGraphModelView(User, db.session))
admin.add_view(KissingGraphModelView(Interaction, db.session))
admin.add_view(KissingGraphModelView(Visitor, db.session))
admin.add_view(KissingGraphModelView(Role, db.session))


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
    app.run("0.0.0.0", port=5001)
