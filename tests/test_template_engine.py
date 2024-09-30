from osa.globals import response
from .utils import abs_url 


def test_template_rendering(app,client):
    @app.route('/testTemplate')
    def testTemplate():
        response.body = app.template('test.html', {'name': 'World'}).encode()
    
    local_response = client.get(abs_url("/testTemplate"))
    print(local_response.text)
    assert local_response.status_code == 200
    assert "<h1>Hello, World</h1>" in local_response.text


