import document as document
from flask import Flask, render_template, request, redirect, json, jsonify, url_for
import pymongo
from datetime import datetime

from flask_pymongo import PyMongo
from mongoengine import connect

from mongoengine import IntField, StringField, Document

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["flask"]
mycol = mydb["todos"]


class Todo(Document):
    id = IntField
    content = StringField
    date_created = datetime.utcnow()

    def __repr__(self):
        return '<Task %r>' % self.id

    def to_json(self):
        return {"id": self.id,
                "content": self.content,
                "date_created": self.date_created}


@app.route('/')
def index():
    saved_todos = mycol.find()
    return render_template('index.html', todos=saved_todos)


@app.route('/', methods=['POST', 'GET'])
def add_todo():
    if request.method == 'POST':
        new_todo = request.form.get('content')
        mycol.insert_one({'content': new_todo, 'date_created': datetime.now()})
        return redirect(url_for('index'))
    else:
        tasks = mycol.find()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<string:id>')
def delete(id):
    myquery ={'id': id}
    task_to_delete = mycol.delete_one(myquery)
    print(task_to_delete)
    return redirect('/')


@app.route('/update/<string:id>', methods=['PUT'])
def update(id):
    task = mycol.get_or_404(id)
    update_todo = request.form.get('content')
    mycol.insert_one({'content': update_todo, 'date_created': datetime.now()})
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
