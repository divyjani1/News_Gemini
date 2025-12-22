from Db.db import db
import asyncio
async def get_data()->list[dict]:
    res=await db["english_text"].find().to_list()
    result=[]
    for i in res:
    # print(str("headline:",str(res.headline)))
        # print(str(i["headline"]))
        print("-----------------------------------------------------------------------------")
        result.append(i)
    # print(str("full_text:",res["full_text"]))
    # print(ress)
    return result


# async def main():
#     result=await get_data()
#     print("Resssssulttttt:",result)

# if __name__=="__main__":
#     asyncio.run(main())
#     # res=get_data()

