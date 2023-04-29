from rich.console import Console
from rich.progress import Progress
from blacksheep import StreamedContent, Response, JSONContent
import json
import anyio
from io import StringIO
from uuid import UUID
from datetime import datetime

progresses = {}
results = {}
app = None


def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def set_app(new_app):
    global app
    app = new_app

    @app.router.get("/track/{task_id}")
    async def stream_progress(request, task_id: UUID):
        """
            Отслеживания прогресса выполняемой задачи. В качестве аргумента принимается task_id
        и в качестве ответа возвращается поток данных с информацией о состоянии прогресса.
        Parameters
        ----------
        task_id : UUID созданной задачи
        """
        # get the progress id from the json body
        progress = progresses.get(task_id)

        if progress is None:
            return Response(404, content=JSONContent({"error": "Progress not found"}))

        if progress.finished:
            res = results.get(task_id)
            res = json.dumps(res, ensure_ascii=False, default=datetime_serializer)
            return Response(200, content=JSONContent(res))

        async def provider():
            while not progress.finished:
                await anyio.sleep(1)
                json_output = progress.get_json()

                yield json.dumps(json_output, ensure_ascii=False).encode() + b"\n\n"

            #     if progress.finished:
            #         result = results.get(task_id)
            #         yield json.dumps(result).encode() + b"\n\n"
            #
            # result = results.get(task_id)
            # yield json.dumps(result).encode() + b"\n\n"

        return Response(200, content=StreamedContent(b"application/json", provider))


class SSEProgress(Progress):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, console=Console(file=StringIO()))

    def get_json(self):
        result = []
        for i in self.tasks:
            result.append(
                {
                    "completed": i.completed,
                    "total": i.total,
                    "percentage": i.percentage,
                    "speed": i.speed,
                    "time_remaining": i.time_remaining,
                    "elapsed": i.elapsed,
                }
            )
        ans = {"result": result, "message": self.console.file.getvalue()}
        return json.dumps(ans)
