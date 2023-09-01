from flask import Flask, render_template, request, jsonify
import openai
import json

openai.api_key = "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"

app = Flask(__name__)

chat_history_arr = []
chat_messages = {"role": "system", "content": "You are a friendly chatbot that takes the medical history from a patient. You do not need to ask for demographic information from the patient. The questions you ask, and the patient's answers will help the doctor understand the patient's medical history. Do not provide any response to the patient about the diagnosis, is the patient asks about the diagnosis. The doctor will give the diagnosis. A successful medical history from the patient will help the doctor to narrow down the diagnosis quickly. Do not ask more than 10 single-part questions regarding the nature of the patient's condition. Ask one question at a time. Based on the patient's response, ask the next question. At the end of asking questions, generate a previsit summary for the doctor with possible diagnosis"}
                    # ,{'role': 'user', 'content': input}
chat_history_arr.append(chat_messages)
# initial_response=""


@app.route("/")
def index():
    # query Prompt table and get prompt description
    # convert prompt description string to json
    # chat_history_arr.append(chat_messages)

    response_content = get_openai_response(chat_history_arr)
    response_content_escaped = response_content.replace("\n", "\\n")
    # initial_response=response_content
    assistant_string = f'{{"role": "assistant", "content":"{response_content_escaped}"}}'
    print("assistant_string=",assistant_string, flush=True)
    assistant_json = json.loads(assistant_string)
    formatted_string = json.dumps(assistant_json)
    formatted_json = json.loads(formatted_string)
    print("assistant_json=",assistant_json, flush=True)
    chat_history_arr.append(formatted_json)
    return render_template('chat.html', response=response_content) #response_content


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    #chat_messages = [{'role': 'system', 'content': 'Welcome! How I can help you?'}, {'role': 'user', 'content': input}]
    chat_messages = [{"role": "system", "content": "You are a friendly chatbot that takes the medical history from a patient. You do not need to ask for demographic information from the patient. The questions you ask, and the patient's answers will help the doctor understand the patient's medical history. Do not provide any response to the patient about the diagnosis, is the patient asks about the diagnosis. The doctor will give the diagnosis. A successful medical history from the patient will help the doctor to narrow down the diagnosis quickly. Do not ask more than 10 single-part questions regarding the nature of the patient's condition. Ask one question at a time. Based on the patient's response, ask the next question. At the end of asking questions, generate a previsit summary for the doctor with possible diagnosis"}
                    ,{'role': 'user', 'content': input}
                    ]
    user_input_json={'role': 'user', 'content': input}
    chat_history_arr.append(user_input_json)
    # assistant_string = f'{"role": "assistant", "content":assistant}'
    response_content = get_openai_response(chat_history_arr)
    response_content_escaped = response_content.replace("\n", "\\n")
    assistant_string = f'{{"role": "assistant", "content":"{response_content_escaped}"}}'
    print("assistant_string=",assistant_string, flush=True)
    assistant_json = json.loads(assistant_string)
    formatted_string = json.dumps(assistant_json)
    formatted_json = json.loads(formatted_string)
    print("assistant_json=",formatted_json, flush=True)
    chat_history_arr.append(formatted_json)


    # return get_openai_response(chat_history_arr)
    # return predict(msg)
    return response_content

def get_openai_response(messages):
    print("messages :: ",messages, flush=True)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100
    )
    print("response :: ",response, flush=True)
    print("response content :: ", response['choices'][0]['message']['content'], flush=True)
    return response['choices'][0]['message']['content']

def predict(message):
    history_openai_format = []

    history_openai_format.append({"role": "system", "content": "You're a physician assistant helping the doctor to understand patient's medical history from chat transcript. The doctor will send you the whole chat transcript from the patient. Create a summary of the chat transcript. Provide details about possible diagnoses and explain your reasoning. Recommend tests to order and provide your reasoning. Provide recommendations for the doctor on what to evlauate during the visit.  You're creating a pre-visit summary of the patient to save doctor's time and also to provide a better consultation to the patient."})
   
    # for human, assistant in history:
    #     history_openai_format.append({"role": "user", "content": human })
    #     history_openai_format.append({"role": "assistant", "content":assistant})
    
    history_openai_format.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages= history_openai_format,         
        temperature=0.1,
        stream=True
    )
    
    partial_message = ""
    for chunk in response:
        if len(chunk['choices'][0]['delta']) != 0:
            partial_message = partial_message + chunk['choices'][0]['delta']['content']
            yield partial_message 
    
    print("partial_message=",partial_message, flush=True)
    return partial_message


if __name__ == '__main__':
    app.run()
