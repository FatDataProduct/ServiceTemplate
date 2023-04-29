from datetime import datetime
from domain.DTO.date import ParsingDates
from domain.models.modelA import Amodel, Dialog, ExportRequest, Status
from uuid import UUID, uuid4
from blacksheep.server.openapi.common import (
    ContentInfo,
    EndpointDocs,
    HeaderInfo,
    RequestBodyInfo,
    ResponseExample,
    ResponseInfo,
)

find_active_sessions_docs = EndpointDocs(
    summary="Find active sessions",
    description="Finds all active sessions and returns them in a list",
    request_body=RequestBodyInfo(
        description="List of sessions to check for active status",
        examples={
            "sessions": [Amodel(app_id=1, hash_id="hash1"), Amodel(app_id=2, hash_id="hash2")]
        },
    ),
    responses={
        200: ResponseInfo(
            "A list of active sessions",
            content=[
                ContentInfo(
                    Amodel,
                    examples=[
                        ResponseExample(
                            Amodel(
                                app_id=1, hash_id="hash1", phone_number="+7999999999", session_name="session1"
                            )
                        )
                    ],
                )
            ],
        ),
    },
)

export_dialogs_docs = EndpointDocs(
    summary="Export dialogs",
    description="Exports a list of dialogs based on given ExportRequest",
    request_body=RequestBodyInfo(
        description="ExportRequest containing dialog ids to be exported",
        examples={
            "export_request": ExportRequest(session_name="session1", dialog_ids=[1, 2, 3])
        },
    ),
    responses={
        200: ResponseInfo(
            "A list of exported dialogs",
            content=[
                ContentInfo(
                    Dialog,
                    examples=[
                        ResponseExample(
                            Dialog(id=1, name="Dialog 1", type="Type 1")
                        )
                    ],
                )
            ],
        ),
    },
)
