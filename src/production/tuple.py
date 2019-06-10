

class Tuple:
    def __init__(self, nation = None, year = None, day_in_year = None, hour = None, holiday = None, production_pv = None, production_hydro = None, production_biomass = None, production_wind = None, consumption = None, transits = None, price_oil = None, price_gas = None, price_carbon = None, production_fossil_coal_gas = None, production_fossil_gas = None, production_fossil_hard_coal = None, production_fossil_oil = None, production_nuclear = None, production_other = None, production_waste = None, production_lignite = None):
        self.nation = nation
        self.year = year
        self.day_in_year = day_in_year
        self.hour = hour
        self.holiday = holiday
        self.production_pv = production_pv
        self.production_hydro = production_hydro
        self.production_biomass = production_biomass
        self.production_wind = production_wind
        self.consumption = consumption
        self.transits = transits
        self.price_oil = price_oil
        self.price_gas = price_gas
        self.price_carbon = price_carbon
        self.production_fossil_coal_gas = production_fossil_coal_gas
        self.production_fossil_gas = production_fossil_gas
        self.production_fossil_hard_coal = production_fossil_hard_coal
        self.production_fossil_oil = production_fossil_oil
        self.production_nuclear = production_nuclear
        self.production_other = production_other
        self.production_waste = production_waste
        self.production_lignite = production_lignite

    def __lt__(self, other):
        if self.nation == other.nation:
            if self.year < other.year:
                if self.day_in_year < other.day_in_year:
                    if self.hour < other.hour:
                        return True

        return False

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        if self.nation == other.nation:
            if self.year == other.year:
                if self.day_in_year == other.day_in_year:
                    if self.hour == other.hour:
                        return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)
