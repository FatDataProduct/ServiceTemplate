from blacksheep.server.controllers import ApiController, get, post
from blacksheep.contents import JsonContent
from blacksheep import Request, Response

from app.controllers.apidocs.docsA import find_active_sessions_docs, export_dialogs_docs
from domain.DTO.date import ParsingDates
from domain.models.modelA import ExportRequest
from domain.bisneslogic.blA import BusinessLogic

def handle_non_serializable(obj):
    return str(obj)

class BusinessLogicController(ApiController):
    @classmethod
    def version(cls) -> str:
        return "v1"

    @classmethod
    def route(cls) -> str:
        return cls.version() + "/business"

    @post("/active-sessions/", docs=find_active_sessions_docs)
    async def active_sessions(request: Request, business_logic: BusinessLogic) -> Response:
        sessions = await business_logic.find_active_sessions()
        return Response(200, content=JsonContent(sessions, json_dumps_kwargs={'default': handle_non_serializable}))

    @post("/export-dialogs/", docs=export_dialogs_docs)
    async def export_dialogs(request: Request, business_logic: BusinessLogic, export_request: ExportRequest) -> Response:
        dialogs = await business_logic.export_dialogs(export_request)
        return Response(200, content=JsonContent(dialogs, json_dumps_kwargs={'default': handle_non_serializable}))

