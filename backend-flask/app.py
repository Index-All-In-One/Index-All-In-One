from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome!'

@app.route('/test')
def api():
    data = {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'phone': '123-456-7890'
    }
    return jsonify(data)

# Custom middleware function to add CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    return response

@app.route('/search', methods=['POST'])
def submit():
    keywords = request.form.get('keywords')
    foo = request.form.get('foo')
    print(keywords)
    print(foo)
    # do something with the data...
    search_results = []
    doc_names = [
        "A very loooooooooooooooooong file name",
        "Apple",
        "Banana",
        "Mango",
        "Pear",
        "Watermelons",
        "Blueberries",
        "Pineapples",
        "Strawberries"]
    for doc_name in doc_names:
        search_results.append(
            {
                "doc_name": doc_name,
                "doc_type": "<Document Type>",
                "link": "<Link>",
                "source": "<Source>",
                "created_date": "<Created Date>",
                "modified_date": "<Modified Date>",
                "summary":
                    "With six children in tow, Catherine raced to the airport departing gate. This wasn't an easy task as the children had other priorities than to get to the gate. She knew that she was tight on time and the frustration came out as she yelled at the kids to keep up. They continued to test her, pretending not to listen and to move in directions that only slowed them down. They had no idea the wrath they were about to receive when Catherine made it to the gate only to be informed that they had all missed the plane.",
                "file_size": "<File Size>"
            })
    return jsonify(search_results)
