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
# Front End
![image](https://github.com/wilark1207/ClosedAI/assets/142299224/8321e309-d735-4184-8e75-6e418780092b)
