import anyio
import tractor
from typing import List
from app.models.modelA import Amodel, Dialog, ExportRequest, Status

class BusinessLogic:

    async def find_active_sessions(self, sessions: List[Amodel]) -> List[Amodel]:
        active_sessions = []
        async with anyio.create_task_group() as tg:
            for session in sessions:
                tg.start_soon(self.check_active_session, session, active_sessions)
        return active_sessions

    async def check_active_session(self, session: Amodel, active_sessions: List[Amodel]):
        async with tractor.open_nursery() as nursery:
            async with anyio.create_lock():
                if session.status == Status.ACTIVE:
                    active_sessions.append(session)
            nursery.start_soon(self.some_concurrent_operation, session)

    async def some_concurrent_operation(self, session: Amodel):
        # Здесь можно выполнять многопоточные операции с сессиями
        pass

    async def export_dialogs(self, export_request: ExportRequest, dialogs: List[Dialog]) -> List[Dialog]:
        dialogs_to_export = [dialog for dialog in dialogs if dialog.id in export_request.dialog_ids]
        return dialogs_to_export
