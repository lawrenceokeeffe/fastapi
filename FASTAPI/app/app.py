from fastapi import FastAPI
app = FastAPI()
from data_store import deps

import asyncio
import requests
import json


URL = "https://registry.npmjs.org/"

def request_foreign(temp):
    r = requests.get(URL + temp)
    return r.text

@app.get("/",tags=['ROOT'])
async def root() -> dict:
    return{"Ping":"Pong"}

@app.get('/dependency/info/{dep}', tags=['dependencies'])
async def get_dependency(dep:str)-> dict:
    full_data = deps.data
    if dep in full_data['dependencies']:
        type_final = 'dependency'
        version = full_data['dependencies'][dep]
    elif dep in full_data['devDependencies']:
        type_final = 'devDependency'
        version = full_data['devDependencies'][dep]

    final_object = {
        "version": version,
        "type": type_final
    }
    
    return{"data": final_object}


@app.get('/dependency/version-check/{dep}', tags=['dependencies'])
async def compare_dependency(dep:str)-> dict:
    
    my_dependency = await asyncio.gather(get_dependency(dep))
    
    my_dep_str = my_dependency[0]["data"]["version"]
    my_dep_ints = list(map(int, my_dep_str.split(".")))
    foreign_dependency = json.loads(request_foreign(dep))
    foreign_dep_str = foreign_dependency["dist-tags"]["latest"]
    foreign_dep_ints = list(map(int, foreign_dep_str.split(".")))

    if foreign_dep_ints[0] != my_dep_ints[0]:
        major = True
    else:
        major = False
    if foreign_dep_ints[1] != my_dep_ints[1]:
        minor = True
    else:
        minor = False
    if foreign_dep_ints[2] != my_dep_ints[2]:
        patch = True
    else:
        patch = False

    
    return_value = {
        "major": major,
        "minor": minor,
        "patch": patch
    }

    return{"data": return_value }
    




