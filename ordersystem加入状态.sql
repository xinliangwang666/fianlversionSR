/*
 Navicat MySQL Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80027 (8.0.27)
 Source Host           : localhost:3306
 Source Schema         : ordersystem

 Target Server Type    : MySQL
 Target Server Version : 80027 (8.0.27)
 File Encoding         : 65001

 Date: 09/06/2025 22:58:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 65 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add user', 7, 'add_user');
INSERT INTO `auth_permission` VALUES (26, 'Can change user', 7, 'change_user');
INSERT INTO `auth_permission` VALUES (27, 'Can delete user', 7, 'delete_user');
INSERT INTO `auth_permission` VALUES (28, 'Can view user', 7, 'view_user');
INSERT INTO `auth_permission` VALUES (29, 'Can add admin', 8, 'add_admin');
INSERT INTO `auth_permission` VALUES (30, 'Can change admin', 8, 'change_admin');
INSERT INTO `auth_permission` VALUES (31, 'Can delete admin', 8, 'delete_admin');
INSERT INTO `auth_permission` VALUES (32, 'Can view admin', 8, 'view_admin');
INSERT INTO `auth_permission` VALUES (33, 'Can add notice', 9, 'add_notice');
INSERT INTO `auth_permission` VALUES (34, 'Can change notice', 9, 'change_notice');
INSERT INTO `auth_permission` VALUES (35, 'Can delete notice', 9, 'delete_notice');
INSERT INTO `auth_permission` VALUES (36, 'Can view notice', 9, 'view_notice');
INSERT INTO `auth_permission` VALUES (37, 'Can add dish flavor', 10, 'add_dishflavor');
INSERT INTO `auth_permission` VALUES (38, 'Can change dish flavor', 10, 'change_dishflavor');
INSERT INTO `auth_permission` VALUES (39, 'Can delete dish flavor', 10, 'delete_dishflavor');
INSERT INTO `auth_permission` VALUES (40, 'Can view dish flavor', 10, 'view_dishflavor');
INSERT INTO `auth_permission` VALUES (41, 'Can add dish type', 11, 'add_dishtype');
INSERT INTO `auth_permission` VALUES (42, 'Can change dish type', 11, 'change_dishtype');
INSERT INTO `auth_permission` VALUES (43, 'Can delete dish type', 11, 'delete_dishtype');
INSERT INTO `auth_permission` VALUES (44, 'Can view dish type', 11, 'view_dishtype');
INSERT INTO `auth_permission` VALUES (45, 'Can add dish', 12, 'add_dish');
INSERT INTO `auth_permission` VALUES (46, 'Can change dish', 12, 'change_dish');
INSERT INTO `auth_permission` VALUES (47, 'Can delete dish', 12, 'delete_dish');
INSERT INTO `auth_permission` VALUES (48, 'Can view dish', 12, 'view_dish');
INSERT INTO `auth_permission` VALUES (49, 'Can add order', 13, 'add_order');
INSERT INTO `auth_permission` VALUES (50, 'Can change order', 13, 'change_order');
INSERT INTO `auth_permission` VALUES (51, 'Can delete order', 13, 'delete_order');
INSERT INTO `auth_permission` VALUES (52, 'Can view order', 13, 'view_order');
INSERT INTO `auth_permission` VALUES (53, 'Can add order info', 14, 'add_orderinfo');
INSERT INTO `auth_permission` VALUES (54, 'Can change order info', 14, 'change_orderinfo');
INSERT INTO `auth_permission` VALUES (55, 'Can delete order info', 14, 'delete_orderinfo');
INSERT INTO `auth_permission` VALUES (56, 'Can view order info', 14, 'view_orderinfo');
INSERT INTO `auth_permission` VALUES (57, 'Can add user', 15, 'add_user');
INSERT INTO `auth_permission` VALUES (58, 'Can change user', 15, 'change_user');
INSERT INTO `auth_permission` VALUES (59, 'Can delete user', 15, 'delete_user');
INSERT INTO `auth_permission` VALUES (60, 'Can view user', 15, 'view_user');
INSERT INTO `auth_permission` VALUES (61, 'Can add img save', 16, 'add_imgsave');
INSERT INTO `auth_permission` VALUES (62, 'Can change img save', 16, 'change_imgsave');
INSERT INTO `auth_permission` VALUES (63, 'Can delete img save', 16, 'delete_imgsave');
INSERT INTO `auth_permission` VALUES (64, 'Can view img save', 16, 'view_imgsave');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$600000$lV76sILrm3SyGMz9o5Sv4d$CBCfS/AmaFh0lURG+QsLNjz3EZacNOlLz2eziTrI/Dk=', NULL, 1, 'root', '', '', '183201@qq.com', 1, 1, '2025-06-02 23:03:25.220232');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for backstageapi_admin
-- ----------------------------
DROP TABLE IF EXISTS `backstageapi_admin`;
CREATE TABLE `backstageapi_admin`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `role` smallint NOT NULL,
  `phone` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of backstageapi_admin
-- ----------------------------
INSERT INTO `backstageapi_admin` VALUES (1, 'admin', 'admin', 1, '19985211122');
INSERT INTO `backstageapi_admin` VALUES (2, 'shangjia', '123123', 2, '18875488888');

-- ----------------------------
-- Table structure for backstageapi_dish
-- ----------------------------
DROP TABLE IF EXISTS `backstageapi_dish`;
CREATE TABLE `backstageapi_dish`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `dish_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `dish_price` decimal(6, 2) NOT NULL,
  `dish_desc` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `dish_img` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `order_count` int NOT NULL,
  `dish_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `BackstageApi_dish_dish_type_id_0ab66a0b_fk_Backstage`(`dish_type_id` ASC) USING BTREE,
  CONSTRAINT `BackstageApi_dish_dish_type_id_0ab66a0b_fk_Backstage` FOREIGN KEY (`dish_type_id`) REFERENCES `backstageapi_dishtype` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of backstageapi_dish
-- ----------------------------
INSERT INTO `backstageapi_dish` VALUES (4, '鱼香肉丝', 24.00, '四川的菜', 'http://127.0.0.1:8000/media/dishes/328bddda5c2950b5a1297318a5d5e41a_jpiWMq3.jpg', 12, 2);
INSERT INTO `backstageapi_dish` VALUES (5, '重庆小面', 20.00, '属于重庆菜，是重庆特色美食之一', 'http://127.0.0.1:8000/media/dishes/小面.jpg', 3, 4);
INSERT INTO `backstageapi_dish` VALUES (6, '红烧鱼', 26.00, '有一定温度的菜品，如刚做好上桌时热热的可直接食用的菜', 'http://127.0.0.1:8000/media/dishes/红烧鱼.jpg', 2, 5);
INSERT INTO `backstageapi_dish` VALUES (7, '凉拌菜', 17.00, '将初步加工和焯水处理后的原料，经过添加红油、酱油、蒜粒等配料制作而成的菜肴', 'http://127.0.0.1:8000/media/dishes/凉拌菜.jpg', 1, 6);
INSERT INTO `backstageapi_dish` VALUES (8, '广东烧鹅', 48.00, '广东的招牌菜', 'http://127.0.0.1:8000/media/dishes/烧鹅.jpg', 0, 7);

-- ----------------------------
-- Table structure for backstageapi_dishflavor
-- ----------------------------
DROP TABLE IF EXISTS `backstageapi_dishflavor`;
CREATE TABLE `backstageapi_dishflavor`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `desc` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of backstageapi_dishflavor
-- ----------------------------
INSERT INTO `backstageapi_dishflavor` VALUES (1, '正常', '默认口味');
INSERT INTO `backstageapi_dishflavor` VALUES (3, '麻辣', '朝天椒炒制而成');
INSERT INTO `backstageapi_dishflavor` VALUES (5, '清淡', '没什么味道，健康');

-- ----------------------------
-- Table structure for backstageapi_dishtype
-- ----------------------------
DROP TABLE IF EXISTS `backstageapi_dishtype`;
CREATE TABLE `backstageapi_dishtype`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `desc` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of backstageapi_dishtype
-- ----------------------------
INSERT INTO `backstageapi_dishtype` VALUES (2, '川菜', '四川的菜');
INSERT INTO `backstageapi_dishtype` VALUES (4, '面食', '主要是面粉做的');
INSERT INTO `backstageapi_dishtype` VALUES (5, '热菜', '热腾腾的菜');
INSERT INTO `backstageapi_dishtype` VALUES (6, '凉菜', '凉凉的菜');
INSERT INTO `backstageapi_dishtype` VALUES (7, '粤菜', '广东口味菜');

-- ----------------------------
-- Table structure for backstageapi_notice
-- ----------------------------
DROP TABLE IF EXISTS `backstageapi_notice`;
CREATE TABLE `backstageapi_notice`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `pub_date` datetime(6) NOT NULL,
  `imgURL` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of backstageapi_notice
-- ----------------------------
INSERT INTO `backstageapi_notice` VALUES (1, '特级牛排', ' 开启你的美食之旅', '2025-06-04 23:23:54.993282', 'http://127.0.0.1:8000/media/notices/牛排.jpg');
INSERT INTO `backstageapi_notice` VALUES (2, '重庆小面', '欢迎品尝重庆小面很好吃', '2025-06-05 00:04:06.878547', 'http://127.0.0.1:8000/media/notices/小面.jpg');

-- ----------------------------
-- Table structure for backstageapi_order
-- ----------------------------
DROP TABLE IF EXISTS `backstageapi_order`;
CREATE TABLE `backstageapi_order`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `total` int NOT NULL,
  `status` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'paid',
  `flavor_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `BackstageApi_order_flavor_id_3b4db686_fk_Backstage`(`flavor_id` ASC) USING BTREE,
  INDEX `BackstageApi_order_user_id_52df3570_fk_ForegroundApi_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `BackstageApi_order_flavor_id_3b4db686_fk_Backstage` FOREIGN KEY (`flavor_id`) REFERENCES `backstageapi_dishflavor` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `BackstageApi_order_user_id_52df3570_fk_ForegroundApi_user_id` FOREIGN KEY (`user_id`) REFERENCES `foregroundapi_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of backstageapi_order
-- ----------------------------
INSERT INTO `backstageapi_order` VALUES (3, '2025-06-03 16:00:57.987909', 24, 'paid', 3, 1);
INSERT INTO `backstageapi_order` VALUES (9, '2025-06-05 00:05:24.895909', 20, 'accepted', 5, 3);
INSERT INTO `backstageapi_order` VALUES (12, '2025-06-09 10:24:05.289962', 24, 'paid', 5, 1);
INSERT INTO `backstageapi_order` VALUES (13, '2025-06-09 10:24:29.720522', 24, 'completed', 5, 1);
INSERT INTO `backstageapi_order` VALUES (30, '2025-06-09 22:32:40.792044', 24, 'paid', 1, 3);

-- ----------------------------
-- Table structure for backstageapi_orderinfo
-- ----------------------------
DROP TABLE IF EXISTS `backstageapi_orderinfo`;
CREATE TABLE `backstageapi_orderinfo`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `count` int NOT NULL,
  `price` int NOT NULL,
  `dish_total_price` double NOT NULL,
  `dish_id` bigint NOT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `BackstageApi_orderinfo_dish_id_02580d94_fk_BackstageApi_dish_id`(`dish_id` ASC) USING BTREE,
  INDEX `BackstageApi_orderin_order_id_e53f9660_fk_Backstage`(`order_id` ASC) USING BTREE,
  CONSTRAINT `BackstageApi_orderin_order_id_e53f9660_fk_Backstage` FOREIGN KEY (`order_id`) REFERENCES `backstageapi_order` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `BackstageApi_orderinfo_dish_id_02580d94_fk_BackstageApi_dish_id` FOREIGN KEY (`dish_id`) REFERENCES `backstageapi_dish` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of backstageapi_orderinfo
-- ----------------------------
INSERT INTO `backstageapi_orderinfo` VALUES (1, 1, 24, 24, 4, 3);
INSERT INTO `backstageapi_orderinfo` VALUES (4, 1, 20, 20, 5, 9);
INSERT INTO `backstageapi_orderinfo` VALUES (8, 1, 24, 24, 4, 12);
INSERT INTO `backstageapi_orderinfo` VALUES (9, 1, 24, 24, 4, 13);
INSERT INTO `backstageapi_orderinfo` VALUES (21, 1, 24, 24, 4, 30);

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (8, 'BackstageApi', 'admin');
INSERT INTO `django_content_type` VALUES (12, 'BackstageApi', 'dish');
INSERT INTO `django_content_type` VALUES (10, 'BackstageApi', 'dishflavor');
INSERT INTO `django_content_type` VALUES (11, 'BackstageApi', 'dishtype');
INSERT INTO `django_content_type` VALUES (9, 'BackstageApi', 'notice');
INSERT INTO `django_content_type` VALUES (13, 'BackstageApi', 'order');
INSERT INTO `django_content_type` VALUES (14, 'BackstageApi', 'orderinfo');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (7, 'ForegroundApi', 'user');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (16, 'Testing', 'imgsave');
INSERT INTO `django_content_type` VALUES (15, 'Testing', 'user');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 57 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'ForegroundApi', '0001_initial', '2025-06-02 22:42:14.388039');
INSERT INTO `django_migrations` VALUES (2, 'ForegroundApi', '0002_dish_alter_user_gender', '2025-06-02 22:42:14.417656');
INSERT INTO `django_migrations` VALUES (3, 'ForegroundApi', '0003_remove_user_integral_remove_user_phone', '2025-06-02 22:42:14.490807');
INSERT INTO `django_migrations` VALUES (4, 'ForegroundApi', '0004_remove_user_gender', '2025-06-02 22:42:14.529308');
INSERT INTO `django_migrations` VALUES (5, 'ForegroundApi', '0005_user_gender_user_integral_user_phone', '2025-06-02 22:42:14.593026');
INSERT INTO `django_migrations` VALUES (6, 'ForegroundApi', '0006_user_email', '2025-06-02 22:42:14.620678');
INSERT INTO `django_migrations` VALUES (7, 'BackstageApi', '0001_initial', '2025-06-02 22:42:14.646703');
INSERT INTO `django_migrations` VALUES (8, 'BackstageApi', '0002_notice', '2025-06-02 22:42:14.669789');
INSERT INTO `django_migrations` VALUES (9, 'BackstageApi', '0003_alter_notice_description_alter_notice_notice_url', '2025-06-02 22:42:14.748869');
INSERT INTO `django_migrations` VALUES (10, 'BackstageApi', '0004_rename_notice_url_notice_img_url_alter_notice_title', '2025-06-02 22:42:14.802442');
INSERT INTO `django_migrations` VALUES (11, 'BackstageApi', '0005_rename_img_url_notice_imgurl', '2025-06-02 22:42:14.815474');
INSERT INTO `django_migrations` VALUES (12, 'BackstageApi', '0006_remove_notice_description_remove_notice_imgurl_and_more', '2025-06-02 22:42:14.920737');
INSERT INTO `django_migrations` VALUES (13, 'BackstageApi', '0007_delete_notice', '2025-06-02 22:42:14.936740');
INSERT INTO `django_migrations` VALUES (14, 'BackstageApi', '0008_notice', '2025-06-02 22:42:14.964762');
INSERT INTO `django_migrations` VALUES (15, 'BackstageApi', '0009_rename_imgurl_notice_notice_url', '2025-06-02 22:42:14.979301');
INSERT INTO `django_migrations` VALUES (16, 'BackstageApi', '0010_rename_notice_url_notice_imgurl', '2025-06-02 22:42:14.991327');
INSERT INTO `django_migrations` VALUES (17, 'BackstageApi', '0011_remove_notice_imgurl', '2025-06-02 22:42:15.033421');
INSERT INTO `django_migrations` VALUES (18, 'BackstageApi', '0012_notice_imgurl', '2025-06-02 22:42:15.050438');
INSERT INTO `django_migrations` VALUES (19, 'BackstageApi', '0013_dishflavor_dishtype_alter_notice_imgurl_dish', '2025-06-02 22:42:15.274787');
INSERT INTO `django_migrations` VALUES (20, 'BackstageApi', '0014_dishflavor_desc_dishtype_desc_alter_dish_dish_flavor_and_more', '2025-06-02 22:42:15.317128');
INSERT INTO `django_migrations` VALUES (21, 'BackstageApi', '0015_alter_dish_dish_flavor_alter_dish_dish_type', '2025-06-02 22:42:15.324120');
INSERT INTO `django_migrations` VALUES (22, 'BackstageApi', '0016_alter_dish_dish_img', '2025-06-02 22:42:15.339664');
INSERT INTO `django_migrations` VALUES (23, 'BackstageApi', '0017_order_orderinfo', '2025-06-02 22:42:15.574105');
INSERT INTO `django_migrations` VALUES (24, 'BackstageApi', '0018_remove_dish_dish_flavor', '2025-06-02 22:42:15.642121');
INSERT INTO `django_migrations` VALUES (25, 'BackstageApi', '0019_rename_dish_id_orderinfo_dish_and_more', '2025-06-02 22:42:15.803026');
INSERT INTO `django_migrations` VALUES (26, 'BackstageApi', '0020_rename_flavor_id_order_flavor_and_more', '2025-06-02 22:42:15.976488');
INSERT INTO `django_migrations` VALUES (27, 'BackstageApi', '0021_admin_phone', '2025-06-02 22:42:15.993501');
INSERT INTO `django_migrations` VALUES (28, 'BackstageApi', '0022_alter_order_total_alter_orderinfo_price', '2025-06-02 22:42:16.102543');
INSERT INTO `django_migrations` VALUES (29, 'ForegroundApi', '0007_delete_dish', '2025-06-02 22:42:16.116563');
INSERT INTO `django_migrations` VALUES (30, 'ForegroundApi', '0008_user_avatar_url', '2025-06-02 22:42:16.145572');
INSERT INTO `django_migrations` VALUES (31, 'ForegroundApi', '0009_alter_user_avatar_url', '2025-06-02 22:42:16.151570');
INSERT INTO `django_migrations` VALUES (32, 'Testing', '0001_initial', '2025-06-02 22:42:16.175885');
INSERT INTO `django_migrations` VALUES (33, 'Testing', '0002_rename_name_user_username_alter_user_integral', '2025-06-02 22:42:16.190894');
INSERT INTO `django_migrations` VALUES (34, 'Testing', '0003_imgsave', '2025-06-02 22:42:16.216942');
INSERT INTO `django_migrations` VALUES (35, 'Testing', '0004_alter_imgsave_imgurl', '2025-06-02 22:42:16.258950');
INSERT INTO `django_migrations` VALUES (36, 'Testing', '0005_alter_imgsave_imgurl', '2025-06-02 22:42:16.270953');
INSERT INTO `django_migrations` VALUES (37, 'Testing', '0006_alter_imgsave_imgurl', '2025-06-02 22:42:16.314011');
INSERT INTO `django_migrations` VALUES (38, 'Testing', '0007_alter_imgsave_imgurl', '2025-06-02 22:42:16.318999');
INSERT INTO `django_migrations` VALUES (39, 'sessions', '0001_initial', '2025-06-02 22:42:16.356605');
INSERT INTO `django_migrations` VALUES (40, 'contenttypes', '0001_initial', '2025-06-02 23:01:35.493808');
INSERT INTO `django_migrations` VALUES (41, 'auth', '0001_initial', '2025-06-02 23:01:36.003776');
INSERT INTO `django_migrations` VALUES (42, 'admin', '0001_initial', '2025-06-02 23:01:36.130428');
INSERT INTO `django_migrations` VALUES (43, 'admin', '0002_logentry_remove_auto_add', '2025-06-02 23:01:36.138429');
INSERT INTO `django_migrations` VALUES (44, 'admin', '0003_logentry_add_action_flag_choices', '2025-06-02 23:01:36.147465');
INSERT INTO `django_migrations` VALUES (45, 'contenttypes', '0002_remove_content_type_name', '2025-06-02 23:01:36.253649');
INSERT INTO `django_migrations` VALUES (46, 'auth', '0002_alter_permission_name_max_length', '2025-06-02 23:01:36.314237');
INSERT INTO `django_migrations` VALUES (47, 'auth', '0003_alter_user_email_max_length', '2025-06-02 23:01:36.375465');
INSERT INTO `django_migrations` VALUES (48, 'auth', '0004_alter_user_username_opts', '2025-06-02 23:01:36.384475');
INSERT INTO `django_migrations` VALUES (49, 'auth', '0005_alter_user_last_login_null', '2025-06-02 23:01:36.529046');
INSERT INTO `django_migrations` VALUES (50, 'auth', '0006_require_contenttypes_0002', '2025-06-02 23:01:36.533048');
INSERT INTO `django_migrations` VALUES (51, 'auth', '0007_alter_validators_add_error_messages', '2025-06-02 23:01:36.542062');
INSERT INTO `django_migrations` VALUES (52, 'auth', '0008_alter_user_username_max_length', '2025-06-02 23:01:36.601746');
INSERT INTO `django_migrations` VALUES (53, 'auth', '0009_alter_user_last_name_max_length', '2025-06-02 23:01:36.661796');
INSERT INTO `django_migrations` VALUES (54, 'auth', '0010_alter_group_name_max_length', '2025-06-02 23:01:36.717909');
INSERT INTO `django_migrations` VALUES (55, 'auth', '0011_update_proxy_permissions', '2025-06-02 23:01:36.729904');
INSERT INTO `django_migrations` VALUES (56, 'auth', '0012_alter_user_first_name_max_length', '2025-06-02 23:01:36.790911');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('20tyqignqoba6v58ujp0jzcr8kzpy0el', '.eJyrVsrMS8tXsqpWykvMTVWyUkpMyc3MU9JRKkgsLi7PL0pBEirKzwGqMKzVUYovTi0uzszPi0-tKMgsqgSqMTIwMtU1MNM1sAwxMrYCITM9IwtjcxNzpVoAYRweKA:1uM70Y:kZIMQgfVzvF-C4_abzw8vdzh7ASsaq4v8UgILL_71b4', '2025-06-09 23:23:26.283747');
INSERT INTO `django_session` VALUES ('7ax3b3k9cbjxbcc96lqx95o4umu09qns', '.eJwNi9sOgjAQRP9ln5FuS0Gz3-E7qaHCGmmbXhQk_LvNzMuZkzmA3dMDHcATkGzAmdUCwVZ-C29coIFgUvr6WDVI1dXWjV22czRvIGzAfEw2cSyxIiw5BxJCqmuLNZJuiChWO7ERJdmYxMPv7SvMcDYwJpsSezfaLXDc612h6i84XKS8q46Upm5oe60Vajj_D04zsA:1uMpym:itqPHW1vI_7wO31yWCISPX7sQyr8AERgwAy61AHK2Rw', '2025-06-11 23:24:36.544204');
INSERT INTO `django_session` VALUES ('7rkb1zkh9lfoyuzx0571l9d9qvyfyozk', '.eJxNyksKgCAUBdC93HHFUzLLdTQXIQMhP_gGFdLea9j0cBpC2jNMQ3LRw8BtMSR0KI75zHX7Uc3HN8TTwbJnDjlZf5VQ7-9IkqqnqRdyJTKkjRqHWepFEZ4XYJUeIA:1uMqeg:gRI2-OtUq7EuUz32FQgqVn5WFkCTCZYad7HyQo-nTIg', '2025-06-12 00:07:54.827950');
INSERT INTO `django_session` VALUES ('8eglesiyu3d881t4nfedelxplb878lfo', '.eJxNykEKgCAQBdC7_HWGCll6jvYhaCCUI86iIrx7Lts-3ouUd4J7kf0Z4eDDmTIGFM98UQ0_qnT0odqAjSNzorzFu6T69KOlnoQ0QplVSSet08tojLWzRfsAYU4eNw:1uORx2:Bc77TU4vtbpWF8WQdcIVm8hi1hKQxqQEmf9vq8I03h0', '2025-06-16 10:09:28.669979');
INSERT INTO `django_session` VALUES ('ayp3y57jbmduoabtbftllqjy1zifgacv', '.eJxNyksKgCAUBdC93LGFn56B62geQgZCfvANKsK917Dp4TyIeS9wD7JPAQ5-SzFDoHrms7TtR60c31BdYOXAHEtew1Vju7-jpaZB2kGpRRtH0k12JDOTJfQXYLYeIw:1uMqO6:Dq-02qM59zli6RKZD9g8XLqhVmR6IOo6dpB-Vg9VHx0', '2025-06-11 23:50:46.537565');
INSERT INTO `django_session` VALUES ('b3gt618zpgze6o863ecbzy5u3c7brbyy', '.eJxNykEKgCAQBdC7_LWGTmngOdqHoIFQKs6iIrp7Lts-3oOUtwL3IPsjwsGHI2UIVM98lhZ-1Mreh34FVo7MqeQ1XjW1ux9SZKSyUttFKUfkjBkszSNNeD9gmB4b:1uOInP:KEltqLoqg0icw-KsBQD9IxitM4EP6GHri_wEJ_sFAXE', '2025-06-16 00:22:55.627324');
INSERT INTO `django_session` VALUES ('b66q824w3x9fmx7sxycdw92wazed5he6', '.eJwNi9sOgyAQRP9ln1EWtLXsd_Td0EiVpgLh0mqN_14y83LmZA6w7umBDrATkGDg9GqAYCu_xW62AIOgU_r6WDUI2dXWzbps5qjfQMhAf3TWcSyxIiw5B-JcyKHFGkE3ROSrmazmJZmY-MPv7SvMcDIYk0nJejeaLdi417tEeWnw2gi8CyQ5UKda0fdKKTj_D3Uzwg:1uMHNL:-ahJ_Iy7cZWhJDL0RCaRiuzEIdojMSoX-NFIfJB_ciU', '2025-06-10 10:27:39.144999');
INSERT INTO `django_session` VALUES ('fc6m05pt99ic5xrp255rnrccukvj1ffk', '.eJxNyk0KgCAQBtC7fOsKR_v1HO1D0GCgNJxFhXT3WrZ9vAKOa4ItiG4PsHB-54gKhxM5U_Y_ymn7Bj0VFgkinOISroPz_R2tdFerviaatbFmsO3YTNSPpPC8YQEeJA:1uMqBY:gEwA3G0nBdXhOksMTjFYR1WiwRx9EttTr5IJMXp6kGI', '2025-06-11 23:37:48.916810');
INSERT INTO `django_session` VALUES ('gm6kmpc942khgfqyvcmo28qyp4fno0co', '.eJwVjNEOwiAUQ_-lz2xcWKbzfofvC2Y4MQ4IMHVZ9u9i2peept3h_D2Ad7gJ3Al4s1gw1myThkA0OX9Cqh2U7qorc77YOZkXmATM2xSTxjXViEcpkaVU-txSleKBiORiJ2fk_zHLW9jaZ5xxCIzZ5uyCH-03urTVuSbdN3RqlL4SMXVM1PbqQpcBxw8PFTIS:1uMqZw:tKYGa6Z0Mfuv2L4daqGwFYy2USUggaDTxWk5Vc6qdyY', '2025-06-12 00:03:00.519098');
INSERT INTO `django_session` VALUES ('ianaztjhdfywxzcb6h6ri8lxj1w85oh5', '.eJxNyjsKgDAQBcC7vDpKdiUWOYe9BIywYD5kC5Xg3bW0HaZD8l7gO3JIER5hS5JhUIPqWdr2o1aOb9BjsGpUlZLXeFVp93fYshvsPBAtPHlH3tqRicgxnhdf8B4H:1uMqOK:2jAxNoWhojmat2Bbf0j8ZPzpfX9A7OkpHlwvAg9wB-0', '2025-06-11 23:51:00.211152');
INSERT INTO `django_session` VALUES ('iptrkwnubh6b71q4ekkimhurw6sxhcuh', '.eJxNyjsKgDAQBcC7vFplN_4w57APASMsaCLZQiV4dy1thymQuCbYguj3AAu_7BJR4fCqZ8rLj3LavsFPBadBVVJ04Tok398xZPqahpppZmM7sjQ2U8_cTnheYEgeGQ:1uMJRX:14qlKzNCa0RxDjajhrmCAgicBPryPDqbF9jg5hQ73p8', '2025-06-10 12:40:07.951139');
INSERT INTO `django_session` VALUES ('n1dxh12phhsiqoxfsdyrm5g8yxgpuca5', '.eJwVjEEOgyAURO8yaxT4ajX_HN0bGqmlqWAA2xrj3Uszq3mTNwecvwfwATeBScCbxYKxJRshsJqUPiGWCZqahnRhzmc7R_MCKwHzNtnEcYul4pHzylJq6mtVonlQSsnFTs7I_2GSt7DXz3XGKTAmm5ILfrTf1cW96KSoq9Sl0vpKDXctU1u3uh8GjfMH6uYx7A:1uMqRc:t1MiXhND7SD4m7gfa0pQGp85mO8scT7EEaMhiGP7AWo', '2025-06-11 23:54:24.417881');
INSERT INTO `django_session` VALUES ('pgfs8a8dor49s0ylkw9it8s1994uh9gc', '.eJwNykEKgCAQRuG7_OsKGzXIc7QPISujNJxFRXT3Bt7q472Iac5wL5I_Ahx49WnZokeF0zNfuUyiLWlJrORdLvoqjByYY05juM9YHplIka1VV6t-IO3IONs1RNoag-8Hss0egQ:1uM720:Z9V0FBiaRf71qMD4vrDllb7-YU-fvVschCCr2rtxi4w', '2025-06-09 23:24:56.223544');
INSERT INTO `django_session` VALUES ('ptcoh3lzkcejo5l048frottonmgjy8zt', '.eJxNyk0KgCAQBtC7fOsMZ-wHPEf7EDQQSsVZVER3z2Xbx3sQ05ZhHyR3BFg4f8SEDsWJnLn6H9W8t0Fvh1WCSMxpDVeJ9W6HNY9KT4poYbJsLHFv5mE0jPcDYC8eEw:1uMo5I:zD1pxURu_Ovu4XcTvFRaeVa2Fw8pJ8zHR1N1W5mlySc', '2025-06-11 21:23:12.374532');
INSERT INTO `django_session` VALUES ('rrn2zmi5nkt9qnr5blqdzn7usni01hcw', 'eyJpbmZvIjp7Im5hbWUiOiJzaGFuZ2ppYSIsInBhc3N3b3JkIjoiMTIzMTIzIiwicm9sZSI6Mn0sIl9zZXNzaW9uX2V4cGlyeSI6IjIwMjUtMDYtMTFUMjM6MjY6MzcuNjU1MTg5In0:1uMq0j:9aCreJNfyMQAtCrJZzIT8keMZAVPLUA0vc_jz6AOVgE', '2025-06-11 23:26:37.655189');
INSERT INTO `django_session` VALUES ('z9cgu0oeimmjiius4pqkli8kgv0skm8f', 'eyJpbmZvIjp7Im5hbWUiOiJzaGFuZ2ppYSIsInBhc3N3b3JkIjoiMTIzMTIzIiwicm9sZSI6Mn0sIl9zZXNzaW9uX2V4cGlyeSI6IjIwMjUtMDYtMTJUMDA6MDc6MzQuODkyNzAxIn0:1uMqeM:VfNz_Mhl0G6gfQGque4EhQHyqBXZlgJ1Q1TDD48-8Cc', '2025-06-12 00:07:34.892701');

-- ----------------------------
-- Table structure for foregroundapi_user
-- ----------------------------
DROP TABLE IF EXISTS `foregroundapi_user`;
CREATE TABLE `foregroundapi_user`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gender` smallint NOT NULL,
  `integral` int NOT NULL,
  `phone` varchar(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `avatar_url` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of foregroundapi_user
-- ----------------------------
INSERT INTO `foregroundapi_user` VALUES (1, 'xuzhixiu', '123123', 1, 100, '18875482222', '123test@qq.com', 'http://127.0.0.1:8000/media/users/boy.jpg');
INSERT INTO `foregroundapi_user` VALUES (2, 'user', '123321', 1, 0, '18875422211', '123test@qq.com', 'http://127.0.0.1:8000/media/users/boy.jpg');
INSERT INTO `foregroundapi_user` VALUES (3, 'user2', '123123', 1, 0, '18874211111', '123test@qq.com', 'http://127.0.0.1:8000/media/users/boy.jpg');

-- ----------------------------
-- Table structure for testing_imgsave
-- ----------------------------
DROP TABLE IF EXISTS `testing_imgsave`;
CREATE TABLE `testing_imgsave`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `imgURL` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of testing_imgsave
-- ----------------------------

-- ----------------------------
-- Table structure for testing_user
-- ----------------------------
DROP TABLE IF EXISTS `testing_user`;
CREATE TABLE `testing_user`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gender` smallint NOT NULL,
  `phone` varchar(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `integral` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of testing_user
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
