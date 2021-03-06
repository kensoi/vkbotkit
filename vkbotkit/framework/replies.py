"""
Copyright 2022 kensoi
"""

import asyncio
import time

class Replies:
    """
    Система ожидания ответа в переписке
    """

    def __init__(self) -> None:
        self.__wait_list = {}


    def __repr__(self) -> str:
        return "<vkbotkit.framework.replies.Replies>"


    def check(self, pkg):
        """
        Специальная функция для получения новых оповещений с беседы.
        """

        for _, task_obj in self.__wait_list.items():
            if task_obj.check(pkg):
                return True


    async def get(self, pkg):
        """
        Специальная функция для получения новых оповещений с беседы.
        """

        task_obj = ReplyTask(pkg)
        task_id = f"${time.time()}_{pkg.peer_id}_{pkg.from_id}"
        self.__wait_list[task_id] = task_obj

        while not task_obj.ready:
            await asyncio.sleep(1)

        self.__wait_list.pop(task_id, None)
        return task_obj.package


class ReplyTask:
    """
    Объект задачи для ожидания ответа
    """

    def __init__(self, pkg):
        self.__chat = pkg.peer_id
        self.__from = pkg.from_id
        self.ready = False
        self.package = None


    def __repr__(self) -> str:
        return "<vkbotkit.framework.replies.ReplyTask>"


    def check(self, pkg):
        """
        Проверка на ожидаемость данного уведомления.
        """


        if self.__chat == pkg.peer_id and self.__from == pkg.from_id:
            self.ready = True
            self.package = pkg
            return True
