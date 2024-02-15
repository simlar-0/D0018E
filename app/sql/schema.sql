CREATE TABLE IF NOT EXISTS `Customer` (
    `customer_id` int  NOT NULL ,
    `name` nvarchar(255)  NOT NULL ,
    `email` nvarchar(255)  NOT NULL ,
    `address` nvarchar(255)  NOT NULL ,
    `postcode` varchar(10)  NOT NULL ,
    `city` nvarchar(255)  NOT NULL ,
    PRIMARY KEY (
        `customer_id`
    ),
    CONSTRAINT `uc_Customer_email` UNIQUE (
        `email`
    )
);

CREATE TABLE IF NOT EXISTS `Manager` (
    `manager_id` int  NOT NULL ,
    `is_admin` bool  NOT NULL ,
    `name` nvarchar(255)  NOT NULL ,
    `email` nvarchar(255)  NOT NULL ,
    PRIMARY KEY (
        `manager_id`
    ),
    CONSTRAINT `uc_Manager_email` UNIQUE (
        `email`
    )
);

CREATE TABLE IF NOT EXISTS `Order` (
    `order_id` int  NOT NULL ,
    `customer_id` int  NOT NULL ,
    `total_amount` decimal(10,2)  NOT NULL ,
    `order_status_id` int  NOT NULL ,
    PRIMARY KEY (
        `order_id`
    )
);

CREATE TABLE IF NOT EXISTS `OrderLine` (
    `order_line_id` int  NOT NULL ,
    `order_id` int  NOT NULL ,
    `product_id` int  NOT NULL ,
    `quantity` int  NOT NULL ,
    `sub_total_amount` decimal(8,2)  NOT NULL ,
    `unit_price` decimal(8,2)  NOT NULL ,
    PRIMARY KEY (
        `order_line_id`
    )
);

CREATE TABLE IF NOT EXISTS `Product` (
    `product_id` int  NOT NULL ,
    `name` nvarchar(255)  NOT NULL ,
    `description` nvarchar(255)  NOT NULL ,
    `price` decimal(8,2)  NOT NULL ,
    `image_path` varchar(255)  NOT NULL ,
    `in_stock` int  NOT NULL ,
    PRIMARY KEY (
        `product_id`
    ),
    CONSTRAINT `uc_Product_name` UNIQUE (
        `name`
    )
);

CREATE TABLE IF NOT EXISTS `OrderStatus` (
    `order_status_id` int  NOT NULL ,
    `name` nvarchar(255)  NOT NULL ,
    PRIMARY KEY (
        `order_status_id`
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
    `customer_id` int  NOT NULL ,
    `hashed_password` binary(60)  NOT NULL ,
    PRIMARY KEY (
        `customer_id`
    )
);

CREATE TABLE IF NOT EXISTS `ManagerPassword` (
    `manager_id` int  NOT NULL ,
    `hashed_password` binary(60)  NOT NULL ,
    PRIMARY KEY (
        `manager_id`
    )
);

ALTER TABLE `Order` ADD CONSTRAINT `fk_Order_customer_id` FOREIGN KEY(`customer_id`)
REFERENCES `Customer` (`customer_id`);

ALTER TABLE `Order` ADD CONSTRAINT `fk_Order_order_status_id` FOREIGN KEY(`order_status_id`)
REFERENCES `OrderStatus` (`order_status_id`);

ALTER TABLE `OrderLine` ADD CONSTRAINT `fk_OrderLine_order_id` FOREIGN KEY(`order_id`)
REFERENCES `Order` (`order_id`);

ALTER TABLE `OrderLine` ADD CONSTRAINT `fk_OrderLine_product_id` FOREIGN KEY(`product_id`)
REFERENCES `Product` (`product_id`);

ALTER TABLE `Review` ADD CONSTRAINT `fk_Review_customer_id` FOREIGN KEY(`customer_id`)
REFERENCES `Customer` (`customer_id`);

ALTER TABLE `Review` ADD CONSTRAINT `fk_Review_product_id` FOREIGN KEY(`product_id`)
REFERENCES `Product` (`product_id`);

ALTER TABLE `CustomerPassword` ADD CONSTRAINT `fk_CustomerPassword_customer_id` FOREIGN KEY(`customer_id`)
REFERENCES `Customer` (`customer_id`);

ALTER TABLE `ManagerPassword` ADD CONSTRAINT `fk_ManagerPassword_manager_id` FOREIGN KEY(`manager_id`)
REFERENCES `Manager` (`manager_id`);

CREATE INDEX `idx_Customer_name`
ON `Customer` (`name`);

CREATE INDEX `idx_Manager_name`
ON `Manager` (`name`);

CREATE INDEX `idx_Order_customer_id`
ON `Order` (`customer_id`);

