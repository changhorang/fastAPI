CREATE TABLE `tbl_api_token` (
  `username` varchar(30) NOT NULL,
  `expired_date` date DEFAULT NULL,
  `refresh_token` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='api user table';

INSERT INTO tbl_api_token (USERNAME)
SELECT USER_ID FROM COM_USER;