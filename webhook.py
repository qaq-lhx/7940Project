import http

import flask
import telegram


class WebHook:
    def __init__(self, env, app, bot, dispatcher):
        @app.post('/' + env.telegram_webhook_secret_path)
        def on_webhook_request():
            dispatcher.process_update(telegram.Update.de_json(flask.request.get_json(force=True), bot))
            return flask.Response('', status=http.HTTPStatus.NO_CONTENT)

        @app.errorhandler(http.HTTPStatus.NOT_FOUND)
        @app.errorhandler(http.HTTPStatus.METHOD_NOT_ALLOWED)
        def on_unauthorized_request(e):
            status = http.HTTPStatus(http.HTTPStatus.UNAUTHORIZED)
            return flask.Response(str(status.value) + ' ' + status.phrase, status=status.value, mimetype='text/plain')
