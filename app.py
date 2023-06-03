from flask import Flask, render_template, request, jsonify, redirect, abort
from manage import update_value, add_list, add_task, update_list, update_task, delete_task

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    lists = update_value()
    first_key = next((key for key, value in lists.items() if value), None)
    print(first_key)
    if first_key:
        return redirect("/" + str(first_key))
    else:
        return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    if request.method == 'GET':
        return render_template('404.html')
    return e


@app.route('/<int:list_id>', methods=['GET'])
def getList(list_id):
    lists = update_value()
    if list_id in lists:
        if lists[list_id] != {}:
            return render_template('index.html')
    abort(404)


@app.route('/api/lists/', methods=['GET'])
def getAllLists():
    lists = update_value()
    return jsonify(lists)


@app.route('/api/lists/count/', methods=['GET'])
def getListCount():
    lists = update_value()
    return jsonify({'count': len(lists)})


@app.route('/api/lists/<int:list_id>', methods=['GET'])
def getListApi(list_id):
    lists = update_value()
    if list_id in lists:
        list_data = lists[list_id]
        return jsonify(list_data)
    else:
        return jsonify({"Error": "Not Found"})


@app.route('/addlist', methods=['POST'])
def addList():
    lists = update_value()
    if request.method == 'POST':
        r = request.json
        if len(r['list']) <= 20:
            data = {
                "list": r['list'],
                "tasks": {}
            }
            add_list(len(lists)+1,data['list']) 
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "faied", "message": "max length is 20"})
    return jsonify({"success": r})


@app.route('/addtask', methods=['POST'])
def addTask():
    r = request.json
    if r:
        if len(r['task']) <= 200:
            try:
                # *Use received json list id to get the list number to be modified after, add a number to current number of tasks so to add a new task
                # lists[int(r['list_id'])]['tasks'][len(lists[int(r['list_id'])]['tasks'])+1] = {
                #     "task": r['task']
                # }
                lists = update_value()
                taskid = len(lists[int(r['list_id'])]['tasks'])+1
                add_task(int(r['list_id']),taskid,r['task'])
                return jsonify({"status": "success", "task": r['task']})
            except:
                return jsonify({"status": "failed"})
        else:
            return jsonify({"status": "failed", "message": "max length is 200"})
    return jsonify({"status": "failed"})


@app.route('/api/tasks/<int:id>/count', methods=['POST'])
def taskCount(id):
    try:
        lists = update_value()
        return jsonify({"task_count": len(lists[int(id)]['tasks'])})
    except KeyError:
        return jsonify({"status": "failed", "message": "Key Error"})


@app.route('/api/lists/<int:list_id>/task/<int:id>/edit', methods=['PATCH'])
def editTask(list_id, id):
    try:
        r = request.json
        if len(r['text']) <= 200:
            update_task(list_id,id,r['text'])
            return jsonify({"task": r['text'], "status": "success"})
        else:
            return jsonify({"status": "failed", "message": "max length is 200"})
    except KeyError as e:
        return jsonify({"status": "failed", "message": "Key Error"})


@app.route('/api/lists/<int:id>/edit', methods=["PATCH"])
def editList(id):
    try:
        r = request.json
        if len(r['text']) <= 20:
            update_list(id,r['text'])
            lists = update_value()
            return jsonify({"status": 'success', "list": lists[int(id)]['list']})
        else:
            return jsonify({"status": "failed", "message": "max length is 20"})
    except KeyError as e:
        return jsonify({"status": "failed", "error": "Key Error"})


@app.route('/api/lists/<int:list_id>/task/<int:task_id>/delete', methods=['DELETE'])
def deleteTask(list_id, task_id):
    try:
        update_task(list_id,task_id,None)
        return jsonify({"status": "success", "message": "task deleted successfully"})
    except KeyError:
        return jsonify({"status": "failed", "message": "Key Error"})


@app.route('/api/lists/<int:list_id>/delete', methods=['DELETE'])
def deleteList(list_id):
    try:
        update_list(list_id,None)
        delete_task(list_id)
        return jsonify({"status": "success", "message": "list deleted successfully"})
    except KeyError:
        return jsonify({"status": "failed", "message": "Key Error"})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9090)
