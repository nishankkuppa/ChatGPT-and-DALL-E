import openai

from APIKeys import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


# This function processes user input through the ChatGPT API
def GPTQuery(myInput):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.5,  # Lower temperature values make the output less random
        max_tokens=256,
        # Instruct the model on how to process certain inputs:
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant. However, if you're asked to generate a picture, delegate to "
                        "DALL-E instead by outputting a query that DALL-E would understand. Indicate this scenario by "
                        "formatting the output exactly like this: Image Query: <query>"},
            {"role": "user", "content": myInput},
        ]
    )

    chatGPTresponse = completion.choices[0].message.content

    # Checks to see if ChatGPT's response needs to be passed to DALL-E
    if "Image Query:" in chatGPTresponse:
        properQuery = chatGPTresponse.replace("Image Query:", "")
        return ImageQuery(properQuery)
    # If not, return ChatGPT's response
    else:
        return chatGPTresponse


def ImageQuery(userInput):
    response = openai.Image.create(
        prompt=userInput,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url


def chatbot():
    while True:
        prompt = input("You: ")
        promptNew = prompt.lower()

        myAnswer = GPTQuery(promptNew)
        print(f"ChatGPT: {myAnswer}")


if __name__ == "__main__":
    chatbot()
