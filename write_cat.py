"""
This takes the input catalog data and writes out the LFT3 catalog.  Only should need once.
"""
import isaacsonetal, ly100


iea = isaacsonetal.Catalog()
ly100 = ly100.Catalog()

fields = [
    'Name',           # Name of the star
    'Distance',       # Distance in light-years
    'Distance_err',   # Distance error in light-years
    'RA',             # Right Ascension in decimal hours
    'Dec',            # Declination in decimal degrees
    'SpectralType',   # Spectral classification
    'Mass',           # Mass in solar masses
    'Mag',            # Magnitude of the star
    'Notes',          # Additional notes
    'OtherNames',     # Other designations
    'Constellation',  # Constellation of the star
    'Source'          # Source of the entry
]


pc2m = 3.08567758128E+16
pc2ly = 3.26156

with open('lft3cat.csv', 'w') as fp:
    print(','.join(fields), file=fp)

    for row in iea.cat:
        data = {
            'Name': row.Name,
            'Distance': f"{row.dist_pc * pc2ly:.2f}",
            'Distance_err': row.disterr,
            'RA': f"{row.RA:.4f}",
            'Dec': f"{row.Dec:.3f}",
            'SpectralType': row.spec,
            'Mass': '',
            'Mag': row.mag,
            'Notes': '',
            'OtherNames': '',
            'Constellation': '',
            'Source': 'Isaacson et al.'
        }
        print(','.join(str(data[field]) for field in fields), file=fp)

    for row in ly100.cat:
        data = {
            'Name': row.name,
            'Distance': f"{row.dist_ly:.2f}",
            'Distance_err': row.disterr,
            'RA': 0.0,
            'Dec': 0.0,
            'SpectralType': row.spec,
            'Mass': '',
            'Mag': row.mag,
            'Notes': row.notes,
            'OtherNames': row.other,
            'Constellation': row.constellation,
            'Source': 'SolStation'
        }
        print(','.join(str(data[field]) for field in fields), file=fp)