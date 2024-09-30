import traceback

def get_error_message(exc ,traceback):
    res_html = """
    <div>
        <h1> Error: {exc} </h1>
        <h4> Traceback: </h4>
        <pre> {traceback} </pre>
        <a href="/" class="btn btn-primary">Go Back Home</a>
    </div>
    """
    return res_html.format(exc=exc, traceback=traceback)

def debug_exception_handler(resp, exception):

    resp.text = get_error_message(exception, traceback.format_exc())
    