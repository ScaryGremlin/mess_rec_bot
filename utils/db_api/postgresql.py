from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def exists_schema(self, schema_name):
        sql = f"""
            SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema_name}';
        """
        if len(await self.execute(sql, fetch=True)) == 1:
            return True
        else:
            return False

    async def create_schema(self, schema_name):
        sql = f"""
            CREATE SCHEMA IF NOT EXISTS {schema_name}
        """
        await self.execute(sql, execute=True)

    async def create_table_dict_problems(self, schema_name):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {schema_name}.{config.TABLE_DICT_PROBLEMS} (
                id INT PRIMARY KEY,
                problem VARCHAR(255)
            );
        """
        await self.execute(sql, execute=True)

    async def create_table_struct_messages(self, schema_name):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {schema_name}.{config.TABLE_STRUCT_MESSAGES} (
                id SERIAL PRIMARY KEY,
                message_id INT,
                reply_id INT,
                hub INT,
                city VARCHAR(255),
                number_problem INT,
                user_id BIGINT,
                full_name VARCHAR(255),
                user_name VARCHAR(255) NULL,
                message_text VARCHAR(255),
                date_time TIMESTAMP
            );
        """
        await self.execute(sql, execute=True)

    async def create_table_unstruct_messages(self, schema_name):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {schema_name}.{config.TABLE_UNSTRUCT_MESSAGES} (
                id SERIAL PRIMARY KEY,
                message_id INT,
                reply_id INT,
                user_id BIGINT,
                full_name VARCHAR(255),
                user_name VARCHAR(255) NULL,
                message_text VARCHAR(255),
                date_time TIMESTAMP
            );
        """
        await self.execute(sql, execute=True)

    async def create_table_dict_operators(self, schema_name):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {schema_name}.{config.TABLE_DICT_OPERATORS} (
                operator_id BIGINT PRIMARY KEY
            );
        """
        await self.execute(sql, execute=True)

    async def create_table_service_messages(self, schema_name):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {schema_name}.{config.TABLE_SERVICE_MESSAGES} (
                message_id INT
            );
        """
        await self.execute(sql, execute=True)

    async def exists_operator_in_dict(self, schema_name, operator_id):
        sql = f"""
            SELECT operator_id FROM {schema_name}.{config.TABLE_DICT_OPERATORS} WHERE operator_id = {operator_id};
        """
        if await self.execute(sql, fetchrow=True) is None:
            return False
        else:
            return True

    async def get_list_operators(self, schema_name):
        sql = f"""
            SELECT operator_id FROM {schema_name}.{config.TABLE_DICT_OPERATORS} 
        """
        data = await self.execute(sql, fetch=True)
        return [dict(row) for row in data]

    async def add_service_message(self, schema_name, message_id):
        sql = f"""
            INSERT INTO {schema_name}.{config.TABLE_SERVICE_MESSAGES} (message_id) VALUES ({message_id});
        """
        await self.execute(sql, execute=True)

    async def clear_table(self, schema_name, table_name):
        sql = f"""
            DELETE FROM {schema_name}.{table_name}
        """
        await self.execute(sql, execute=True)

    async def get_messages_for_delete(self, schema_name):
        sql = f"""
            SELECT message_id FROM {schema_name}.{config.TABLE_SERVICE_MESSAGES}
        """
        data = await self.execute(sql, fetch=True)
        return [dict(row) for row in data]
