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
    # `tags` 用于存储所有的标签，包含标签名以及标签热度
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `tags` (\
                        `id` int NOT NULL,\
                        `tag_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `tag_hot` int NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `languages` 用于存储所有的语言，包含语言的名称、标识颜色以及标签热度
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `languages` (\
                        `id` int NOT NULL,\
                        `language_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `language_color` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `language_hot` int NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `project_tag` 用于储存项目所包含的对应标签名
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_tag` (\
                        `id` int NOT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `tag_id` int NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;") 
    # `project_language` 用于存储项目所包含的对应语言
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_language` (\
                        `id` int NOT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `language_id` int NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `project_url` 用于存储项目上线和开源仓库的地址
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_url` (\
                        `id` int NOT NULL AUTO_INCREMENT,\
                        `project_id` int NULL DEFAULT NULL,\
                        `upline_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `github_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `gitee_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `readme` readme 是项目的详细介绍
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `readme` (\
                        `id` int NOT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;") 
    # `project_picture` 用于存放项目的介绍图片
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_picture` (\
                        `id` int NOT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `picture_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `user_starred` 用于存储用户和项目间的 starred 关系
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `user_starred` (\
                        `id` int NOT NULL,\
                        `user_id` int NULL DEFAULT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `starred_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `user_starred` 用于存储用户间的 follow 关系
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `user_follow` (\
                        `id` int NOT NULL,\
                        `user_id` int NULL DEFAULT NULL,\
                        `follow_id` int NULL DEFAULT NULL,\
                        `follow_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")

    db.close()