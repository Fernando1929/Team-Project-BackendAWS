-- tables
CREATE TABLE users (user_id serial primary key, user_firstname varchar(20), user_lastname varchar(20), 
user_date_birth char(10));

CREATE TABLE login (login_id serial primary key, username varchar(30), password varchar(30), 
user_id integer references users(user_id));

CREATE TABLE admin (admin_id serial primary key, user_id integer references users(user_id));

CREATE TABLE faction_leader (leader_id serial primary key, user_id integer references users(user_id));

CREATE TABLE survivor (survivor_id serial primary key, user_id integer references users(user_id));

CREATE TABLE manages (user_id integer references users(user_id), admin_id integer references admin(admin_id), 
primary key (user_id, admin_id));

CREATE TABLE location (location_id serial primary key, user_id integer references users(user_id), city varchar(20), state_province varchar(20));

CREATE TABLE represents (faction_id integer references faction(faction_id), leader_id integer references 
faction_leader(leader_id), primary key (faction_id, leader_id));

CREATE TABLE faction (faction_id serial primary key, faction_name varchar(20), faction_population integer, faction_rating varchar(20), faction_wealth varchar(50), 
faction_territory char(10));

--Relationships tables




--Resources
CREATE TABLE resource (resource_id serial primary key, resource_name varchar(50), resource_availability boolean);

CREATE TABLE fuel (fuel_id serial primary key, resource_id integer references resource(resource_id), 
fuel_type varchar(10), fuel_gallons float);


CREATE TABLE food (food_id serial primary key, resource_id integer references resource(resource_id), 
food_category varchar(15), food_quantity integer, food_type varchar(15));


CREATE TABLE medicine (med_id serial primary key, resource_id integer references resource(resource_id), 
med_type varchar(15), med_quantity integer);


CREATE TABLE water (water_id serial primary key, resource_id integer references resource(resource_id), 
water_quantity varchar(10), water_container varchar(10), water_type varchar(10));


CREATE TABLE cloth (cloth_id serial primary key, resource_id integer references resource(resource_id), 
cloth_type varchar(15), cloth_quatity integer);

CREATE TABLE weapons (weapon_id serial primary key, resource_id integer references resource(resource_id), 
weapon_type varchar(10), weapon_quantity integer);