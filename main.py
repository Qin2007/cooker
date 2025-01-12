import datetime
import json
import uuid

from aiohttp import web

routes = web.RouteTableDef()


def html_encode(strx: str) -> str:
    strx = strx.replace('&', '&amp;')
    strx = strx.replace('"', '&quot;')
    strx = strx.replace("'", '&#39;')
    return strx.replace('<', '&lt;').replace('>', '&gt;')


@routes.get('')
@routes.get('/')
@routes.post('')
@routes.post('/')
async def home(request: web.Request):
    x = ''
    for i in [['creat_recipe', 'recept aanmaken']]:
        x += f'<li><a href="{i[0]}">{i[1]}</a>'
    thing = '<meta charset=\"UTF-8\"/><style> body, input {font-family: monospace;}'
    thing += "a:visited,a:link{color:blue;}a:hover{color:orangered;}a:active{color:black;}"
    thing += "html,input{font-family:monospace;}</style>"
    thing += '<meta name="viewport" content="width=device-width, initial-scale=1" />'
    with open('recipes.json', 'rt', encoding='utf8') as file:
        things = html_encode(file.read())
    return web.Response(
        body=f"<!DOCTYPE html><html lang=\"nl\">{thing}<title>Cookbook</title><body><h1>kook boek</h1>"
             + f"<h2>links</h2><ul>{x}</ul><h2>Recipes</h2><ol id=elementById></ol>"
             + f"<pre hidden>{things}</pre><script src='javascript1.js'></script>",
        content_type='text/html', charset='UTF-8')
    pass


@routes.get('/javascript1.js')
async def home(request: web.Request):
    with open('javascript1.js', 'rt', encoding='utf8') as file:
        return web.Response(body=file.read(), content_type='text/javascript', charset='UTF-8')


@routes.get('/creat_recipe')
@routes.post('/creat_recipe')
async def home(request: web.Request):
    with open('h.html', 'rt', encoding='utf8') as file, open('recipes.json', 'rt', encoding='utf8') as jsonic:
        text = file.read().replace('$recipes', html_encode(jsonic.read()))
    return web.Response(body=text, content_type='text/html', charset='UTF-8')

@routes.post('/post')
async def home_add_recipe(request: web.Request):
    array = dict(await request.post())
    with open('recipes.json', 'rt', encoding='utf8') as file:
        arrays = json.loads(file.read())
    arrays.append(array)
    array['Date'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    array['uuid'] = str(uuid.uuid4())
    with open('recipes.json', 'wt', encoding='utf8') as file:
        file.write(json.dumps(arrays, indent=4))
    return web.Response(status=307, headers={'Location': '/'})


app = web.Application()
app.add_routes(routes)
web.run_app(app, host='127.0.0.1', port=80)
