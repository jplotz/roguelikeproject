# I think it makes a lot more sense to have a spreadsheet of things
# that is saved to a CSV file or something, and then have the code
# import the data from that human-readable file. That way, adding new content
# to the game can be as simple as editing a spreadsheet.


from entity import Entity

player = Entity(char="@", color=(255, 255, 255), name="Player", blocks_movement=True)

orc = Entity(char="o", color=(255, 255, 0), name="Orc", blocks_movement=True)
troll = Entity(char="T", color=(0, 255, 0), name="Troll", blocks_movement=True)
