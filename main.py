from telegraph.telegraph_manager import TelegraphManager, TelegraphException
from telegraph.elements import Symbol


def main():
    print("------------------------- R1 -------------------------")
    mg = TelegraphManager()

    print(mg.add_station("Marsiglia"))  # 1
    print(mg.add_station("Parigi"))     # 2 
    print(mg.add_station("Marsiglia"))  # 2

    print(mg.add_station("Nantes"))     # 3
    print(mg.add_station("Lione"))      # 4
    print(mg.add_station("Avignone"))   # 5

    print(mg.stations)  # {'Parigi', 'Nantes', 'Marsiglia', 'Lione', 'Avignone'}

    msg1 = mg.add_message("salut", "Nantes", "Parigi")  
    print(msg1.text)        # salut
    print(msg1.sender)      # Nantes
    print(msg1.receiver)    # Parigi
    print(len(msg1))        # 5
    
    try:
        mg.add_message("bonjour", "Nizza", "Parigi")
        print("[Error]: missing sender station not identified") 
    except TelegraphException:
        print("Missing sender station correctly identified") # Missing sender station correctly identified

    try:
        mg.add_message("bonjour", "Parigi", "Nizza")
        print("[Error]: missing receiver station not identified")
    except TelegraphException:
        print("Missing receiver station correctly identified") # Missing receiver station correctly identified        

    print("------------------------- R2 -------------------------")
    mg.add_message("baguette", "Avignone", "Parigi")                
    mg.add_message("bon soiree", "Parigi", "Avignone")              
    mg.add_message("vive la france", "Marsiglia", "Avignone")
    mg.add_message("bonjour", "Marsiglia", "Lione")

    print(mg.get_destinations_by_frequency())   # {0: ['Marsiglia', 'Nantes'], 2: ['Avignone', 'Parigi'], 1: ['Lione']}
                                                # (ordine nomi nelle liste città è importante)

    print(mg.get_most_frequent_exchange())      # ('Avignone', 'Parigi')
                                                # (ordine nomi non è importante)

    print("------------------------- R3 -------------------------")
    print(mg.add_character_encoding('o', Symbol.DOT, previous=None))    # .
    print(mg.add_character_encoding('m', Symbol.DASH, previous=None))   # -
    print(mg.add_character_encoding('e', Symbol.DOT, previous="o"))     # ..
    print(mg.add_character_encoding('l', Symbol.DASH, previous="m"))    # --
    print(mg.add_character_encoding('t', Symbol.DASH, previous="o"))    # .-    
    print(mg.add_character_encoding('d', Symbol.DOT, previous="m"))     # -.

    print(mg.add_character_encoding('u', Symbol.DOT, previous="e"))     # ...
    print(mg.add_character_encoding('f', Symbol.DASH, previous="e"))    # ..-
    print(mg.add_character_encoding('r', Symbol.DOT, previous="l"))     # --.
    print(mg.add_character_encoding('a', Symbol.DASH, previous="l"))    # ---
    print(mg.add_character_encoding('g', Symbol.DOT, previous="t"))     # .-.

    enc = mg.encode_text("omelette du fromage")
    print(enc) # ['. - .. -- .. .- .- ..', '-. ...', '..- --. . - --- .-. ..']
    if enc ==  ['. - .. -- .. .- .- ..', '-. ...', '..- --. . - --- .-. ..']: 
        print("Correct encoding") # Correct encoding

    print("------------------------- R4 -------------------------")
    mg.add_connection("Parigi", "Marsiglia")
    mg.add_connection("Parigi", "Nantes")
    mg.add_connection("Marsiglia", "Nantes")
    mg.add_connection("Nantes", "Lione")

    print(mg.are_connected("Marsiglia", "Parigi"))  # True
    print(mg.are_connected("Lione", "Marsiglia"))   # False

    print(mg.get_connected_stations("Nantes"))      # {'Parigi', 'Lione', 'Marsiglia'}
    
    print("------------------------- R5 -------------------------")
    print(mg.get_shortest_path("Marsiglia", "Lione"))  # ['Marsiglia', 'Nantes', 'Lione']
    print(mg.get_shortest_path("Parigi", "Lione"))     # ['Parigi', 'Nantes', 'Lione']


if __name__ == "__main__":
    main()