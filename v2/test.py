from mistralrs import Runner, Which, ChatCompletionRequest, VisionArchitecture

runner = Runner(
    which=Which.VisionPlain(
        model_id="microsoft/Phi-3-vision-128k-instruct",
        tokenizer_json=None,
        repeat_last_n=64,
        arch=VisionArchitecture.Phi3V,
    ),
)

res = runner.send_chat_completion_request(
    ChatCompletionRequest(
        model="phi3v",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Everest_North_Face_toward_Base_Camp_Tibet_Luca_Galuzzi_2006.jpg"
                        },
                    },
                    {
                        "type": "text",
                        "text": "<|image_1|>\nWhat is shown in this image? Write a detailed response analyzing the scene.",
                    },
                ],
            }
        ],
        max_tokens=256,
        presence_penalty=1.0,
        top_p=0.1,
        temperature=0.1,
    )
)
print(res.choices[0].message.content)
print(res.usage)