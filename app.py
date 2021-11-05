from transformers import pipeline, set_seed
import streamlit as st
import random

@st.cache(allow_output_mutation=True)
def create_generator():
    return pipeline('text-generation', model='gpt2')

set_seed(42)
generator = create_generator()

def get_results(user_input, length, num_examples):
    return generator(user_input, max_length=length, num_return_sequences=num_examples)

st.title("**Create your own story with** GPT2 :brain:")
st.header("Lacking inspiration ? Let the algorithm work for you and write a story all by itself ! All you need is a sentence to start the magic. :books:")
st.write("GPT2 is a NLP model developed by the team of OpenAI - [take a closer look to their work](https://openai.com/blog/better-language-models/).")
st.write("Choose the length of your story hereunder :")

length = st.slider("Number of words expected", 10, 500, 120, 10)

st.write("Do you fully trust the algorithm or would you like to have several choices to begin your story ?")

num_examples = st.selectbox("Number of examples", [1, 2, 3, 4, 5], index = 2)

st.write("For better results, your input has to be in English :black_nib:")

user_input = st.text_input("Start your journey here")

if user_input == "":

    st.header("Still no idea ? No inspiration ? :confused:")
    # choice = st.button("Really ?")
    # if choice :

    st.write("Please use one of the following topic :")
    # random_topics = generator("", max_length=70, num_return_sequences=3)
    topic = st.radio("Choose one of the topic", ["A train carriage containing controlled nuclear materials was stolen in Cincinnati today. Its whereabouts are unknown.", "Legolas and Gimli advanced on the orcs, raising their weapons with a harrowing war cry.", "Recycling is good for the world. NO! YOU COULD NOT BE MORE WRONG!!"])
    st.session_state['topic'] = topic
    selected_topic = st.session_state['topic']
    predict = st.button("I want more information !")

    if predict:
        second_length = length * 2
        result = generator(selected_topic, max_length=second_length, num_return_sequences=1)
        complete_story =st.write(result[0]["generated_text"])

else :

    result = get_results(user_input, length, num_examples)
    st.session_state["result"] = result

    if st.session_state["result"]:
        st.write("Here are several examples of how your story can continue. Choose the one that you like the most and continue right after !")
        follow_story = st.radio("Choose the story that you like the most", [st.session_state["result"][i]["generated_text"] + "\n" for i in range(len(st.session_state["result"]))])
        # follow_story = st.session_state["result"][0]["generated_text"]
        st.write("Here is the first part of your story :")
        st.write(follow_story)

        st.header("Do you want more ?")

        second_length = st.slider("How much more ?", length*2, length*4, length*3, 10)

        predict = st.button("Continue your journey here !")

        if predict:
            second_length = length * 2
            result = generator(follow_story, max_length=second_length, num_return_sequences=1)
            complete_story =st.write(result[0]["generated_text"])

