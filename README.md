#### Inspired from (https://github.com/imartinez/privateGPT), (https://github.com/jmorganca/ollama), and (https://github.com/PromptEngineer48/Ollama)

#### This project is a remix of PromptEngineer's [Ollama project](https://github.com/PromptEngineer48/Ollama), check out his Youtube channel for more projects like this: https://www.youtube.com/@PromptEngineer48/


#### Step 1: Step into a Virtual Environment

#### Step 2: Install the Requirements
```
pip install -r requirements.txt
```

#### Step 3: Pull the models (if you already have models loaded in Ollama, then not required)
#### Make sure to have Ollama running on your system from https://ollama.ai
```
ollama pull mistral
```

#### Step 4: Ingest the files (use python3 if on mac)
```
python website/ingest.py
```

Output should look like this:
```shell
Creating new vectorstore
Loading documents from source_documents
Loading new documents: 100%|██████████████████████| 1/1 [00:01<00:00,  1.99s/it]
Loaded 235 new documents from source_documents
Split into 1268 chunks of text (max. 500 tokens each)
Creating embeddings. May take some minutes...
Ingestion complete! You can now run privateGPT.py to query your documents
```

#### Step 5: Run this command (use python3 if on mac) to start the local host flask server
```
python main.py
```

#### Step 6: Register an acount and go to http://127.0.0.1:8000/ to start chatting

## Add more files

Put any and all your files into the `website/source_documents` directory, then repeat Step 4

The supported extensions are:

- `.csv`: CSV,
- `.docx`: Word Document,
- `.doc`: Word Document,
- `.enex`: EverNote,
- `.eml`: Email,
- `.epub`: EPub,
- `.html`: HTML File,
- `.md`: Markdown,
- `.msg`: Outlook Message,
- `.odt`: Open Document Text,
- `.pdf`: Portable Document Format (PDF),
- `.pptx` : PowerPoint Document,
- `.ppt` : PowerPoint Document,
- `.txt`: Text file (UTF-8),
