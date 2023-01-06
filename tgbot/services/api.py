import aiohttp
import asyncio
import requests

async def sessionss():
    return aiohttp.ClientSession()



# TODO: language implementation
async def categories(lang, sess: aiohttp.ClientSession):
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
    async with sess as session:
        async with session.get(f'http://139.162.159.187:8000/{lang}/extra-category/') as resp:
            resp = await resp.json()
            ret = dict()
            for response in resp:
                ret[response['id']] = response["extra_category_name"]
            print(ret)
            return ret


async def register_user(chat_id, full_name, phone_number, gender, education, age, progra_language, extra_skills, resume_name, lang):
    payload={'chat_id': chat_id,
    'full_name': full_name,
    'phone_number': phone_number,
    'gender': gender,
    'education': education,
    'age': age,
    'program_language': progra_language,
    'extra_skill': extra_skills,
    'cv': open(resume_name, 'rb') }
    # files=[
    # ('cv',(resume_name,open(resume_name,'rb'),'application/json'))]
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://139.162.159.187:8000/{lang}/register/', data=payload) as resp:
            resp = await resp.text()

            print(resp)
            return resp

# def register(chat_id, full_name, phone_number, gender, education, age, progra_language, extra_skills, resume_name, lang):
#     url = f"http://139.162.159.187:8000/{lang}/register/"

#     payload={'chat_id': chat_id,
#     'full_name': full_name,
#     'phone_number': phone_number,
#     'gender': gender,
#     'education': education,
#     'age': age,
#     'program_language': progra_language,
#     'extra_skill': extra_skills}
#     files=[
#     ('cv',(f'{resume_name}',open(f'{resume_name}','rb'),'application/json'))
#     ]
#     headers = {}

#     response = requests.request("POST", url, headers=headers, data=payload, files=files)

#     print(response.text)

asyncio.run(register_user(lang='ru', chat_id='123456',progra_language='1', full_name='Abdulloh a a', phone_number="998888888", gender='E', education="Oliy", age="18-24", extra_skills=['1', '2'], resume_name='1357813137 resume HR-agrozamin.postman_collection.json'))