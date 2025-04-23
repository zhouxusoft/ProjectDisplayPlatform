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
                        `user_id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',\
                        `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户名',\
                        `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码',\
                        `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',\
                        `lastest_login_time` datetime NULL DEFAULT NULL COMMENT '最近登录时间',\
                        `follower_num` int NOT NULL DEFAULT 0 COMMENT '粉丝数量',\
                        `following_num` int NOT NULL DEFAULT 0 COMMENT '关注数量',\
                        `status` int NOT NULL DEFAULT 1 COMMENT '状态（正常1、封禁0、注销2）',\
                        PRIMARY KEY (`user_id`) USING BTREE\
                        ) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;")
    # `access_token` 用于存储用户的登录口令
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `access_token` (\
                        `id` int NOT NULL AUTO_INCREMENT COMMENT 'Token Id',\
                        `user_id` int NOT NULL COMMENT '用户 Id',\
                        `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录令牌',\
                        `set_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '生成时间',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `user_id`(`user_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_access_token_user_id_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;")
    # `projects` 用于存储项目的基本信息，包括项目id、项目名称、项目简介、上传时间等
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `projects` (\
                        `id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',\
                        `user_id` int NULL DEFAULT NULL COMMENT '作者id',\
                        `project_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文章名称',\
                        `project_overview` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '文章简介',\
                        `main_language_id` int NULL DEFAULT NULL COMMENT '主要使用语言',\
                        `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',\
                        `starred_num` int NOT NULL DEFAULT 0 COMMENT '点赞数量',\
                        `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',\
                        `cover` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '封面url',\
                        `page_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文章路由地址',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_projects_user_id_users_user_id`(`user_id` ASC) USING BTREE,\
                        INDEX `fk_projects_main_language_id_languages_id`(`main_language_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_projects_main_language_id_languages_id` FOREIGN KEY (`main_language_id`) REFERENCES `project_display`.`languages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_projects_user_id_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `tags` 用于存储所有的标签，包含标签名以及标签热度
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `tags` (\
                        `id` int NOT NULL COMMENT '自增id',\
                        `tag_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '标签名称',\
                        `tag_hot` int NOT NULL DEFAULT 0 COMMENT '标签热度',\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `languages` 用于存储所有的语言，包含语言的名称、标识颜色以及标签热度
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `languages` (\
                        `id` int NOT NULL COMMENT '自增id',\
                        `language_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '语言名称',\
                        `language_color` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '图标颜色',\
                        `language_hot` int NOT NULL DEFAULT 0 COMMENT '热度',\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `project_tag` 用于储存项目所包含的对应标签名
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_tag` (\
                        `id` int NOT NULL COMMENT '自增id',\
                        `project_id` int NULL DEFAULT NULL COMMENT '项目id',\
                        `tag_id` int NULL DEFAULT NULL COMMENT '标签id',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_project_tag_project_id_projects_id`(`project_id` ASC) USING BTREE,\
                        INDEX `fk_project_tag_tag_id_tags_id`(`tag_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_project_tag_project_id_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_project_tag_tag_id_tags_id` FOREIGN KEY (`tag_id`) REFERENCES `project_display`.`tags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;") 
    # `project_language` 用于存储项目所包含的对应语言
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_language` (\
                        `id` int NOT NULL COMMENT '自增id',\
                        `project_id` int NULL DEFAULT NULL COMMENT '项目id',\
                        `language_id` int NULL DEFAULT NULL COMMENT '语言id',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_project_language_project_id_projects_id`(`project_id` ASC) USING BTREE,\
                        INDEX `fk_project_language_language_id_projects_id`(`language_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_project_language_language_id_projects_id` FOREIGN KEY (`language_id`) REFERENCES `project_display`.`languages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_project_language_project_id_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `project_url` 用于存储项目上线和开源仓库的地址
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_url` (\
                        `id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',\
                        `project_id` int NULL DEFAULT NULL COMMENT '项目id',\
                        `upline_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '线上地址',\
                        `github_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'github地址',\
                        `gitee_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'gitee地址',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_project_url_project_id_projects_id`(`project_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_project_url_project_id_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")\
    # `readme` readme 是项目的详细介绍
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_readme` (\
                        `id` int NOT NULL COMMENT '自增id',\
                        `project_id` int NULL DEFAULT NULL COMMENT '项目id',\
                        `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '正文',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_project_readme_project_id_projects_id`(`project_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_project_readme_project_id_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;") 
    # `project_picture` 用于存放项目的介绍图片
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `project_picture` (\
                        `id` int NOT NULL COMMENT '自增id',\
                        `project_id` int NULL DEFAULT NULL COMMENT '项目id',\
                        `picture_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '图片路径',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_project_picture_project_url_projects_id`(`project_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_project_picture_project_url_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `user_starred` 用于存储用户和项目间的 starred 关系
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `user_starred` (\
                        `id` int NOT NULL COMMENT '自增id',\
                        `user_id` int NULL DEFAULT NULL COMMENT '用户id',\
                        `project_id` int NULL DEFAULT NULL COMMENT '项目id',\
                        `starred_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '点赞时间',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `user_id`(`user_id` ASC) USING BTREE,\
                        INDEX `fk_user_starred_project_id_projects_id`(`project_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_user_starred_project_id_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_user_starred_user_id_users_userid` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `user_followed` 用于存储用户间的 follow 关系
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `user_follow` (\
                       `id` int NOT NULL COMMENT '自增id',\
                        `user_id` int NULL DEFAULT NULL COMMENT '关注人id',\
                        `follow_id` int NULL DEFAULT NULL COMMENT '被关注人id',\
                        `follow_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '关注时间',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_user_follow_follow_id_users_user_id`(`follow_id` ASC) USING BTREE,\
                        INDEX `fk_user_follow_user_id_users_user_id`(`user_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_user_follow_follow_id_users_user_id` FOREIGN KEY (`follow_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_user_follow_user_id_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `user_info` 用于存储用户的个人信息
    dbcursor.execute("CREATE TABLE IF NOT EXISTS `user_info` (\
                        `id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',\
                        `user_id` int NULL DEFAULT NULL COMMENT '用户id',\
                        `user_icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户头像',\
                        `nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '昵称',\
                        `bio` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '个性签名',\
                        `position` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'ip所在地',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_user_info_user_id_users_user_id`(`user_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_user_info_user_id_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
    # `kinds` 用于存储平台侧边的分类
    dbcursor.execute("""CREATE TABLE IF NOT EXISTS `kinds` (
                        `id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',\
                        `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '类型名称',\
                        `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '类型图标',\
                        PRIMARY KEY (`id`) USING BTREE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;""")
    # `user_browse` 用于存储用户浏览项目的记录
    dbcursor.execute("""CREATE TABLE IF NOT EXISTS `user_browse` (
                        `id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',\
                        `user_id` int NOT NULL COMMENT '用户id',\
                        `project_id` int NOT NULL COMMENT '项目id',\
                        `browse_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '浏览时间',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_user_browse_user_id_users_user_id`(`user_id` ASC) USING BTREE,\
                        INDEX `fk_user_browse_project_id_projects_id`(`project_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_user_browse_project_id_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_user_browse_user_id_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;""")
    # `user_comment` 用于存储用户对项目的评论
    dbcursor.execute("""CREATE TABLE IF NOT EXISTS `user_comment` (
                        `id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',\
                        `user_id` int NOT NULL COMMENT '用户id',\
                        `project_id` int NOT NULL COMMENT '项目id',\
                        `comment_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论内容',\
                        `comment_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '评论时间',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_user_comment_user_id_users_user_id`(`user_id` ASC) USING BTREE,\
                        INDEX `fk_user_comment_project_id_projects_id`(`project_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_user_comment_project_id_projects_id` FOREIGN KEY (`project_id`) REFERENCES `project_display`.`projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_user_comment_user_id_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;""")
    # `user_message` 用于存储用户之间的私信
    dbcursor.execute("""CREATE TABLE IF NOT EXISTS `user_message` (
                        `id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',\
                        `sender_id` int NOT NULL COMMENT '发送人id',\
                        `receiver_id` int NOT NULL COMMENT '接收人id',\
                        `message_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '消息类型',\
                        `message_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '消息内容',\
                        `send_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '发送时间',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_user_message_sender_id_users_user_id`(`sender_id` ASC) USING BTREE,\
                        INDEX `fk_user_message_receiver_id_users_user_id`(`receiver_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_user_message_receiver_id_users_user_id` FOREIGN KEY (`receiver_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                        CONSTRAINT `fk_user_message_sender_id_users_user_id` FOREIGN KEY (`sender_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;""")
    # `system_notification` 用于存储系统通知
    dbcursor.execute("""CREATE TABLE IF NOT EXISTS `system_notification` (
                       `id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',\
                        `user_id` int NOT NULL COMMENT '用户id',\
                        `notification_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '通知类型',\
                        `notification_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '通知内容',\
                        `notification_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '通知时间',\
                        `is_read` tinyint(1) NOT NULL DEFAULT 0 COMMENT '用户是否已读',\
                        PRIMARY KEY (`id`) USING BTREE,\
                        INDEX `fk_system_notification_user_id_users_user_id`(`user_id` ASC) USING BTREE,\
                        CONSTRAINT `fk_system_notification_user_id_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `project_display`.`users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE\
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;""")

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

    # 触发器，创建 user 的同时，创建改 user 的 user_info
    dbcursor.execute("""CREATE TRIGGER IF NOT EXISTS create_user_info 
                        AFTER INSERT ON `users`
                        FOR EACH ROW 
                        BEGIN 
                            INSERT INTO `user_info` (`user_id`, `nickname`) VALUES (NEW.user_id, NEW.username);
                        END;""")

    db.close()