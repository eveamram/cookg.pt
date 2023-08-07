import streamlit as st
import os
import openai
from cooklang import parse_cooklang, convert_to_markdown

st.title("cookg.pt")

OPENAI_KEY = os.getenv("OPENAI_COOKGPT_KEY")

openai.api_key = OPENAI_KEY

SECRET_SAUCE = """
Cooklang is a markup language defined with the following rules (examples are given inside ``):

- To define an ingredient, use the @ symbol, indicate the end of the name with {}. `Then add @salt{} and @ground black pepper{} to taste.`
- To indicate ONLY the quantity of an item, place the quantity inside {} after the name. `Poke holes in @potato{2}.`
- To use a unit of an item, such as weight or volume, add a % between the quantity and unit. `Place @bacon strips{1%kg} on a baking sheet and glaze with @syrup{1/2%tbsp}.`
- Add metadata tags to your recipe: title, total prep time, and number of people served. `>> title: Beefy Tuna
>> preparation time: 1.5 hours
>> people served: 4`
- You can define any necessary cookware with #, indicate the end of the name with {}. `Place the potatoes into a #pot{}. Mash the potatoes with a #potato masher{}.`.
- You can define a timer using ~. Indicate the required time with {}. `Lay the potatoes on a #baking sheet{} and place into the #oven{}. Bake for ~{25%minutes}.`

In cooklang you give directly the recipe in steps line by line.
Do not numerate lines.
Avoid printing anything else.
Do not use # to mark sections or steps.

You will be given a cuisine_type, a list of ingredients, a type_of_dish, and a difficulty_level.
There are three difficulty levels:  easy, medium, hard. You should adapt the recipe number of steps and execution difficulty to these levels. 
Difficulty level should drive the culinary technique to be used.
The maximum number of steps must be no more than 12.
You have to provide a recipe for the required type of dish.
You have to adapt the recipe to match the cuisine type provided.
Feel free to add ingredients with respect to the cuisine type.
Provide a funky, creative and imaginative name for your recipe in metadata.
Return only the recipe in cooklang.
"""


def assemble_input(cuisine, ingredients, type_of_dish, difficulty):
    return f"""
    cuisine: {cuisine}
    ingredients: {ingredients}
    type_of_dish: {type_of_dish}
    difficulty_level: {difficulty}
    """


def gen_recipe(cuisine, ingredients, type_of_dish, difficulty):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SECRET_SAUCE},
            {
                "role": "user",
                "content": assemble_input(
                    cuisine, ingredients, type_of_dish, difficulty
                ),
            },
        ],
        temperature=0.8,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )


c1, c2 = st.columns(2)
with c1:
    cuisine = st.text_input("cuisine", placeholder="Korean, British, Italian, ...")

with c2:
    difficulty = st.select_slider("difficulty", ["easy", "medium", "hard"])
ingredients = st.text_input(
    "ingredients",
    placeholder="comma separated list of ingredients",
)
type_of_dish = st.radio(
    "course",
    ["breakfast", "appetizer", "main", "side", "dessert"],
    horizontal=True,
)

with st.spinner():
    if st.button("generate"):
        recipe = gen_recipe(cuisine, ingredients, type_of_dish, difficulty)
        raw = recipe["choices"][0]["message"]["content"]

        stuff = parse_cooklang(raw)

        md = convert_to_markdown(raw, *stuff)
        md = md.replace("```", "")

        st.markdown(md)
