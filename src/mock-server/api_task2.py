import csv
import json
from flask import Flask, jsonify, request, make_response
import os
import glob
import re

app = Flask(__name__)

NUMBER_OF_RUNS = 1
current_round = 0
waiting_for_post = False
post_data_per_round = {"task2a": {}, "task2b":{}}
finished_serving = False
completed_runs_task2a = set()
completed_runs_task2b = set()

user_path = os.path.join("data","task2","trial","subjects_trial")

def read_json_file(filename):
    with open(filename,mode="r", encoding="utf-8-sig") as json_file:
        return json.load(json_file)

@app.route('/task2/getmessages_trial/789c16fe57f3bc7f0108525b1ea89a0bb4a4952b', methods=['GET'])
def serve_messages():
    global current_round, waiting_for_post, finished_serving, completed_runs_task2a, completed_runs_task2b


    if waiting_for_post and len(completed_runs_task2a) < NUMBER_OF_RUNS:
        lacking = NUMBER_OF_RUNS - len(completed_runs_task2a)
        return make_response(jsonify({"error": f"Lacking {lacking} POST requests for task1a"}), 400)  
    
    if waiting_for_post and len(completed_runs_task2b) < NUMBER_OF_RUNS:
        lacking = NUMBER_OF_RUNS - len(completed_runs_task2b)
        return make_response(jsonify({"error": f"Lacking {lacking} POST requests for task1a"}), 400) 

    if waiting_for_post:
        return make_response(jsonify({"error": "POST request required for each run and task before accepting a new GET request."}), 400)  


    if finished_serving:
        print("No more GET requests are needed. All data has been served.")
        return make_response(jsonify({}), 200)
        #return make_response(jsonify({"info": "No more GET requests are needed. All data has been served."}), 200)
    
    round_number = current_round
    user_files = glob.glob(os.path.join(user_path, "*.json"))  # Assuming user files are named like user_1.json, user_2.json, etc.

    messages = []
    for user_file in user_files:
        user_messages = read_json_file(user_file)
        if len(user_messages) >= round_number + 1:
            msg = user_messages[round_number]
            user_id = int(re.search(r'subject(\d+)\.json', user_file).group(1))
            msg["nick"] = "subject" + str(user_id)
            msg["round"] = current_round
            messages.append(msg)

    if not messages:
        finished_serving = True
        print("No more messages, saving data to predictions_task2.json")
        with open('predictions_task2.json', 'w') as f:
            json.dump(post_data_per_round, f, indent=2)
        return make_response(jsonify({}), 200)
        #return make_response(jsonify({"info": "No more messages. Awaiting POST request and save data."}), 200)

    # if current_round >= 3:
    #     finished_serving = True
    #     return make_response(jsonify({"info": "No more messages. Awaiting POST request and save data."}), 200)

    current_round += 1
    waiting_for_post = True

    return jsonify(messages)



def validate_json_data(data):
    if not isinstance(data, list) or len(data) != 1:
        # print(not isinstance(data, list))
        # print(len(data))
        # print(data[0])
        # print(len(data) != 1)
        # print("HUBO UN ERROR VALIDANDO LOS DATOS 1")
        return False
    data_dict = data[0]
    if not ('predictions' in data_dict and 'emissions' in data_dict):
        # print("HUBO UN ERROR VALIDANDO LOS DATOS 2")
        return False
    if not (isinstance(data_dict['predictions'], dict) and isinstance(data_dict['emissions'], dict)):
        # print("HUBO UN ERROR VALIDANDO LOS DATOS 3")
        return False
    return True


@app.route('/task2a/submit_trial/789c16fe57f3bc7f0108525b1ea89a0bb4a4952b/<int:runs>', methods=['POST'])
def process_data_task2a(runs):
    global waiting_for_post, post_data_per_round, current_round, completed_runs_task2a, completed_runs_task2b

    if runs not in range(NUMBER_OF_RUNS):
        return make_response(jsonify({"error": f"Invalid run number. Allowed values: {range(NUMBER_OF_RUNS)}"}), 400)

    
    
    data = request.get_json()
    
    if not validate_json_data(data):
        return make_response(jsonify({"error": "Invalid JSON data format."}), 400)

    # Process the data as needed
    # ...

    post_data_per_round["task2a"].setdefault(current_round - 1, {})[runs] = data
    completed_runs_task2a.add(runs)

    if len(completed_runs_task2a) == NUMBER_OF_RUNS and len(completed_runs_task2b) == NUMBER_OF_RUNS:
        waiting_for_post = False
        completed_runs_task2a.clear()
        completed_runs_task2b.clear()

    if finished_serving:
        return jsonify({"success": "Finished"})

    return jsonify({"success": "Data processed successfully."})


@app.route('/task2b/submit_trial/789c16fe57f3bc7f0108525b1ea89a0bb4a4952b/<int:runs>', methods=['POST'])
def process_data_task2b(runs):
    global waiting_for_post, post_data_per_round, current_round, completed_runs_task2a, completed_runs_task2b

    if runs not in range( NUMBER_OF_RUNS):
        return make_response(jsonify({"error": f"Invalid run number. Allowed values: {range(NUMBER_OF_RUNS )}"}), 400)


    
    
    data = request.get_json()
    
    if not validate_json_data(data):
        return make_response(jsonify({"error": "Invalid JSON data format."}), 400)

    # Process the data as needed
    # ...

    post_data_per_round["task2b"].setdefault(current_round - 1, {})[runs] = data
    completed_runs_task2b.add(runs)

    if len(completed_runs_task2a) == NUMBER_OF_RUNS and len(completed_runs_task2b) == NUMBER_OF_RUNS:
        waiting_for_post = False
        completed_runs_task2a.clear()
        completed_runs_task2b.clear()

    if finished_serving:
        return jsonify({"success": "Finished"})

    return jsonify({"success": "Data processed successfully."})

if __name__ == '__main__':
    app.run(debug=True)