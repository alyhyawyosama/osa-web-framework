
from osa.globals import  response

def test_not_found_error(app, client):
    err = "non-existent page"
    
    @app.errorhandler(404)
    def not_found_error(error):
        response.text = err
    res = client.get('http://testserver/404') 
    assert res.text == err  
    