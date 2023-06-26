employees = [
                [0, 'Nari', 'Udale', 'Female', '1993-05-13', 'Allergologist', 4636, 'Ecuador'],
                [1, 'Quinton', 'Matthai', 'Male', '1969-01-05', 'Immunologist', 7531, 'UnitedArab Emirates'],
                [2, 'Latrina', 'Gadsby', 'Female', '1959-07-21', 'Dentist', 6570, 'Ukraine'],
                [3, 'Vanna', 'Springett', 'Female', '1984-04-25', 'Orthopedist', 1589, 'Nigeria'],
                [4, 'Madelyn', 'Venneur', 'Female', '1982-03-25', 'Traumatologist', 4004, 'China'],
                [5, 'Maddy', 'McGilvary', 'Male', '1969-12-07', 'Neurosurgeon', 7649, 'Indonesia'],
                [6, 'Risa', 'Boles', 'Female', '1959-01-12', 'Anesthetist', 2063, 'Portugal'],
                [7, 'Jackie', 'Hammell', 'Male', '1973-09-15', 'Urologist', 5803, 'Estonia'],
                [8, 'Rennie', 'Dobey', 'Female', '1979-06-19', 'Gynecologist', 3984, 'Ukraine'],
                [9, 'Stacee', 'Pinckney', 'Male', '1983-10-02', 'Rheumatologist', 2626, 'China'],
                [10, 'Erica', 'Trollope', 'Female', '1983-01-20', 'Pulmonologist', 6088, 'Indonesia'],
                [11, 'Brandyn', 'Probet', 'Male', '1960-05-15', 'Infectious diseases doctor', 7784, 'Japan'],
                [12, 'Ardis', 'Tomaselli', 'Female', '1963-04-06', 'Hematologist',  1092, 'Finland'],
                [13, 'Reine', 'Murthwaite', 'Female', '1987-03-03', 'Endocrinologist', 3716, 'Indonesia'],
                [14, 'Alexandrina', 'Perkins', 'Female', '1970-12-30', 'Cardiologist', 7201, 'Brazil'],
                [15, 'Ellen', 'Tolumello', 'Female', '1972-09-07', 'Oncologist', 2224, 'Ethiopia'],
                [16, 'Kylila', 'Mc Mechan', 'Female', '1993-06-20', 'Pediatrician', 1282, 'Antigua and Barbuda'],
                [17, 'Louella', 'Salvador', 'Female', '1986-12-30', 'Nephrologist', 2218, 'Philippines'],
    ]

titles = ['id', 'first_name', 'last_name', 'gender', 'birth_date', 'position', 'salary', 'country']

employees_json = {emp[0]: {titles[idx]: e for idx, e in enumerate(emp)} for emp in employees}
