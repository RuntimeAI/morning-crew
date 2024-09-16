import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import sqlite3
import urllib3
from skillset import Skillset
from pydantic import BaseModel, PrivateAttr
from typing import Optional, Dict, Any
from config.settings import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB

# 忽略 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class KnowledgeBase(Skillset, BaseModel):
    _db_connection: Optional[sqlite3.Connection] = PrivateAttr(default=None)
    _db_cursor: Optional[sqlite3.Cursor] = PrivateAttr(default=None)
    _db_path: str = PrivateAttr(default="knowledge_base.db")

    def __init__(self, name: str = "Knowledge Base", description: str = "Store and retrieve knowledge", db_path: str = "knowledge_base.db"):
        super().__init__(name=name, description=description)
        self._db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        # 创建数据库连接
        self._db_connection = sqlite3.connect(self._db_path)
        self._db_cursor = self._db_connection.cursor()
        
        # 创建表格如果不存在
        self._db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
        """)
        self._db_connection.commit()

    def save(self, input: str) -> None:
        if input.startswith("http"):
            response = requests.get(input, verify=False)  # 忽略 SSL 验证
            content = response.text
        else:
            content = input

        self._db_cursor.execute("INSERT INTO knowledge_base (content) VALUES (?)", (content,))
        self._db_connection.commit()
        print(f"Saved content: {content[:100]}...")  # 添加调试信息

    def retrieve(self, query: str) -> Dict[str, Any]:
        self._db_cursor.execute("SELECT content FROM knowledge_base WHERE content LIKE ?", ('%' + query + '%',))
        results = self._db_cursor.fetchall()
        print(f"Retrieved {len(results)} results for query: {query}")  # 添加调试信息
        return {"results": [row[0] for row in results]}

    def __del__(self):
        if self._db_connection:
            self._db_connection.close()

# Example usage
if __name__ == "__main__":
    kb = KnowledgeBase()
    # kb.save("https://insights.glassnode.com/the-week-onchain-week-37-2024/")
    kb.save("This is a long text content to be saved in the knowledge base.")
    result = kb.retrieve("content about bitcoin")
    print(result)