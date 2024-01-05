import sqlite3


class Hero:
    def __init__(self, name, main_attribute, base_damage, armor, start_HP, abilities):
        self.name = name
        self.main_attribute = main_attribute
        self.base_damage = base_damage
        self.armor = armor
        self.start_HP = start_HP
        self.abilities = abilities


    def __str__(self):
        return f'''Hero name: {self.name};
Main attribute: {self.main_attribute};
Armor: {self.armor};
Start HP: {self.start_HP};
Abilities: {", ".join((self.abilities).split(', '))};
'''



con = sqlite3.connect('dota.db')
cursor = con.cursor()
con.execute('''CREATE TABLE IF NOT EXISTS heroes(
            name TEXT PRIMARY KEY NOT NULL,
            main_attribute TEXT,
            base_damage INTEGER,
            armor INTEGER,
            start_HP INTEGER,
            abilities TEXT
)''')


def appearanceHero(cursor):
    rows = cursor.fetchall()
    for row in rows:
        heroOutput = Hero(row[0], row[1], row[2], row[3], row[4], row[5])
        print(f'\n{heroOutput}')
        
        
def messageSearchHeroNoFound(name = None):
        if name:
            print(f'\nHero {name} is not found')
        else:
            print('\nNo heroes found')
    

def checkCorrectIntValue(value):
    if value.isdigit():
        if int(value) >= 0:
            return True
        else:
            print('Invalid value')
            return False     


def addHero():
    name = input('Enter the name: ')
    try:
        con.execute("INSERT INTO heroes (name, main_attribute, base_damage, armor, start_HP, abilities) VALUES (?, ?, ?, ?, ?, ?)", settingCharacteristicsByName(name, True))
        print(f'Hero {name} successfully added!')
        con.commit()
    except sqlite3.IntegrityError:
        print(f'Error: Hero with name {name} already exists!')


def showData():
    cursor.execute("SELECT * FROM heroes")
    appearanceHero(cursor)


def settingCharacteristicsByName(name, need_for_name):        
    main_attribute = input('Enter the main attribute (\'S\', \'A\', \'I\', \'U\'): ')
    while main_attribute not in ['S', 'A', 'I', 'U']:
        print('Invalid value. Please enter one of the valid main attributes: \'S\', \'A\', \'I\'or \'U\'.')
        main_attribute = input('Enter the main attribute (\'S\', \'A\', \'I\', \'U\'): ')
    while True:
        base_damage = input('Enter the Based damage: ')
        if checkCorrectIntValue(base_damage):
            break
    while True:
        armor = input('Enter the Armor: ')
        if checkCorrectIntValue(armor):
            break
    while True:
        start_HP = input('Enter the Start HP: ')
        if checkCorrectIntValue(start_HP):
            break
    abilities = input('Enter the abilities (Enter separated by commas): ')
    hero = Hero(name, main_attribute, base_damage, armor, start_HP, abilities)
    if need_for_name:
        return (hero.name, hero.main_attribute, hero.base_damage, hero.armor, hero.start_HP, hero.abilities)
    else:
        return (hero.main_attribute, hero.base_damage, hero.armor, hero.start_HP, hero.abilities)


def searchName(name):
    if isHeroInDatabase(name) == True:
        appearanceHero(cursor)
    else:
        messageSearchHeroNoFound(name)
    
    
def updateHeroInformation(name):
    data_to_update = settingCharacteristicsByName(name, False)
    cursor.execute("UPDATE heroes  SET main_attribute = ?, base_damage = ?, armor = ?, start_HP = ?, abilities = ? WHERE name = ?",
                   data_to_update + (name, ))
    con.commit()
    print(f'Information about {name} successfully update')
    
    
def isHeroInDatabase(name):
    try:
        name = name.lower()
        cursor.execute("SELECT * FROM heroes WHERE lower(name) == ?", (name,))
        return True
    except:
        messageSearchHeroNoFound(name)
        return False
        


while True:
    print('\n1. Add hero')
    print('2. Print')
    print('3. Searh from Name')
    print('4. Update')
    print('5. Выход')

    choice = input('Выберите действие: (1/2/3/4/5)\n')

    if choice == '1':
        addHero()

    elif choice == '2':
        showData()
         
    elif choice == '3':
        name = input('Enter the name: ')
        searchName(name)

    elif choice == '4':
        name = input('Enter the name: ')
        updateHeroInformation(name)

    elif choice == '5':
        print('Exit')
        break

    else:
        print('Invalid value')

con.close()
