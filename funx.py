from flask import Flask, render_template, request
from EvalVisitor import EvalVisitor

app = Flask(__name__)
results = []
visitor = EvalVisitor()

if __name__ == '__main__':
    app.run()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['input']
        try:
            str_result = str(visitor.Result(input_text))
            s = "Input: " + input_text + ", Output: " + str_result
        except Exception as e:
            s = "Input: " + input_text + ", Output: " + str(e)
        results.append(s)
        if len(results) > 5:
            results.pop(0)

        functions = visitor.getFunctions()

        return render_template(
            'base.html', input_text=input_text, results=results, functions=functions)

    else:
        return render_template('base.html')
