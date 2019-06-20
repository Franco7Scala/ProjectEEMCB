DROP SCHEMA eemcb;
CREATE SCHEMA eemcb;
USE eemcb;

CREATE TABLE nation (
	code VARCHAR(5) PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE production_data (
	nation_code VARCHAR(5),
	year INTEGER,
    day_in_year INTEGER,
    holiday BOOL,
    hour INTEGER,
    production_pv FLOAT,
    production_hydro FLOAT,
    production_biomass FLOAT,
    production_wind FLOAT,
    consumption FLOAT,
    transits FLOAT,
    price_oil FLOAT,
    price_gas FLOAT,
    price_carbon FLOAT,
    
    production_fossil_coal_gas FLOAT,
    production_fossil_gas FLOAT,
    production_fossil_hard_coal FLOAT,
    production_fossil_oil FLOAT,
    production_nuclear FLOAT,
    production_other FLOAT,
    production_waste FLOAT,
    production_lignite FLOAT,
    production_other_renewable FLOAT,
    production_other_geothermal FLOAT,

    PRIMARY KEY (nation_code, day_in_year, hour),
    FOREIGN KEY (nation_code) REFERENCES nation (code)
);


INSERT INTO nation VALUES ('IT', 'Italy');
INSERT INTO nation VALUES ('DE', 'Germany');
INSERT INTO nation VALUES ('BE', 'Belgium');
INSERT INTO nation VALUES ('CH', 'Switzerland');
INSERT INTO nation VALUES ('FR', 'France');
INSERT INTO nation VALUES ('NL', 'Netherlands');
