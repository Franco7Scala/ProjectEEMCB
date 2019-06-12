

class Tuple:
    def __init__(self, nation = None, year = 0, day_in_year = 0, hour = 0, holiday = False, date = None, production_pv = 0, production_hydro = 0, production_biomass = 0, production_wind = 0, consumption = 0, transits = 0, price_oil = 0, price_gas = 0, price_carbon = 0, production_fossil_coal_gas = 0, production_fossil_gas = 0, production_fossil_hard_coal = 0, production_fossil_oil = 0, production_nuclear = 0, production_other = 0, production_waste = 0, production_lignite = 0):
        self.nation = nation
        self.year = year
        self.day_in_year = day_in_year
        self.hour = hour
        self.holiday = holiday
        self.date = date
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

    def __str__(self):
        return "nation: " + str(self.nation) + "\t" + \
               "year: " + str(self.year) + "\t" + \
               "day_in_year: " + str(self.day_in_year) + "\t" + \
               "hour: " + str(self.hour) + "\t" + \
               "holiday: " + str(self.holiday) + "\t" + \
               "date: " + str(self.date) + "\t" + \
               "production_pv: " + str(self.production_pv) + "\t" \
               "production_hydro: " + str(self.production_hydro) + "\t" + \
               "production_biomass: " + str(self.production_biomass) + "\t" \
               "production_wind: " + str(self.production_wind) + "\t" \
               "consumption: " + str(self.consumption) + "\t" + \
               "transits: " + str(self.transits) + "\t" + \
               "price_oil: " + str(self.price_oil) + "\t" + \
               "price_gas: " + str(self.price_gas) + "\t" + \
               "price_carbon: " + str(self.price_carbon) + "\t" + \
               "production_fossil_coal_gas: " + str(self.production_fossil_coal_gas) + "\t" \
               "production_fossil_gas: " + str(self.production_fossil_gas) + "\t" + \
               "production_fossil_hard_coal: " + str(self.production_fossil_hard_coal) + "\t" \
               "production_fossil_oil: " + str(self.production_fossil_oil) + "\t" \
               "production_nuclear: " + str(self.production_nuclear) + "\t" \
               "production_other: " + str(self.production_other) + "\t" + \
               "production_waste: " + str(self.production_waste) + "\t" \
               "production_lignite: " + str(self.production_lignite)
