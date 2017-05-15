from flask import Flask
from flask_restplus import Api, Resource, abort
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


app = Flask(__name__)
api = Api(app, version='1.0', title='Github star history api',
          description='API for getting star history',
          doc='/api/starhistory/doc/')
api.add_resource(StarHistoryAPI, '/api/starhistory/1.0/<user>/<repo>/',
                 endpoint='starhistory')


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
