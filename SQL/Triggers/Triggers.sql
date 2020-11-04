alter table innodb.WorldTesting  add constraint PositiveCheck check (positive >= 0);

alter table innodb.UsCountyCaseInformation add constraint CaseCheck check (cases >= 0);

DELIMITER $$

CREATE TRIGGER trigger_name
    BEFORE INSERT
    ON innodb.UsCountyCaseInformation FOR EACH ROW
BEGIN
    -- statements
    declare sum_deaths int;
    declare deaths int;
    
    select sum(deaths) into sum_deaths from innodb.UsCountyCaseInformation where Dat like new.Dat;
    
    select death into deaths from innodb.world_death where dat like new.Dat;
    
   IF sum_deaths > deaths THEN
        signal sqlstate '45000' set message_text = 'Sum of deaths error!';
    END IF; 
    
END$$    

DELIMITER ;

