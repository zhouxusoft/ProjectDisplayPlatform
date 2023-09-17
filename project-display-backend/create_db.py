from dotenv import load_dotenv
import pymysql
import os

load_dotenv()
# 从配置文件中读取数据
MYSQL_DATABASE_HOST = os.getenv("MYSQL_DATABASE_HOST")
MYSQL_DATABASE_USER = os.getenv("MYSQL_DATABASE_USER")
MYSQL_DATABASE_PASSWORD = os.getenv("MYSQL_DATABASE_PASSWORD")
if not MYSQL_DATABASE_PASSWORD:
    exit()


def create_database():
    # 创建数据库连接
    db = pymysql.connect(
        host=MYSQL_DATABASE_HOST,
        user=MYSQL_DATABASE_USER,
        password=MYSQL_DATABASE_PASSWORD, # type: ignore
        charset="utf8mb4"
    )
    dbcursor = db.cursor()
    # 创建数据库
    dbcursor.execute("CREATE DATABASE IF NOT EXISTS `project_display`")
    # 选择数据库
    dbcursor.execute("use project_display")
    # 创建数据表

    # `user_table` 用于存储用户信息，包括用户id、用户名、状态等
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `user_table` (\
                        `user_id` int NOT NULL AUTO_INCREMENT,\
                        `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,\
                        `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,\
                        `nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,\
                        `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                        `lastest_login_time` datetime NULL DEFAULT NULL,\
                        `status` int NOT NULL DEFAULT 1 COMMENT '（正常1、封禁0、注销2）',\
                        PRIMARY KEY (`user_id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `access_token` 用于存储用户的登录口令
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `access_token` (\
                        `id` int NOT NULL AUTO_INCREMENT,\
                        `user_id` int NOT NULL,\
                        `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,\
                        `set_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `projects` 用于存储项目的基本信息，包括项目id、项目名称、项目简介、上传时间等
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `projects` (\
                        `id` int NOT NULL AUTO_INCREMENT,\
                        `project_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `project_overview` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,\
                        `main_language_id` int NULL DEFAULT NULL,\
                        `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                        `starred_num` int NULL DEFAULT NULL,\
                        `update_time` datetime NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")

    dbcursor.execute("CREATE TABLE IF NOT EXISTS `tags` (\
                        `id` int NOT NULL,\
                        `tag_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `tag_hot` int NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `languages` (\
                        `id` int NOT NULL,\
                        `language_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `language_color` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `language_hot` int NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_tag` (\
                        `id` int NOT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `tag_id` int NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;") 
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_language` (\
                        `id` int NOT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `language_id` int NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `readme` (\
                        `id` int NOT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;") 


    db.close()