from mtg_search import db


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    multiverse_id = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer)
    power = db.Column(db.Text)
    toughness = db.Column(db.Text)

    artist_id = db.Column(db.Integer, db.ForeignKey('cardartists.id'))
    cost_id = db.Column(db.Integer, db.ForeignKey('cardcosts.id'))
    flavor_text_id = db.Column(db.Integer, db.ForeignKey('cardflavortexts.id'))
    name_id = db.Column(db.Integer, db.ForeignKey('cardnames.id'))
    oracle_rules_id = db.Column(db.Integer, db.ForeignKey('cardoraclerules.id'))
    printed_name_id = db.Column(db.Integer, db.ForeignKey('cardprintednames.id'))
    printed_rules_id = db.Column(db.Integer, db.ForeignKey('cardprintedrules.id'))
    printed_type_id = db.Column(db.Integer, db.ForeignKey('cardprintedtypes.id'))
    rarity_id = db.Column(db.Integer, db.ForeignKey('cardrarities.id'))
    set_id = db.Column(db.Integer, db.ForeignKey('cardsets.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('cardtypes.id'))
    watermark_id = db.Column(db.Integer, db.ForeignKey('cardwatermarks.id'))


class CardArtist(db.Model):
    __tablename__ = 'cardartists'
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.Text, nullable=False)
    cards = db.relationship("Card", backref='artist')


class CardCost(db.Model):
    __tablename__ = 'cardcosts'
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Text, nullable=False)
    cards = db.relationship("Card", backref='cost')


class CardFlavorText(db.Model):
    __tablename__ = 'cardflavortexts'
    id = db.Column(db.Integer, primary_key=True)
    flavor_text = db.Column(db.Text, nullable=False)
    cards = db.relationship("Card", backref='flavor_text')


class CardName(db.Model):
    __tablename__ = 'cardnames'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    cards = db.relationship("Card", backref='name')


class CardOracleRules(db.Model):
    __tablename__ = 'cardoraclerules'
    id = db.Column(db.Integer, primary_key=True)
    oracle_rules = db.Column(db.Text, nullable=False)
    cards = db.relationship("Card", backref='oracle_rules')


class CardPrintedName(db.Model):
    __tablename__ = 'cardprintednames'
    id = db.Column(db.Integer, primary_key=True)
    printed_name = db.Column(db.Text, nullable=False)
    cards = db.relationship("Card", backref='printed_name')


class CardPrintedRules(db.Model):
    __tablename__ = 'cardprintedrules'
    id = db.Column(db.Integer, primary_key=True)
    printed_rules = db.Column(db.Text, nullable=False)
    cards = db.relationship("Card", backref='printed_rules')


class CardPrintedType(db.Model):
    __tablename__ = 'cardprintedtypes'
    id = db.Column(db.Integer, primary_key=True)
    printed_type = db.Column(db.Text, nullable=False)
    cards = db.relationship("Card", backref='printed_type')


class CardRarity(db.Model):
    __tablename__ = 'cardrarities'
    id = db.Column(db.Integer, primary_key=True)
    rarity = db.Column(db.Text, nullable=False)
    cards = db.relationship("Card", backref='rarity')


class CardSet(db.Model):
    __tablename__ = 'cardsets'
    id = db.Column(db.Integer, primary_key=True)
    set = db.Column(db.Text, nullable=False)
    cards = db.relationship("Card", backref='set')


class CardType(db.Model):
    __tablename__ = 'cardtypes'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text, nullable=False)
    cards = db.relationship("Card", backref='type')


class CardWatermark(db.Model):
    __tablename__ = 'cardwatermarks'
    id = db.Column(db.Integer, primary_key=True)
    watermark = db.Column(db.Text, nullable=False)
    cards = db.relationship("Card", backref='watermark')
