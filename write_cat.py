"""
This takes the input catalog data and writes out the LFT3 catalog.  Only should need once.
"""
import isaacsonetal, ly100, recons100, recons49
import csv


iea = isaacsonetal.Catalog()
ly100 = ly100.Catalog()
recons100 = recons100.Catalog()
recons49 = recons49.Catalog()

fields = [
    'Name',           # Name of the star
    'Distance',       # Distance in light-years
    'Distance_err',   # Distance error in light-years
    'RA',             # Right Ascension in decimal hours
    'Dec',            # Declination in decimal degrees
    'SpectralType',   # Spectral classification
    'Mass',           # Mass in solar masses
    'Notes',          # Additional notes
    'OtherNames',     # Other designations
    'Constellation',  # Constellation of the star
    'Source'          # Source of the entry
]


pc2m = 3.08567758128E+16
pc2ly = 3.26156

with open('lft3cat_V.csv', 'w') as fp:
    writer = csv.writer(fp)
    writer.writerow(fields)

    for row in iea.cat:
        data = {
            'Name': row.Name,
            'Distance': f"{row.dist_pc * pc2ly:.2f}",
            'Distance_err': row.disterr,
            'RA': f"{row.RA:.4f}",
            'Dec': f"{row.Dec:.3f}",
            'SpectralType': row.spec,
            'Mass': '',
            'Notes': '',
            'OtherNames': '',
            'Constellation': '',
            'Source': 'Isaacson et al.'
        }
        row = [data[field] for field in fields]
        writer.writerow(row)

    for row in ly100.cat:
        data = {
            'Name': row.name,
            'Distance': f"{row.dist_ly:.2f}",
            'Distance_err': row.disterr,
            'RA': 0.0,
            'Dec': 0.0,
            'SpectralType': row.spec,
            'Mass': '',
            'Notes': row.notes,
            'OtherNames': row.other,
            'Constellation': row.constellation,
            'Source': 'https://chview.nova.org/solcom/'
        }
        row = [data[field] for field in fields]
        writer.writerow(row)

    for row in recons100.cat:
        data = {
            'Name': row.name,
            'Distance': '0.0',
            'Distance_err': '0.0',
            'RA': f"{row.ra:.4f}",
            'Dec': f"{row.dec:.3f}",
            'SpectralType': row.spec,
            'Mass': row.mass,
            'Notes': row.notes,
            'OtherNames': row.common_name,
            'Constellation': '',
            'Source': 'http://www.recons.org/TOP100.posted.htm'
        }
        row = [data[field] for field in fields]
        writer.writerow(row)

    for row in recons49.cat:
        data = {
            'Name': row.name,
            'Distance': '0.0',
            'Distance_err': '0.0',
            'RA': f"{row.ra:.4f}",
            'Dec': f"{row.dec:.3f}",
            'SpectralType': row.spec,
            'Mass': 0.0,
            'Notes': '',
            'OtherNames': '',
            'Constellation': '',
            'Source': '2006AJ....132.2360H'
        }
        row = [data[field] for field in fields]
        writer.writerow(row)