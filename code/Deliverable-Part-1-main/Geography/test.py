import re
import csv


pattern = r"""
    ^
    (?P<country>[^,]+),                     
    "(?P<area_data>[^"]+)",                 # Total/Land/Water areas
    "(?P<border_data>[^"]+)",               # Border information
    (?:"
        (?P<elevation_data>[^"]+)"         # Elevation points
    |                                      
        (?P<unquoted_elevation>[^,]+)      # Unquoted elevation fallback
    ),
    (?P<land_use>[^,]+),                   # Agricultural land data
    (?P<salt_lakes>.*?)                    # Salt lake information
    (?:,\s*(?P<notes>.*))?                 
    $
"""

regex = re.compile(pattern, re.VERBOSE | re.IGNORECASE)

def parse_data(file_path):
    countries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Normalize special cases
            line = re.sub(r'note\s*\d*:', 'note:', line)
            match = regex.match(line)
            
            if not match:
                print(f"Skipping unparseable line: {line}")
                continue
            
            data = match.groupdict()
            country = {
                'Country': data['country'].strip(),
                'Total_Area': None,
                'Land_Area': None,
                'Water_Area': None,
                'Total Border Length (km)': None,
                'Number of Border Countries': None,
                'Bordering Countries': None,
                'Highest Point': None,
                'Lowest Point': None,
                'Mean Elevation': None,
                'Agricultural Land (%)': None,
                'Arable Land (%)': None,
                'Permanent Crops (%)': None,
                'Salt Lake Name': None,
                'Salt Lake Size (sq km)': None
            }

            area_match = re.match(
                r':([\d,]+)\s*sq\s*kmland:([\d,]+)\s*sq\s*kmwater:([\d,]+)\s*sq\s*km',
                data['area_data']
            )
            if area_match:
                country.update({
                    'Total_Area': area_match[1].replace(',', ''),
                    'Land_Area': area_match[2].replace(',', ''),
                    'Water_Area': area_match[3].replace(',', '')
                })

            border_info = data['border_data']
            border_length = re.search(r'^([\d,]+)\s*km', border_info)
            if border_length:
                country['Total Border Length (km)'] = border_length[1].replace(',', '')
                
            countries_match = re.search(r'border countries \((\d+)\):(.+)', border_info)
            if countries_match:
                country.update({
                    'Number of Border Countries': countries_match[1],
                    'Bordering Countries': ', '.join(
                        [c.split()[0] for c in countries_match[2].split(';')]
                    )
                })


            elevation = data['elevation_data'] or data['unquoted_elevation']
            if elevation:
                hp = re.search(r'([A-Za-z\s]+)\s*([\d,]+)\s*m', elevation)
                lp = re.search(r'lowest point:([A-Za-z\s]+)\s*([\d,]+)\s*m', elevation)
                me = re.search(r'mean elevation:([\d,]+)\s*m', elevation)
                
                if hp:
                    country['Highest Point'] = f"{hp[1].strip()} ({hp[2]} m)"
                if lp:
                    country['Lowest Point'] = f"{lp[1].strip()} ({lp[2]} m)"
                if me:
                    country['Mean Elevation'] = f"{me[1]} m"

            land_use_pattern = r"""
                ([\d.]+)%\s*\(.*?\)\s*
                arable\s*land:\s*([\d.]+)%\s*  
                permanent\s*crops:\s*([\d.]+)%
            """
            lu_match = re.search(land_use_pattern, data['land_use'], re.VERBOSE)
            if lu_match:
                country.update({
                    'Agricultural Land (%)': lu_match[1],
                    'Arable Land (%)': lu_match[2],
                    'Permanent Crops (%)': lu_match[3]
                })

            salt_lake_match = re.search(r'([A-Za-z\-\(\)\s]+)\s*-\s*([\d,]+)\s*sq\s*km', data['salt_lakes'])
            if salt_lake_match:
                country.update({
                    'Salt Lake Name': salt_lake_match[1].strip(),
                    'Salt Lake Size (sq km)': salt_lake_match[2].replace(',', '')
                })

            countries.append(country)
    return countries

def export_to_csv(data, output_file):
    fieldnames = [
        'Country', 'Total_Area', 'Land_Area', 'Water_Area',
        'Total Border Length (km)', 'Number of Border Countries',
        'Bordering Countries', 'Highest Point', 'Lowest Point',
        'Mean Elevation', 'Agricultural Land (%)', 'Arable Land (%)',
        'Permanent Crops (%)', 'Salt Lake Name', 'Salt Lake Size (sq km)'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


input_file = "output_1.csv"
output_file = "country_geography.csv"
parsed_data = parse_data(input_file)
export_to_csv(parsed_data, output_file)