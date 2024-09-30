
# Osa Framework

**Osa** is a lightweight [WSGI](https://wsgi.readthedocs.io/) web application framework built for learning purposes. Inspired by popular Python frameworks like Flask, it provides developers with essential tools to understand how modern web frameworks operate under the hood. Osa is an excellent resource for learning routing, middleware, and request/response handling in web applications. 

Table of content :

[Story](#story)
[Installation](#installation)
[Example of a Simple  App](#example-of-a-simple-app)
[Key features](#key-features)
[Setting Up Your Project Structure](#setting-up-your-project-structure)
[Creating Your First App](#creating-your-first-app)
[Working with Templates and Static Files](#working-with-templates-and-static-files)
[Running the App](#running-the-app)
[Advanced Usage](#advanced-usage)
[Template Rendering](#template-rendering)
[Static Files](#static-files)
[Resources](#resources)

## <a id="story">Story</a>

I never had a deep love for Python. In fact, I didn't even enjoy working with it. But during my final year at university, everything changed. My team and I decided to build a project that could make a real impact, something beneficial for our University  or for government organization  
to help speed up their processes  and people's transactions .
We approached one such organization, they agreed. However, they had one condition: the system had to be built using Frappe—a Python-based web framework.

Suddenly, I found myself diving headfirst into a language and framework I didn't particularly like, just to meet the project’s demands. As we started learning Frappe, I constantly bumped into elements I didn’t understand—things that I knew how to use but didn’t know how they worked under the hood. This didn’t sit right with me. I’ve always had a curious mind, and knowing how things work behind the scenes is something I value deeply.

Frustrated by the lack of detailed resources explaining the core workings of Frappe, I turned to Flask, a more widely known Python framework with rich documentation. I dug deeper, practicing with projects and discovering how different components interacted in the background. Medium articles and other sources became my guides as I slowly pieced together the puzzle of how web frameworks operate.

As I learned, I started experimenting by building the main functions of a framework myself. I wasn't content with just using prebuilt tools—I wanted to construct them. Step by step, I wrote functions, broke things, fixed them, and began to understand how everything fit together. It was born from this desire to learn, not out of necessity or love for Python, but out of curiosity. It’s not meant for real-world applications but for exploration—something to help people understand how web frameworks work at a fundamental level, just like I wanted to when I first started.


## <a id="installation">Installation</a>

1. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Install Osa**:

   ```bash
   pip install -i https://test.pypi.org/simple/ osa-web-framework==0.0.1
   ```

---

## <a id="example-of-a-simple-app">Example of a Simple  App</a>

```python
from osa import Osa, request, response

app = Osa()

@app.route("/")
def home():
    response.text = "Welcome to Osa Framework!"

@app.route("/hello/<name>",methods=["GET"])
def greet_user(name):
    response.text = f"Hello, {name}!"

if __name__ == "__main__":
    app.run()
```

---

## <a id="key-features">Key features</a>

- **Command-Line Interface (CLI)**: Manage the server easily with Osa’s CLI.
- **WSGI Compatibility**: Compatible with WSGI servers like Gunicorn and uWSGI.
- **Routing System**: Supports path parameters, method-based and class-based routing.
- **Middleware Support**: Easily handle tasks before and after requests.
- **Static File Handling**: Efficient serving of CSS, JavaScript, and images.
- **Custom Error Handling**: Create custom error responses for status codes.
- **Context Management**: Each request has its own isolated context, providing global access to request/response objects during a request's lifecycle.

---

## <a id="setting-up-your-project-structure">Setting Up Your Project Structure</a>

To start using Osa, it’s helpful to follow a recommended project layout. Here’s a structure for organizing templates, static files, and more:

```
my_osa_project/
│
├── venv/                     # Virtual environment
├── app.py                    # Main application file
├── static/                   # Static files (CSS, JavaScript, images)
│   ├── css/
│   └── js/
├── templates/                # HTML templates
│   └── index.html

```

---

## <a id="creating-your-first-app">Creating Your First App</a>

In your project folder, create `app.py`:

```python
from osa import Osa, request, response

app = Osa()

@app.route("/")
def index():
    response.text = "Welcome to Osa Framework!"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
```

---

## <a id="working-with-templates-and-static-files">Working with Templates and Static Files</a>

### 1. **Setting Up Templates**

- Create a `templates` folder in your project.
- Inside the folder, add your HTML files (e.g., `index.html`):

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Osa</title>
</head>
<body>
    <h1>{{ greeting }}</h1>
</body>
</html>
```

To render the template in your route:

```python
@app.route("/")
def index():
    return app.template("index.html", {"greeting": "Welcome to Osa Framework!"})
```

### 2. **Serving Static Files**

- Create a `static` folder with subfolders like `css`, `js`, etc.
- Example CSS file (`static/css/style.css`):

```css
/* static/css/style.css */
body {
    background-color: #f0f0f0;
    font-family: Arial, sans-serif;
}
```

To include the static file in your HTML template:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

---

## <a id="running-the-app">Running the App</a>

You can run your Osa application using the CLI:

```bash
osa run --host 127.0.0.1 --port 5000
```

Alternatively, set environment variables:

```bash
export OSA_APP=app:app   # (Linux)
set OSA_APP=app:app      # (Windows)
osa run
```

Osa will search for `app.py` or `wsgi.py` and look for the `app` object.

#### Running the Server

```bash
osa run
```
### more Details :
#### Command-Line Options

```bash
osa run --help
```

Usage:

```bash
osa run [OPTIONS]
```
Options:
- `--host TEXT`: Specify the host to bind the server to. Example: `osa run --host 0.0.0.0`
- `--port INTEGER`: Specify the port to run the server on. Example: `osa run --port 8000`
- `--app TEXT`: Specify the WSGI application to run, in the format `filename:app_variable`. Example: `osa run --app myapp:app`
- `--no-debug`: Disable debug mode. Debug mode is enabled by default and provides helpful error messages and live reloading during development. Example: `osa run --no-debug`
- `--help`: Show the help message and exit.
#### How Osa Locates Your Application
Osa will automatically search for the following files in the directory you run the command from:
- `wsgi.py`
- `app.py`
Within these files, Osa looks for an `app` variable that holds the WSGI application. If you want to use a different filename or variable, you can specify it with the `--app` option.

Example with all arguments (they are all optional):
```bash
osa run --host 127.0.0.1 --port 5000 --app myapp:app --no-debug 
```


---
## <a id="advanced-usage">Advanced Usage</a>

### **Routing with URL Parameters**

```python
@app.route("/hello/<name>")
def greet(name):
    response.text = f"Hello, {name}!"
```

### **Handling Static and Dynamic Content**

Class-based routing example:

```python
@app.route("/item/<item_id>", methods=["GET","POST","PUT"])
class ItemHandler:
    def get(self, item_id):
        response.text = f"Fetching item {item_id}"

    def post(self, item_id):
        response.text = f"Item {item_id} added "
    def PUT(self,item_id):
	    response.text = f"Update item{item_id}"
	    
```

### **Custom Error Handling**

Define custom error responses:

you can use the `abort` function to raise HTTP exceptions with custom status codes and error messages


```python
from osa import Osa, abort , request , response
app = Osa()
@app.errorhandler(404)
def not_found():
    response.text = "Page not found."

@app.route("/admin")
def admin_panel():
    user_authenticated = False
    if not user_authenticated:
        abort(403, "Forbidden: You are not authorized to access the admin panel.")
    response.text = "Welcome to the Admin Panel!"

```

### **Middleware**

Run functions before and after requests:

```python
@app.before_request
def log_request():
    print(f"Request received: {request.path}")

@app.after_request
def add_headers():
    response.headers["X-Framework"] = "Osa"
```

---

## <a id="template-rendering">Template Rendering</a>

The default folder for template files is templates. You can change this by setting the templates_dir attribute when creating the Osa instance.

```python
app = Osa(templates_dir="templates_directory")
```

To use the template engine, place your HTML files in the `templates` directory and render them using:

```python
@app.route("/greet")
def greet_template():
    response.text = app.template("greet.html", {"name": "Osa User"})
```

Example HTML template (`greet.html`):

```html
<h1>Hello, {{ name }}!</h1>
```

---

## <a id="static-files">Static Files</a>

By default, static files are served from the `static` folder. You can change this using:

```python
app = Osa(static_dir="my_static")
```

In your HTML files, link static assets like so:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

---
### More examples 
Example 1 
```python
@app.route('/register', methods=['POST', 'GET'])
def register():
    html_form = """

    """
    if request.method == 'GET':
        response.text = app.template('register.html')
    elif request.method == 'POST':
	    #request.POST like request.form in flask 
        print(request.POST['username'])
        print(request.POST['password'])
        # You must sanitize the input before using it in your application ,
        #but for now we will just use it as is
        input_username = request.POST['username']
        response.text = f"Hello, {input_username}! You have successfully registered."
```

```html
<!-- register.html -->
<html>
    <body>
        <form method="post" action="/register">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="Register">
        </form>
    </body>
</html>
```


example 2
```python
@app.route("/item/<item_id>", methods=["GET","POST","PUT"])
class ItemHandler:
    def get(self, item_id):
        response.text = f"Fetching item {item_id}"

    def post(self, item_id):
        response.text = f"Item {item_id} added "
    def PUT(self,item_id):
	    response.text = f"Update item{item_id}"
	
```


## <a id="resources">Resources</a>

- [Flask Documentation](https://github.com/pallets/flask)
- [Flask Web Development book]( https://www.amazon.com/Flask-Web-Development-Developing-Applications/dp/1449372627)
- [Alcazar](https://github.com/rahmonov/alcazar)
- [WSGI Guide](https://wsgi.readthedocs.io)
- [Context Management in Python](https://docs.python.org/3/library/contextvars.html)
Other

Python Web Framework
[flasky](https://github.com/miguelgrinberg/flasky)
[Alcazar](https://rahmonov.me/posts/write-python-framework-part-one/)

Wsgi

[WSGI for Web Developers (Ryan Wilson-Perkin)](https://www.youtube.com/watch?v=WqrCnVAkLIo&t=998s&pp=ygULd3NnaSBzZXJ2ZXI%3D "WSGI for Web Developers (Ryan Wilson-Perkin)")
[what-the-hell-is-wsgi-anyway-and-what-do-you-eat-it-with/](https://rahmonov.me/posts/what-the-hell-is-wsgi-anyway-and-what-do-you-eat-it-with/)
[pythons-wsgi-server-application-interface](https://www.toptal.com/python/pythons-wsgi-server-application-interface)

Contextvars :
[python-contextvars-and-multithreading](https://kobybass.medium.com/python-contextvars-and-multithreading-faa33dbe953d)
[keeping-request-context-over-the-function-call-stack](https://medium.com/ssense-tech/keeping-request-context-over-the-function-call-stack-308f23550dcd)
[repository-pattern-with-context-variables](https://medium.com/@sawaamun/repository-pattern-with-context-variables-in-async-python-519728211d67)

--- 
