class Entry:
    fields = [
        'Name',           # Name of the star
        'Distance',       # Distance in light-years
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

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if key not in self.fields:
                raise ValueError(f"Invalid field: {key}")
            setattr(self, key, val)