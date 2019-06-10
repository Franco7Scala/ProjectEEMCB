CREATE TABLE nation (
	id INTEGER PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE production_data (
	nation_id INTEGER,
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
    
    PRIMARY KEY (nation_id, day_in_year, hour),
    FOREIGN KEY (nation_id) REFERENCES nation (id)
);