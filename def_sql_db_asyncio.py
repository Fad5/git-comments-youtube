import aiosqlite
import sqlite3


async def add_data_video(db, id_video):
    try:
        c = await db.cursor()
        await c.execute(' INSERT INTO video_bd_table (video)  VALUES (?)',(id_video,))
        await db.commit()
    except sqlite3.IntegrityError:
        pass
    cur = await db.cursor()
    await cur.execute(f"""SELECT id FROM video_bd_table WHERE video == '{id_video}'""")
    result = await cur.fetchall()
    return result


async def add_data_athor(db, id_athor_channel):
    try:
        c = await db.cursor()
        await c.execute('INSERT INTO authorChannelId_bd_table (authorChannelId) VALUES (?)',(id_athor_channel,))
        await db.commit()
    except sqlite3.IntegrityError:
        pass
    cur = await db.cursor()
    await cur.execute(f"SELECT id FROM authorChannelId_bd_table WHERE authorChannelId == '{id_athor_channel}'")
    record = await cur.fetchall()
    return record


async def insert_event(db, id_comment, id_video, id_channel, text_commment, publishedAt):
    """Insert a new event into the events table"""
    try:
        sql = """INSERT INTO main_table 
                  (id_comment, id_video, id_channel, text_commment, publishedAt)  
                  VALUES (?, ?, ?, ?, ?)"""
        await db.execute(sql, (id_comment, id_video, id_channel, text_commment, publishedAt))
        await db.commit()
    except:
        pass
    
    
async def main(id_comment, id_video, id_channel, text_commment, publishedAt):  
    async with aiosqlite.connect('COMMENTS_MAIN.db') as db:
            id_in_db_author = await add_data_athor(db=db, id_athor_channel=id_channel)
            id_in_db_video = await add_data_video(db=db, id_video=id_video)
            await insert_event(db, id_comment, id_in_db_video[0][0], id_in_db_author[0][0], text_commment, publishedAt)