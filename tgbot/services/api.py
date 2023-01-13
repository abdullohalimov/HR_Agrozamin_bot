import aiohttp
# import asyncio
import requests
import json

async def sessionss():
    return aiohttp.ClientSession()

# TODO: language implementation
async def categories(lang, sess: aiohttp.ClientSession):
    if lang == "de":
        lang = 'uz'
    async with sess as session:
        async with session.get(f'http://139.162.159.187:8000/{lang}/category/') as resp:
            resp = await resp.json()
            ret = dict()
            for response in resp:
                ret[response['id']] = response["category_name"]
            print(ret)
            return ret

# TODO: language implementation
async def extra_categories(lang, sess: aiohttp.ClientSession):
    if lang == "de":
        lang = 'uz'
    async with sess as session:
        async with session.get(f'http://139.162.159.187:8000/{lang}/extra-category/') as resp:
            resp = await resp.json()
            ret = dict()
            for response in resp:
                ret[response['id']] = response["extra_category_name"]
            print(ret)
            return ret



def register(chat_id, full_name, phone_number, gender, education, age, progra_language, extra_skills, resume_name, lang):
    url = f"http://139.162.159.187:8000/{lang}/register/"

    payload={'chat_id': chat_id,
    'full_name': full_name,
    'phone_number': phone_number,
    'gender': gender,
    'education': education,
    'age': age,
    'program_language': progra_language,
    'extra_skill': extra_skills}
    files=[
    ('cv',(f'{resume_name}',open(f'{resume_name}','rb'),'application/json'))
    ]
    headers = {}

    response = requests.post(url, headers=headers, data=payload, files=files)

    return response.text


def get_questions(lang, category):
    url = f"http://139.162.159.187:8000/{lang}/question/?category_id={category}"

    response = requests.request("GET", url)
    resp = response.json()
    resp
    dictt = {}
    for i in range(1, len(resp) + 1):

        dictt[f"{i}"] = resp[i-1]

    return dictt


def get_extra_quesions(lang, extra_cat):
    url = f"http://139.162.159.187:8000/{lang}/extra-question/"

    payload = json.dumps({
    "extra_category_id": extra_cat
    })
    headers = {
            'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    resp = response.json()
    dictt = {}
    for i in range(1, len(resp) + 1):

        dictt[f"{i}"] = resp[i-1]

    return dictt

print(get_extra_quesions('uz', [1]))

# print(get_questions('uz', '2'))




# for res in resp:
#     print(res['id'])
#     print(res['question'])
#     print(res['A'])
#     print(res['B'])
#     print(res['C'])
#     print(res['D'])
#     print(res['category'])

# get_questions()

# async def register_user(chat_id, full_name, phone_number, gender, education, age, progra_language, extra_skills, resume_name, lang):
#     if lang == "de":
#         lang = 'uz'
#     payload={'chat_id': chat_id,
#     'full_name': full_name,
#     'phone_number': phone_number,
#     'gender': gender,
#     'education': education,
#     'age': age,
#     'program_language': progra_language,
#     'extra_skill': extra_skills,
#     'cv': open(resume_name, 'rb') }
#     # files=[
#     # ('cv',(resume_name,open(resume_name,'rb'),'application/json'))]
#     async with aiohttp.ClientSession() as session:
#         async with session.post(f'http://139.162.159.187:8000/{lang}/register/', data=payload) as resp:
#             resp = await resp.text()

#             print(resp)
#             return resp


# asyncio.run(register_user(lang='ru', chat_id='123456',progra_language='1', full_name='Abdulloh a a', phone_number="998888888", gender='E', education="Oliy", age="18-24", extra_skills=['1', '2'], resume_name='1357813137 resume HR-agrozamin.postman_collection.json'))
# print(register(lang='ru', chat_id='123456',progra_language='1', full_name='Abdulloh a a', phone_number="998888888", gender='E', education="Oliy", age="18-24", extra_skills=['1', '2'], resume_name='1357813137 resume 1357813137_998998881965.docx'))
