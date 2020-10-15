"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

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

def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    table = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    country_code_dict = {}
    code_info_reader = read_csv_as_list_dict(codeinfo['codefile'],
                                             codeinfo['separator'],
                                             codeinfo['quote'])
    for country in code_info_reader:
        plot_codes = country[codeinfo['plot_codes']]
        data_codes = country[codeinfo['data_codes']]
        country_code_dict[plot_codes] = data_codes
    return country_code_dict


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    country_dict = {}
    country_notfound = []
    country_code_dict = build_country_code_converter(codeinfo)
    new_country_code_dict = {}
    for plotcode, wbcode in country_code_dict.items():
        new_country_code_dict[plotcode.lower()] = wbcode.lower() 
    for country_code in plot_countries:
        if country_code.lower() in new_country_code_dict:
            wb_country_code = new_country_code_dict[country_code.lower()]
        else:
            country_notfound.append(country_code)
            continue
        temp = 0
        for gdp_country_code in gdp_countries:
            if wb_country_code == gdp_country_code.lower():
                country_dict[country_code] = gdp_country_code
                temp = 1
                break
        if temp == 0:
            country_notfound.append(country_code)
    return country_dict, set(country_notfound)


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

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
                                       gdpinfo['country_code'],
                                       gdpinfo['separator'],
                                       gdpinfo['quote'])
    (plot_country_dict, plot_country_notfound) = reconcile_countries_by_code(codeinfo,
                                                                             plot_countries,
                                                                             gdp_dict)
    for country_code in plot_country_dict:
        if gdp_dict[plot_country_dict[country_code]][year] != '':
            log_gdp = math.log(float(gdp_dict[plot_country_dict[country_code]][year]), 10)
            country_log_gdp[country_code] = log_gdp
        else:
            country_no_gdp.append(country_code)
    return country_log_gdp, plot_country_notfound, set(country_no_gdp)


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    (country_gdp, plot_country_notfound, country_no_gdp) = build_map_dict_by_code(gdpinfo,
                                                                                  codeinfo,
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
    Test the project code for several years
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

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

#test_render_world_map()
