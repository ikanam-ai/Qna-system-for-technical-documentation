from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()
iam_token = "kitkat-ru0central-sfqo1283124"
folder_id = "kitkat_1"
model_uri = "ds://sk-proj-4ZJCMqRi0iygdm8jcGRkT3BlbkFJqlkbT2OENbLtoT7IXOgv"
classifier_url = "http://classifier_server_endpoint/classify"


class Prompt(BaseModel):
    text: str


@app.post("/receive-prompt")
async def receive_text(prompt: Prompt):
    try:
        with open('./doc/doc.txt', 'r', encoding='utf-8') as file:
            file_content = file.read()
    except IOError:
        raise HTTPException(status_code=500, detail="Ошибка чтения файла")

    if prompt.text:
        category = await classify_query(prompt.text)
        try:
            with open(f'./doc/{category}.txt', 'r', encoding='utf-8') as file:
                file_content1 = file.read()
        except IOError:
            raise HTTPException(status_code=500, detail="Ошибка чтения файла")
        category = file_content1
        yandex_response = await send_to_yandex(prompt.text, file_content, category)
        yandex_text = yandex_response.get("choices")[0].get("message").get("content") if yandex_response.get(
            "choices") else ""
        return JSONResponse(content=jsonable_encoder({"message": yandex_text}))
    else:
        raise HTTPException(status_code=400, detail="Недостаточно данных в запросе")


async def classify_query(prompt: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(classifier_url, json={"text": prompt})

            if response.status_code == 200:
                return response.json().get("category", "unknown")
            else:
                raise HTTPException(status_code=500, detail="Ошибка запроса к классификатору")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка классификации запроса: {str(e)}")


async def send_to_yandex(prompt: str, system_message: str, category: str):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Bearer {iam_token}",
        "x-folder-id": folder_id,
        "Content-Type": "application/json",
    }
    system_message = (
    'Вы являетесь системой вопрос-ответ на основе документации, которую я предоставлю. Ваша задача - анализировать текст, который я вам отправлю, и отвечать на вопросы, используя предоставленную информацию и ссылки. Текст будет включать вопросы, иногда отмеченные знаком вопроса, и последующий ответ с указанием ссылок для более детального изучения. '
    'Вам необходимо следовать следующим шагам: '
    '1. Изучить предоставленный текст и ссылки, чтобы понять контекст и детали. '
    '2. Ответить на каждый вопрос, основываясь на тексте ответа и информации по ссылкам. '
    '3. Если конкретной информации по вопросу нет, составить логичный и правдоподобный ответ, используя ваш общий знаниевый фонд, как если бы такая информация существовала. '
    '4. Всегда отвечать на русском языке. '
    '5. Отвечать исключительно на вопросы, касающиеся RuStore. '
    '6. Использовать официальный и деловой стиль в своих ответах. '
    'Пожалуйста, следуйте этим инструкциям точно, чтобы ваши ответы были максимально полезными и соответствовали предоставленной информации.'
                ) + '\n\n' + system_message
    data = {
        "modelUri": model_uri,
        "completionOptions": {
            "stream": False,
            "temperature": 0.1,
            "maxTokens": 2000
        },
        "messages": [
            {"role": "system", "text": system_message},
            {"role": "user", "text": f"Category: {category}\n\n{prompt}"}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=500, detail="Ошибка запроса к YandexGPT")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

