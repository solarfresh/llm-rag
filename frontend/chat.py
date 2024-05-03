import os
import requests
import time
from urllib.parse import urljoin

import streamlit as st

API_BASE_URL = os.environ.get('API_BASE_URL', '')
OPENSEARCH_INDEX = os.environ.get('OPENSEARCH_INDEX', '')
LLM_ENDPOINT = '/api/llm/completion'
SEARCH_ENDPOINT = f'/api/knowledge/{OPENSEARCH_INDEX}/search'
if not API_BASE_URL:
    raise ValueError('The base URL of API must be set...')


def response_search(query):
    if not query:
        return []

    response = requests.post(
        url=urljoin(API_BASE_URL, SEARCH_ENDPOINT),
        data={
            'query': query,
            'limit': 3,
            'score_threshold': 0.75
        },
        timeout=60
    )

    information = '\n'.join([
        f'{idx}: {res["page_content"]}'
        for idx, res in enumerate(response.json().get('results', []))
    ])

    if not information:
        return []
    else:
        return [
            {
                "role": "assistant",
                "content": "以下是找到的資訊:\n{}".format(information)
            },
            {
                "role": "user",
                "content": "用中文總結之後，列出處理方法的步驟。"
            }
        ]


def response_llm():
    system_messages = [
        {
            "role": "system",
            "content": "你是精通 Tableau 的大師，回答的內容必須滿足下列要點:"
        },
        {
            "role": "system",
            "content": "1. 回答的主要語言是中文"
        },
        {
            "role": "system",
            "content": "2. 回答必須是簡單並且容易理解"
        },
        {
            "role": "system",
            "content": "3. 需要條列操作 Tableau 的步驟"
        }
    ]

    if len(st.session_state.messages) < 10:
        history = st.session_state.messages
    else:
        history = st.session_state.messages[-10:]

    query = st.session_state.messages[-1]

    information = response_search(query)

    messages = system_messages + history + information
    if messages:
        response = requests.post(
            url=urljoin(API_BASE_URL, LLM_ENDPOINT),
            json={
                "messages": messages
            },
            timeout=120
        )

        results = [
            res[-1]
            for res in response.json().get('result', '')
            if res[0] == 'content'
        ]
    else:
        results = []

    return results


def response_generator():
    if not st.session_state.messages:
        data = ['很榮幸有機會與您交流 Tableau 這套工具，歡迎討論任何相關問題。']
    else:
        data = response_llm()

    for word in data[0].split():
        yield word + " "
        time.sleep(0.05)


st.title("Tableau 小博士")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("有甚麼想聊的內容？"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display assistant response in chat message container
with st.chat_message("assistant"):
    response = st.write_stream(response_generator())
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})
