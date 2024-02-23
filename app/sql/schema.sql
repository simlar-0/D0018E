CREATE TABLE IF NOT EXISTS `Customer` (
    `id` int  NOT NULL AUTO_INCREMENT,
    `name` nvarchar(255)  NOT NULL ,
    `email` nvarchar(255)  NOT NULL ,
    `address` nvarchar(255)  NOT NULL ,
    `postcode` varchar(10)  NOT NULL ,
    `city` nvarchar(255)  NOT NULL ,
    PRIMARY KEY (
        `id`
    ),
    CONSTRAINT `uc_Customer_email` UNIQUE (
        `email`
    )
);

CREATE TABLE IF NOT EXISTS `Manager` (
    `id` int  NOT NULL AUTO_INCREMENT,
    `is_admin` bool  NOT NULL ,
    `name` nvarchar(255)  NOT NULL ,
    `email` nvarchar(255)  NOT NULL ,
    PRIMARY KEY (
        `id`
    ),
    CONSTRAINT `uc_Manager_email` UNIQUE (
        `email`
    )
);

CREATE TABLE IF NOT EXISTS `CustomerOrder` (
    `id` int  NOT NULL AUTO_INCREMENT,
    `customer_id` int  NOT NULL ,
    `order_date` DATETIME ON UPDATE CURRENT_TIMESTAMP,
    `order_status_id` int  NOT NULL ,
    PRIMARY KEY (
        `id`
    )
);

CREATE TABLE IF NOT EXISTS `OrderLine` (
    `id` int  NOT NULL AUTO_INCREMENT,
    `order_id` int  NOT NULL ,
    `product_id` int  NOT NULL ,
    `quantity` int  NOT NULL ,
    `sub_total_amount` decimal(8,2)  NOT NULL ,
    `unit_price` decimal(8,2)  NOT NULL ,
    PRIMARY KEY (
        `id`
    )
);

CREATE TABLE IF NOT EXISTS `Product` (
    `id` int  NOT NULL AUTO_INCREMENT,
    `name` nvarchar(255)  NOT NULL ,
    `description` nvarchar(255)  NOT NULL ,
    `price` decimal(8,2)  NOT NULL ,
    `image_path` varchar(255)  NOT NULL ,
    `in_stock` int  NOT NULL ,
    PRIMARY KEY (
        `id`
    ),
    CONSTRAINT `uc_Product_name` UNIQUE (
        `name`
    )
);

CREATE TABLE IF NOT EXISTS `OrderStatus` (
    `id` int  NOT NULL,
    `name` nvarchar(255)  NOT NULL ,
    PRIMARY KEY (
        `id`
    ),
    CONSTRAINT `uc_OrderStatus_name` UNIQUE (
        `name`
    )
);

CREATE TABLE IF NOT EXISTS `Review` (
    `customer_id` int  NOT NULL ,
    `product_id` int  NOT NULL ,
    `rating` int  NOT NULL ,
    `review_text` nvarchar(255)  NULL ,
    `review_date` datetime  NOT NULL ,
    `review_header` nvarchar(255)  NULL ,
    PRIMARY KEY (
        `customer_id`,`product_id`
    )
);

CREATE TABLE IF NOT EXISTS `CustomerPassword` (
    `id` int  NOT NULL ,
    `hashed_password` binary(60)  NOT NULL ,
    PRIMARY KEY (
        `id`
    )
);

CREATE TABLE IF NOT EXISTS `ManagerPassword` (
    `id` int  NOT NULL ,
    `hashed_password` binary(60)  NOT NULL ,
    PRIMARY KEY (
        `id`
    )
);

ALTER TABLE `CustomerOrder` ADD CONSTRAINT `fk_CustomerOrder_customer_id` FOREIGN KEY(`customer_id`)
REFERENCES `Customer` (`id`);

ALTER TABLE `CustomerOrder` ADD CONSTRAINT `fk_CustomerOrder_order_status_id` FOREIGN KEY(`order_status_id`)
REFERENCES `OrderStatus` (`id`);

ALTER TABLE `OrderLine` ADD CONSTRAINT `fk_OrderLine_order_id` FOREIGN KEY(`order_id`)
REFERENCES `CustomerOrder` (`id`);

ALTER TABLE `OrderLine` ADD CONSTRAINT `fk_OrderLine_product_id` FOREIGN KEY(`product_id`)
REFERENCES `Product` (`id`);

ALTER TABLE `Review` ADD CONSTRAINT `fk_Review_customer_id` FOREIGN KEY(`customer_id`)
REFERENCES `Customer` (`id`);

ALTER TABLE `Review` ADD CONSTRAINT `fk_Review_product_id` FOREIGN KEY(`product_id`)
REFERENCES `Product` (`id`);

ALTER TABLE `CustomerPassword` ADD CONSTRAINT `fk_CustomerPassword_customer_id` FOREIGN KEY(`id`)
REFERENCES `Customer` (`id`);

ALTER TABLE `ManagerPassword` ADD CONSTRAINT `fk_ManagerPassword_manager_id` FOREIGN KEY(`id`)
REFERENCES `Manager` (`id`);

CREATE INDEX `idx_Customer_name`
ON `Customer` (`name`);

CREATE INDEX `idx_Manager_name`
ON `Manager` (`name`);

CREATE INDEX `idx_CustomerOrder_customer_id`
ON `CustomerOrder` (`id`);

