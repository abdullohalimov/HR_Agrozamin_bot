# import aiohttp
# import asyncio

# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://httpbin.org//ru/category/') as resp:
#             print(resp.status)
#             print(await resp.text())

# asyncio.run(main())

def categories(lang):
    categores = dict()
    categores["1"] = 'python'
    categores["2"] = "java"
    categores["3"] = 'javascript'
    categores["4"] = 'laravel'
    categores["5"] = 'angular'
    categores["6"] = 'go'
    return categores

def extra_categories(lang):
    categores = dict()
    categores["1"] = 'sql'
    categores["2"] = "html"
    categores["3"] = 'linux'
    categores["4"] = 'bash'
    return categores

# cat = categories('asd')
# for key in cat:
    # print(key, cat[key])