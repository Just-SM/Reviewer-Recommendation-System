import asyncio


async def some_coroutine(x):
    await asyncio.sleep(5)
    print(x)
    qd = input()
    return 'done'


ioloop = asyncio.get_event_loop()
tasks = [some_coroutine(x) for x in range(5)]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()