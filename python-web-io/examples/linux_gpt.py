from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory


template = "I want you to act as a Linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique block and nothing else. Do not write explanations. Do not type commands unless I instruct you to do so."


def chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(template),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

    llm = ChatOpenAI(temperature=0)
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

    return conversation


def main():
    print("<h2>LinuxGPT terminal</h2>")

    print("<small>System prompt:", template, "</small>")

    conversation = chain()

    output = conversation.predict(input="ls")

    print("<br>")
    print("<code>", output, "</code>")

    while True:
        print("<br>")
        human_input = input("👩‍💻")
        output = conversation.predict(input=human_input)
        print("<code>", f"🤖: {output}", "</code>")
