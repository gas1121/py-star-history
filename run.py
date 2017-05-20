from flask import Flask, Blueprint
from werkzeug.contrib.fixers import ProxyFix
from flask_restplus import Api, Resource, abort, apidoc
import star_history


class StarHistoryAPI(Resource):
    def get(self, user, repo):
        try:
            data = star_history.get_star_history(user, repo)
        except star_history.NoEnoughStargazorsError:
            # return message when no enough stars
            result = dict()
            result["message"] = "No enough stars"
            return result
        except (star_history.ReachLimitError,
                star_history.ConnectionError) as error:
            # TODO manage different exceptions
            abort(404)
        return data


# url prefix
url_prefix = '/api/pystarhistory/1.0'


# Blueprint is needed to avoid swagger ui static assets 404 error
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
# register swagger ui static assets to avoid 404 error when use nginx 
# as reverse proxy server with sub path
app.register_blueprint(apidoc.apidoc, url_prefix=url_prefix)

blueprint = Blueprint('starhistory', __name__, url_prefix=url_prefix)
api = Api(blueprint, version='1.0', title='Github star history api',
          description='API for getting star history',
          doc='/doc/')
api.add_resource(StarHistoryAPI, '/<user>/<repo>/',
                 endpoint='starhistory')
app.register_blueprint(blueprint)


@app.after_request
def after_request(response):
    """
    Handle CORS Requests
    """
    # TODO remove CORS support after blog using domain?
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run()
