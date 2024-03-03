# ClosedAI
### Setup frontend: ###
```
cd react/template
npm i
```
### Setup openai API key: ###
Either fill in the API key in prompt_translation.py or export OPENAI_API_KEY in console
```
#5 client = OpenAI(api_key="APIKEY")
export OPENAI_API_KEY=<API_KEY>
```
### Run frontend: ###
```
cd react/template
npm run dev
```
### Run Backend: ###
```
pip install openai
pip install flask
python -m flask --debug run
```
