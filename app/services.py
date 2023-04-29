"""
Use this module to register required services.
Services registered inside a `rodi.Container` are automatically injected into request
handlers.

For more information and documentation, see:
    https://www.neoteroi.dev/blacksheep/dependency-injection/
"""
from typing import Tuple

from roconfiguration import Configuration
from rodi import Container

from core.events import ServicesRegistrationContext

from domain.businesslogic.blA import BusinessLogic


"""
Метод add_instance используется для регистрации экземпляра объекта в контейнере. Этот метод принимает один аргумент - экземпляр объекта, который нужно зарегистрировать.

Метод add_transient используется для регистрации сервиса как временного. Это означает, что каждый раз, когда сервис запрашивается, будет создаваться новый экземпляр. Этот метод принимает один аргумент - класс сервиса, который нужно зарегистрировать.

Кроме того, есть метод add_singleton, который используется для регистрации сервиса как одиночки. Это означает, что будет создан только один экземпляр сервиса, который будет использоваться повторно на протяжении всего времени жизни контейнера.
"""


def configure_services(
    configuration: Configuration,
) -> Tuple[Container, ServicesRegistrationContext, Configuration]:
    container = Container()

    context = ServicesRegistrationContext()

    container.add_instance(configuration)
    container.add_transient(BusinessLogic)




    # Use the container object for example to register dependent services such as
    # classes used to connect to a database or other services, or to handle business
    # logic. Services registered here automatically injected into request handlers
    # when their function signature is type annotated with matching types.

    return container, context, configuration
