from roconfiguration import Configuration
from rodi import Container

from blacksheep.server import Application
from core.events import ServicesRegistrationContext
from essentials.folders import ensure_folder

from .di import dependency_injection_middleware
from .errors import configure_error_handlers
from .docs import docs
import os
import importlib

async def before_start(application: Application) -> None:
    application.services.add_instance(application)
    application.services.add_alias("app", Application)

def configure_controllers(app):
    controllers_path = os.path.dirname(__file__) + '/controllers'
    # Call set_app function to set app variable in controllers module
    controllers_module = importlib.import_module('app.controllers', __name__)
    controllers_module.set_app(app)
    for filename in os.listdir(controllers_path):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            module = importlib.import_module(f'app.controllers.{module_name}', __name__)


def configure_cors(app):
    app.use_cors(
        allow_methods="*",
        allow_origins="*",
        allow_headers="* Authorization",
        max_age=300,
    )

    # specific cors for some routes
    app.add_cors_policy(
        "example",
        allow_methods="GET POST",
        allow_origins="*",
    )
    app.add_cors_policy("deny")



def configure_application(
    services: Container,
    context: ServicesRegistrationContext,
    configuration: Configuration,
) -> Application:
    app = Application(
        services=services,
        show_error_details=configuration.show_error_details,
        debug=configuration.debug,
    )

    app.on_start += before_start


    app.on_start += context.initialize
    app.on_stop += context.dispose

    app.use_sessions("<SIGNING_KEY>")

    app.middlewares.append(dependency_injection_middleware)

    ensure_folder("app/static")
    app.serve_files("app/static", fallback_document="index.html", allow_anonymous=True)

    configure_error_handlers(app)
    configure_cors(app)
    configure_controllers(app)

    docs.bind_app(app)
    return app
