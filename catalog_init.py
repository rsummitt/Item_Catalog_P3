from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a few categories
football_cat = Category(name='Football')
baseball_cat = Category(name='Baseball')
soccer_cat = Category(name='Soccer')
boxing_cat = Category(name='Boxing')

# Football Items
helmet = Item(name='Helmet', description='Protects head', category=football_cat)
shoulder_pads = Item(name='Shoulder Pads', description='Protects shoulders', category=football_cat)
thigh_pads = Item(name='Thigh Pads', description='Protects thighs', category=football_cat)
# Baseball Items
batting_gloves = Item(name='Batting Gloves', description='Provides better grip', category=baseball_cat)
bat = Item(name='Bat', description='Hit the ball with this', category=baseball_cat)
baseball_pants = Item(name='Baseball Pants', description='Protects legs while sliding', category=baseball_cat)
# Soccer Items
shin_guards = Item(name='Shin Guards', description='Protects Shins', category=soccer_cat)
goalie_gloves = Item(name='Goalie Gloves', description='Protects Goalies hands while blocking', category=soccer_cat)
cleats = Item(name='Cleats', description='Cleats used for Soccer', category=soccer_cat)
# Boxing Items
hand_wraps = Item(name='Hand Wraps', description='Stabilizes wrist', category=boxing_cat)
sparring_gloves = Item(name='Sparring Gloves', description='Padded gloves for sparring', category=boxing_cat)
heavy_bag = Item(name='Heavy Bag', description='Bag used for training', category=boxing_cat)

if __name__ == '__main__':

    # Add categories
    session.add(football_cat)
    session.add(baseball_cat)
    session.add(soccer_cat)
    session.add(boxing_cat)
    session.commit()

    # Add Items
    session.add(helmet)
    session.add(shoulder_pads)
    session.add(thigh_pads)

    session.add(batting_gloves)
    session.add(bat)
    session.add(baseball_pants)

    session.add(shin_guards)
    session.add(goalie_gloves)
    session.add(cleats)

    session.add(hand_wraps)
    session.add(sparring_gloves)
    session.add(heavy_bag)

    session.commit()
