import anyio
import httpx


class HttpGetter:
    def __init__(self, urls, batch_size, progress):
        self.batches = [
            urls[i : i + batch_size] for i in range(0, len(urls), batch_size)
        ]
        self.responses = []
        self.errors = []
        self.progress = progress
        self.task_id = self.progress.add_task("Fetching URLs", total=len(urls))

    async def __aenter__(self):
        # self.nursery = await trio.open_nursery().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        ...
        # await self.nursery.__aexit__(exc_type, exc_value, traceback)

    async def process_batch(self, batch):
        async with httpx.AsyncClient(timeout=30) as client:
            for url in batch:
                await anyio.sleep(1)
                try:
                    response = await client.get(url)
                    self.responses.append(response)
                    self.progress.console.print(f"[green]fetched[/] {url} ")
                except Exception as exc:
                    self.errors.append((url, exc))
                    self.progress.console.print(f"[red]error[/] {url}")
                finally:
                    self.progress.advance(self.task_id)

    async def run(self):
        async with anyio.create_task_group() as nursery:
            for batch in self.batches:
                await nursery.spawn(self.process_batch, batch)
