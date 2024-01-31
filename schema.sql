CREATE TABLE IF NOT EXISTS `Customer` (
    `CustomerID` int  NOT NULL ,
    `Name` nvarchar(255)  NOT NULL ,
    `E-mail` nvarchar(255)  NOT NULL ,
    `Address` nvarchar(255)  NOT NULL ,
    `Postcode` varchar(10)  NOT NULL ,
    `City` nvarchar(255)  NOT NULL ,
    PRIMARY KEY (
        `CustomerID`
    )
);

CREATE TABLE IF NOT EXISTS `Manager` (
    `ManagerID` int  NOT NULL ,
    `IsAdmin` bool  NOT NULL ,
    `Name` nvarchar(255)  NOT NULL ,
    `E-mail` nvarchar(255)  NOT NULL ,
    PRIMARY KEY (
        `ManagerID`
    )
);

CREATE TABLE IF NOT EXISTS `Order` (
    `OrderID` int  NOT NULL ,
    `CustomerID` int  NOT NULL ,
    `TotalAmount` decimal(6,2)  NOT NULL ,
    `OrderStatusID` int  NOT NULL ,
    PRIMARY KEY (
        `OrderID`
    )
);

CREATE TABLE IF NOT EXISTS `OrderLine` (
    `OrderLineID` int  NOT NULL ,
    `OrderID` int  NOT NULL ,
    `ProductID` int  NOT NULL ,
    `Quantity` int  NOT NULL ,
    PRIMARY KEY (
        `OrderLineID`
    )
);

CREATE TABLE IF NOT EXISTS `Product` (
    `ProductID` int  NOT NULL ,
    `Name` nvarchar(255)  NOT NULL ,
    `Description` nvarchar(255)  NOT NULL ,
    `Price` decimal(6,2)  NOT NULL ,
    `ImagePath` varchar(255)  NOT NULL ,
    `InStock` int  NOT NULL ,
    PRIMARY KEY (
        `ProductID`
    ),
    CONSTRAINT `uc_Product_Name` UNIQUE (
        `Name`
    )
);

CREATE TABLE IF NOT EXISTS `OrderStatus` (
    `OrderStatusID` int  NOT NULL ,
    `Name` nvarchar(255)  NOT NULL ,
    PRIMARY KEY (
        `OrderStatusID`
    ),
    CONSTRAINT `uc_OrderStatus_Name` UNIQUE (
        `Name`
    )
);

CREATE TABLE IF NOT EXISTS `Review` (
    `CustomerID` int  NOT NULL ,
    `ProductID` int  NOT NULL ,
    `Rating` int  NULL ,
    `ReviewText` nvarchar(255)  NULL ,
    `ReviewDate` datetime  NULL ,
    `ReviewHeader` nvarchar(255)  NULL ,
    PRIMARY KEY (
        `CustomerID`,`ProductID`
    )
);

CREATE TABLE IF NOT EXISTS `CustomerPasswords` (
    `CustomerID` int  NOT NULL ,
    `HashedPassword` binary(60)  NOT NULL ,
    PRIMARY KEY (
        `CustomerID`
    )
);

CREATE TABLE IF NOT EXISTS `ManagerPasswords` (
    `ManagerID` int  NOT NULL ,
    `HashedPassword` binary(60)  NOT NULL ,
    PRIMARY KEY (
        `ManagerID`
    )
);

ALTER TABLE `Order` ADD CONSTRAINT `fk_Order_CustomerID` FOREIGN KEY(`CustomerID`)
REFERENCES `Customer` (`CustomerID`);

ALTER TABLE `Order` ADD CONSTRAINT `fk_Order_OrderStatusID` FOREIGN KEY(`OrderStatusID`)
REFERENCES `OrderStatus` (`OrderStatusID`);

ALTER TABLE `OrderLine` ADD CONSTRAINT `fk_OrderLine_OrderID` FOREIGN KEY(`OrderID`)
REFERENCES `Order` (`OrderID`);

ALTER TABLE `OrderLine` ADD CONSTRAINT `fk_OrderLine_ProductID` FOREIGN KEY(`ProductID`)
REFERENCES `Product` (`ProductID`);

ALTER TABLE `Review` ADD CONSTRAINT `fk_Review_CustomerID` FOREIGN KEY(`CustomerID`)
REFERENCES `Customer` (`CustomerID`);

ALTER TABLE `Review` ADD CONSTRAINT `fk_Review_ProductID` FOREIGN KEY(`ProductID`)
REFERENCES `Product` (`ProductID`);

ALTER TABLE `CustomerPasswords` ADD CONSTRAINT `fk_CustomerPasswords_CustomerID` FOREIGN KEY(`CustomerID`)
REFERENCES `Customer` (`CustomerID`);

ALTER TABLE `ManagerPasswords` ADD CONSTRAINT `fk_ManagerPasswords_ManagerID` FOREIGN KEY(`ManagerID`)
REFERENCES `Manager` (`ManagerID`);

CREATE INDEX `idx_Customer_Name`
ON `Customer` (`Name`);

CREATE INDEX `idx_Manager_Name`
ON `Manager` (`Name`);