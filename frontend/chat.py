import os
import requests
import time
from urllib.parse import urljoin

import streamlit as st

API_BASE_URL = os.environ.get('API_BASE_URL', '')
OPENSEARCH_INDEX = os.environ.get('OPENSEARCH_INDEX', '')
LLM_ENDPOINT = '/api/llm/completionstream'
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

    results = response.json().get('results', [])
    information = '\n'.join([
        f'{idx}: {res["page_content"]}'
        for idx, res in enumerate(results)
    ])
    references = '\n'.join([
        f'- {res["source"]}'
        for res in results
    ])

    if not information:
        return [
            {
                "role": "system",
                "content": "為了尋找不到問題表示遺憾，並建議問題相關的提示詞。"
            }
        ], None
    else:
        return [
            {
                "role": "system",
                "content": f"以下是搜尋到的資訊:\n{information}\n需要依照下面原則回答:"
            },
            {
                "role": "system",
                "content": "1. 不能夠回答搜尋到的資訊以外的內容。"
            },
            {
                "role": "system",
                "content": "2. 如果搜尋到的資訊不存在相關內容，詢問一個與內容相關的問題。"
            }
        ], references


def response_llm():
    system_messages = [
        {
            "role": "system",
            "content": "你是精通 Tableau 的大師，回答的內容必須滿足下列要點:"
        },
        {
            "role": "system",
            "content": "1. 回答的主要語言是正體中文"
        },
        {
            "role": "system",
            "content": "2. 回答必須是簡單並且容易理解"
        }
    ]

    if len(st.session_state.messages) < 10:
        history = st.session_state.messages
    else:
        history = st.session_state.messages[-10:]

    query_message = st.session_state.messages[-1]
    information, references = response_search(query_message['content'])

    messages = system_messages + history + information
    if messages:
        response = requests.post(
            url=urljoin(API_BASE_URL, LLM_ENDPOINT),
            json={
                "messages": messages
            },
            stream=True,
            timeout=120
        )

        for line in response.iter_content(chunk_size=10):
            if line:
                yield line.decode('utf-8')
                time.sleep(.1)

        yield f'### 以下為參考資訊來源:\n{references}'
    else:
        yield ''


def response_generator():
    if not st.session_state.messages:
        yield '很榮幸有機會與您交流 Tableau 這套工具，歡迎討論任何相關問題。'
    else:
        for word in response_llm():
            yield word


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
