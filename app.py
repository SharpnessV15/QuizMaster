from config import app,db,login_manager

import models

with app.app_context():
    db.create_all()
    if not models.User.query.filter_by(email="admin").first():
        newUser=models.User(name="admin",email="admin",password="admin123",qualification="admin",dob=None)
        db.session.add(newUser)
        db.session.commit()

import routes

if __name__ == '__main__':
    app.run(debug=True)

