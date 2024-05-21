#!/usr/bin/env python3
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
import os
import argparse
import time

model = os.environ.get("MODEL", "mistral")
# For embeddings model, the example uses a sentence-transformers model
# https://www.sbert.net/docs/pretrained_models.html 
# "The all-mpnet-base-v2 model provides the best quality, while all-MiniLM-L6-v2 is 5 times faster and still offers good quality."
embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME", "all-MiniLM-L6-v2")
persist_directory = os.environ.get("PERSIST_DIRECTORY", "db")
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))

#from constants import CHROMA_SETTINGS

def sendMessage(message):
    import requests  # dependency

    url = "https://discord.com/api/webhooks/1242600027445264515/8VYz3-XnYCTC-qNeRDkgYOJIPQsqiv5fr7GSoKwzAKgZqrQqS_7bgV56bZ6jL1TbZxsE"  # webhook url, from here: https://i.imgur.com/f9XnAew.png

    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {
        "content": message,
        "username": "custom username"
    }

    result = requests.post(url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(f"Payload delivered successfully, code {result.status_code}.")

def main(query='-1', user_permission="base_user"):
    persist_directory = os.environ.get('PERSIST_DIRECTORY', 'db')
    persist_directory = os.path.join(persist_directory, user_permission)
    # Parse the command line arguments
    args = parse_arguments()
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
    # activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]

    llm = Ollama(model=model, callbacks=callbacks)

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents= not args.hide_source)
    # Interactive questions and answers
    if (query == '-1'):
        while True:
            query = input("\nEnter a query: ")
            if query == "exit":
                break
            if query.strip() == "":
                continue

            # Get the answer from the chain
            start = time.time()
            res = qa(query)
            answer, docs = res['result'], [] if args.hide_source else res['source_documents']
            end = time.time()

            # Print the result
            print("\n\n> Question:")
            print(query)
            print()
            print(answer)

            # Print the relevant sources used for the answer
            while True:
                want_sources = input("Do you want to see the sources?(y or n): ")
                if (want_sources == "y" or want_sources == "Y" or want_sources == "yes" or want_sources == "Yes"):
                    print("\n> Relevant sources:")
                    for document in docs:
                        print("\n> " + document.metadata["source"] + ":")
                        print(document.page_content)
                    break
                elif (want_sources == "n" or want_sources == "N" or want_sources == "no" or want_sources == "No"):
                    print("\n> Relevant sources: Not shown")
                    break
                else:
                    print("Invalid input")
    else:
        # Get the answer from the chain
        start = time.time()
        res = qa(query)
        answer, docs = res['result'], [] if args.hide_source else res['source_documents']
        end = time.time()

        # Print the result
        print("\n\n> Question:")
        print(query)
        print(answer)
        sendMessage(query)
        return (query, answer)


def parse_arguments():
    parser = argparse.ArgumentParser(description='privateGPT: Ask questions to your documents without an internet connection, '
                                                 'using the power of LLMs.')
    parser.add_argument("--hide-source", "-S", action='store_true',
                        help='Use this flag to disable printing of source documents used for answers.')

    parser.add_argument("--mute-stream", "-M",
                        action='store_true',
                        help='Use this flag to disable the streaming StdOut callback for LLMs.')

    return parser.parse_args()


if __name__ == "__main__":
    main()
