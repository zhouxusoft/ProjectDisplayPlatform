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

    # `user` 用于存储用户信息，包括用户id、用户名、状态等
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `users` (\
                        `user_id` int NOT NULL AUTO_INCREMENT,\
                        `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,\
                        `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,\
                        `nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,\
                        `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                        `lastest_login_time` datetime NULL DEFAULT NULL,\
                        `follower_num` int NOT NULL DEFAULT 0,\
                        `following_num` int NOT NULL DEFAULT 0,\
                        `status` int NOT NULL DEFAULT 1 COMMENT '（正常1、封禁0、注销2）',\
                        PRIMARY KEY (`user_id`) USING BTREE\
                        ) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;")
    # `access_token` 用于存储用户的登录口令
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `access_token` (\
                        `id` int NOT NULL AUTO_INCREMENT,\
                        `user_id` int NOT NULL,\
                        `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,\
                        `set_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `user_id`(`user_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_access_token_user_id_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;")
    # `projects` 用于存储项目的基本信息，包括项目id、项目名称、项目简介、上传时间等
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `projects` (\
                        `id` int NOT NULL AUTO_INCREMENT,\
                        `user_id` int NULL DEFAULT NULL,\
                        `project_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `project_overview` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,\
                        `main_language_id` int NULL DEFAULT NULL,\
                        `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                        `starred_num` int NULL DEFAULT NULL,\
                        `update_time` datetime NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_projects_user_id_users_user_id`(`user_id` ASC) USING BTREE,\
                        INDEX `fk_projects_main_language_id_languages_id`(`main_language_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_projects_user_id_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_projects_main_language_id_languages_id` FOREIGN KEY (`main_language_id`) REFERENCES `project_display`.`languages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `tags` 用于存储所有的标签，包含标签名以及标签热度
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `tags` (\
                        `id` int NOT NULL,\
                        `tag_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `tag_hot` int NOT NULL DEFAULT 0,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `languages` 用于存储所有的语言，包含语言的名称、标识颜色以及标签热度
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `languages` (\
                        `id` int NOT NULL,\
                        `language_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `language_color` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `language_hot` int NOT NULL DEFAULT 0,\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `project_tag` 用于储存项目所包含的对应标签名
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_tag` (\
                        `id` int NOT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `tag_id` int NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_project_tag_project_id_projects_id`(`project_id` ASC) USING BTREE,\
                        INDEX `fk_project_tag_tag_id_tags_id`(`tag_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_project_tag_project_id_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_project_tag_tag_id_tags_id` FOREIGN KEY (`tag_id`) REFERENCES `project_display`.`tags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;") 
    # `project_language` 用于存储项目所包含的对应语言
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_language` (\
                        `id` int NOT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `language_id` int NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_project_language_project_id_projects_id`(`project_id` ASC) USING BTREE,\
                        INDEX `fk_project_language_language_id_projects_id`(`language_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_project_language_project_id_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_project_language_language_id_projects_id` FOREIGN KEY (`language_id`) REFERENCES `project_display`.`languages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `project_url` 用于存储项目上线和开源仓库的地址
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_url` (\
                        `id` int NOT NULL AUTO_INCREMENT,\
                        `project_id` int NULL DEFAULT NULL,\
                        `upline_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `github_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        `gitee_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_project_url_project_id_projects_id`(`project_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_project_url_project_id_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `readme` readme 是项目的详细介绍
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_readme` (\
                        `id` int NOT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_project_readme_project_id_projects_id`(`project_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_project_readme_project_id_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;") 
    # `project_picture` 用于存放项目的介绍图片
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_picture` (\
                        `id` int NOT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `picture_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_project_picture_project_url_projects_id`(`project_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_project_picture_project_url_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `user_starred` 用于存储用户和项目间的 starred 关系
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `user_starred` (\
                        `id` int NOT NULL,\
                        `user_id` int NULL DEFAULT NULL,\
                        `project_id` int NULL DEFAULT NULL,\
                        `starred_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `user_id`(`user_id` ASC) USING BTREE,\
                        INDEX `fk_user_starred_project_id_projects_id`(`project_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_user_starred_project_id_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_user_starred_user_id_users_userid` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `user_followed` 用于存储用户间的 follow 关系
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `user_follow` (\
                        `id` int NOT NULL,\
                        `user_id` int NULL DEFAULT NULL,\
                        `follow_id` int NULL DEFAULT NULL,\
                        `follow_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_user_follow_follow_id_users_user_id`(`follow_id` ASC) USING BTREE,\
                        INDEX `fk_user_follow_user_id_users_user_id`(`user_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_user_follow_follow_id_users_user_id` FOREIGN KEY (`follow_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_user_follow_user_id_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `user_info` 用于存储用户的个人信息
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `user_info` (\
                        `id` int NOT NULL AUTO_INCREMENT,\
                        `user_id` int NULL DEFAULT NULL,\
                        `bio` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_user_info_user_id_users_user_id`(`user_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_user_info_user_id_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")

    # 触发器，使 project 的 starred_num 与 user_starred 的数据保持一致
    dbcursor.execute("""CREATE TRIGGER IF NOT EXISTS update_starred_num
                        AFTER INSERT ON user_starred
                        FOR EACH ROW
                        BEGIN
                            DECLARE project_count INT;
                            SELECT COUNT(*) INTO project_count
                            FROM user_starred
                            WHERE project_id = NEW.project_id;
                            UPDATE projects
                            SET starred_num = project_count
                            WHERE id = NEW.project_id;
                        END;""")

    # 触发器，使 tags 的 hot 值，与 project_tag 中包含该 tag_id 的数据量保持一致
    dbcursor.execute("""CREATE TRIGGER IF NOT EXISTS update_tag_hot
                        AFTER INSERT ON project_tag
                        FOR EACH ROW
                        BEGIN
                            UPDATE tags
                            SET tag_hot = tag_hot + 1
                            WHERE id = NEW.tag_id;
                        END;""")

    # 触发器，使 tags 的 hot 值，与 project_tag 中包含该 tag_id 的数据量保持一致
    dbcursor.execute("""CREATE TRIGGER IF NOT EXISTS update_tag_hot_after_delete
                        AFTER DELETE ON project_tag
                        FOR EACH ROW
                        BEGIN
                            UPDATE tags
                            SET tag_hot = tag_hot - 1
                            WHERE id = OLD.tag_id;
                        END;""")

    # 触发器，使 languages 的 hot 值，与 project_language 中包含该 language_id 的数据量保持一致
    dbcursor.execute("""CREATE TRIGGER IF NOT EXISTS update_language_hot
                    AFTER INSERT ON project_language
                    FOR EACH ROW
                    BEGIN
                        UPDATE languages
                        SET language_hot = language_hot + 1
                        WHERE id = NEW.language_id;
                    END;""")

    # 触发器，使 languages 的 hot 值，与 project_language 中包含该 language_id 的数据量保持一致
    dbcursor.execute("""CREATE TRIGGER IF NOT EXISTS update_language_hot_after_delete
                        AFTER DELETE ON project_language
                        FOR EACH ROW
                        BEGIN
                            UPDATE languages
                            SET language_hot = language_hot - 1
                            WHERE id = OLD.language_id;
                        END;""")

    # 触发器，使 users 的 following_num 和 follower_num 的数据，与 user_follow 中包含该 user_id 的数据量保持一致
    dbcursor.execute("""CREATE TRIGGER IF NOT EXISTS update_follow_num
                        AFTER INSERT ON user_follow
                        FOR EACH ROW
                        BEGIN
                            UPDATE users
                            SET following_num = following_num + 1
                            WHERE user_id = NEW.user_id;
                            UPDATE users
                            SET follower_num = follower_num + 1
                            WHERE user_id = NEW.follow_id;
                        END;""")
    
    # 触发器，使 users 的 following_num 和 follower_num 的数据，与 user_follow 中包含该 user_id 的数据量保持一致
    dbcursor.execute("""CREATE TRIGGER IF NOT EXISTS update_follow_num_after_delete
                        AFTER DELETE ON user_follow
                        FOR EACH ROW
                        BEGIN
                            UPDATE users
                            SET following_num = following_num - 1
                            WHERE user_id = OLD.user_id;
                            UPDATE users
                            SET follower_num = follower_num - 1
                            WHERE user_id = OLD.follow_id;
                        END;""")

    db.close()