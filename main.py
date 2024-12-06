import json

from aiohttp import web

routes = web.RouteTableDef()


@routes.get('')
@routes.get('/')
@routes.post('')
@routes.post('/')
async def home(request: web.Request):
    with open('h.html', 'rt', encoding='utf8') as file, open('recipes.json', 'rt', encoding='utf8') as jsonic:
        jsonic = jsonic.read().replace('<', '&lt;').replace('>', '&gt;')
        jsonic = jsonic.replace('&', '&amp;').replace('"', '&quot;')
        text = file.read().replace('$recipes', jsonic.replace("'", '&#39;'))
    return web.Response(body=text, content_type='text/html', charset='UTF-8')


@routes.post('/post')
async def home(request: web.Request):
    array = dict(await request.post())
    with open('recipes.json', 'rt', encoding='utf8') as file:
        arrays = json.loads(file.read())
    arrays.append(array)
    with open('recipes.json', 'wt', encoding='utf8') as file:
        file.write(json.dumps(arrays, indent=2))
    return web.Response(status=307, headers={'Location': '/'})


app = web.Application()
app.add_routes(routes)
web.run_app(app, host='127.0.0.1')
