CREATE TABLE login (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username NOT NULL,
  email TEXT NOT NULL,
  Full_name NoT NULL,
  password TEXT NOT NULL,
  Access text not null
);
ALTER TABLE login
ADD COLUMN Payment text;

INSERT INTO login (username, email, Full_name, password, Access)
VALUES ('hemu', 'hmanral265@gmail.com', 'himanshu manral', '123', 'admin');
select * from login
Update login set Payment='pending' where username='hritik';

DELETE FROM login WHERE id =3;


Create Table Profile 
(id INTEGER PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
email TEXT NOT NULL,
age TEXT NOT NULL,
height text ,
weight text,
experience text ,
achivements text ,
intrest text);

CREATE table Equipments(buy_date text,Equip_name text,Manufacturer text,Quantity text,Price text)
INSERT INTO Equipments (buy_date, Equip_name, Manufacturer, Quantity, Price) VALUES ('2023-06-05', 'Dumbbells', 'ABC Sports', '10', '200');


CREATE TABLE class_shedule(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username text,
shift text,
date text,
start_time text,
end_time text);

ALTER TABLE class_shedule
ADD COLUMN Performance text;

SELECT * From class_shedule


CREATE TABLE feedback (name text,message text);


CREATE TABLE trainer_shedule(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username text,
shift text,
date text,
start_time text,
end_time text);
ALTER TABLE trainer_shedule
ADD COLUMN To_date text;
SELECT * From trainer_shedule