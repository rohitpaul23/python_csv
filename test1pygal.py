"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    nestdictlist = {}
    with open(filename, "rt", newline='') as csvfile:
        csvreader = csv.DictReader(csvfile,
                                   delimiter=separator,
                                   quotechar=quote)
        for row in csvreader:
            nestdictlist[row[keyfield]] = row
    return nestdictlist


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    country_dict = {}
    country_notfound = []
    for country_code in plot_countries:
        if plot_countries[country_code] in gdp_countries:
            country_dict[country_code] = plot_countries[country_code]
        else:
            country_notfound.append(country_code)
    return country_dict, set(country_notfound)


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    country_log_gdp = {}
    country_no_gdp = []
    gdp_dict = read_csv_as_nested_dict(gdpinfo['gdpfile'],
                                       gdpinfo['country_name'],
                                       gdpinfo['separator'],
                                       gdpinfo['quote'])
    (plot_country_dict, plot_country_notfound) = reconcile_countries_by_name(plot_countries,
                                                                             gdp_dict)
    for country_code in plot_country_dict:
        if gdp_dict[plot_country_dict[country_code]][year] != '':
            log_gdp = math.log(float(gdp_dict[plot_country_dict[country_code]][year]), 10)
            country_log_gdp[country_code] = log_gdp
        else:
            country_no_gdp.append(country_code)
    return country_log_gdp, plot_country_notfound, set(country_no_gdp)


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    (country_gdp, plot_country_notfound, country_no_gdp) = build_map_dict_by_name(gdpinfo,
                                                                                  plot_countries,
                                                                                  year)
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = f'GDP by country for {year} (log scale), unified by common country NAME'
    worldmap_chart.add(f'GDP for {year}',
                       country_gdp)
    worldmap_chart.add('Missing from World Bank Data',
                       plot_country_notfound)
    worldmap_chart.add('No GDP data',
                       country_no_gdp)
    worldmap_chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

#test_render_world_map()