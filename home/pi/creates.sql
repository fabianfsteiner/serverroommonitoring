create database if not exists severraum_temperaturueberwachung;
use severraum_temperaturueberwachung;

create table sensor (sensorID int primary key auto_increment, sensorName varchar(20),
	sensorKennung varchar(50) unique, sensorPosition varchar(50));
create table temp (tempID int primary key auto_increment, temp decimal(10,1));
create table feucht (feuchtID int primary key auto_increment, feucht decimal(10,1));

create table messung(messungsID bigint primary key auto_increment, zeit datetime,fk_tempID int, fk_feuchtID int
, fk_sensorID int,
constraint fk_tmp foreign key (fk_tempID) references temp (tempID),
constraint fk_feu foreign key (fk_feuchtID) references feucht (feuchtID),
constraint fk_sen foreign key (fk_sensorID) references sensor (sensorID));

#drop function func_temp;
DELIMITER //
CREATE function func_temp(t decimal(10,1))
     RETURNS int
     DETERMINISTIC
    BEGIN
		DECLARE count INT;
        select count(*) into count from temp where temp = t;
        if count = 0 then
		insert into temp (temp) values (t);
        select tempID into count from temp order by tempID desc limit 1;
        else
         select tempID into count from temp where temp = t;
        end if;
        return count;
	END //
    DELIMITER ;

DELIMITER //
CREATE function func_feucht(f decimal(10,1))
     RETURNS int
     DETERMINISTIC
    BEGIN
		DECLARE count INT;
        select count(*) into count from feucht where feucht = f;
        if count = 0 then
		insert into feucht (feucht) values (f);
        select feuchtID into count from feucht order by feuchtID desc limit 1;
        else
         select feuchtID into count from feucht where feucht = f;
        end if;
        return count;
	END //
    DELIMITER ;

#drop function func_getSID;
DELIMITER //
CREATE function func_getSID(sK varchar(50))
     RETURNS int
     DETERMINISTIC
    BEGIN
		DECLARE sID INT;
        select count(*) into sID from sensor where sensorKennung = sK;
        if sID = 0 then
		insert into sensor (sensorKennung) values (sK);
        end if;
        select sensorID into sID from sensor where sensorKennung = sK;
        return sID;
	END //
    DELIMITER ;

#alter table sensor change column sensorKennung sensorKennung varchar(50) unique;
CREATE UNIQUE INDEX un_sensor ON sensor (sensorID, sensorKennung);  

grant all on *.* TO 'webuser'@'%' 
identified by 'La4R2uyME78hAfn9I1pH';

CREATE USER 'webuser'@'%' IDENTIFIED BY 'La4R2uyME78hAfn9I1pH';

SET PASSWORD FOR 'webuser'@'localhost' = PASSWORD('La4R2uyME78hAfn9I1pH');


#drop trigger tri_messung;
DELIMITER //
CREATE TRIGGER tri_messung before insert on messung
 FOR EACH ROW
 BEGIN
	set new.zeit = SYSDATE();
 END //
DELIMITER ;


create view view_mes as select zeit, temp, feucht , sensorName from messung inner join sensor s on fk_sensorID =  s.sensorID left outer join temp on fk_tempID = tempID left outer join feucht on  fk_feuchtID = feuchtID order by zeit desc;
create view web as select zeit, temp, feucht , sensorName, sensorID from messung inner join sensor s on fk_sensorID =  s.sensorID left outer join temp on fk_tempID = tempID left outer join feucht on  fk_feuchtID = feuchtID order by zeit desc;