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
            CREATE SCHEMA IF NOT EXISTS {schema_name}"""
        await self.execute(sql, execute=True)

    async def create_table_dict_problems(self, schema_name, table_name):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                id INT,
                problem VARCHAR(255) NOT NULL
            );
        """
        await self.execute(sql, execute=True)

    async def create_table_struct(self, schema_name, table_name):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                id SERIAL PRIMARY KEY,
                hub INT,
                city VARCHAR(255),
                number_problem INT,
                user_id BIGINT NOT NULL,
                full_name VARCHAR(255) NOT NULL,
                user_name VARCHAR(255) NULL,
                message_text VARCHAR(255),
                date_time TIMESTAMP
            );
        """
        await self.execute(sql, execute=True)

    async def create_table_unstruct(self, schema_name, table_name):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                full_name VARCHAR(255) NOT NULL,
                user_name VARCHAR(255) NULL,
                message_text VARCHAR(255),
                date_time TIMESTAMP
            );
        """
        await self.execute(sql, execute=True)
