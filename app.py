from flask import Flask, render_template, request
from script.comment_classification import *
import seaborn as sns
from hashlib import md5


app = Flask(__name__)

def custom_style(category):
    return """
    <div style="
        color: white;
        background: linear-gradient(to right, #B39DDB, #CE93D8);
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        text-align: center;
        box-shadow: 0px 3px 15px rgba(0,0,0,0.2);
        border: 2px solid #E1BEE7;
        font-family: 'Lucida Console', Monaco, monospace;
        font-size: 16px;
        font-weight: bold;
    ">
        """ + category + "</div>"

# Precompute some distinct colors for visualization
colors = sns.color_palette("pastel", 20).as_hex()

@app.route('/', methods=['GET', 'POST'])
def review_analyser():
    result = None
    user_input = ''

    if request.method == 'POST':
        user_input = request.form.get('review')
        raw_result = comment_classification(user_input)
        
        comments = []
        for idx, comment in enumerate(raw_result['Comments']):
            text_position = comment['Text_Position']
            start = user_input.find(text_position)

            if idx != len(raw_result['Comments']) - 1:
                end = user_input.find(raw_result['Comments'][idx+1]['Text_Position'])
                full_text = user_input[start:end].strip()
            else:
                full_text = user_input[start:].strip()

            # Generate unique color for each category using its hash
            color_index = int(md5(comment['Category'].encode()).hexdigest(), 16) % len(colors)
            category_color = colors[color_index]

            comments.append({**comment, 'Full_Text': full_text, 'Color': category_color})

        # Split the input and place span with highlight class around full_text
        highlighted_input = user_input
        for comment in comments:
            highlighted_input = highlighted_input.replace(comment['Full_Text'], f"<span class='highlight' style='background-color:{comment['Color']}'>{comment['Full_Text']}</span>")

        result = {'Main_Category': raw_result['Main_Category'], 'Comments': comments, 'Highlighted_Input': highlighted_input}

    return render_template('home.html', input=user_input, result=result, custom_style=custom_style)

if __name__ == '__main__':
    app.run(debug=True)