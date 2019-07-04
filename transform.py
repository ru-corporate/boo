"""Transform numbers"""
from columns import get_unit, COLUMNS_LONG, COLUMNS_SHORT_DATA

def which_positions(short=COLUMNS_SHORT_DATA, long=COLUMNS_LONG):
    return [i for (i, col) in enumerate(long) if col in short]

def change_data_fields(f, row, positions=which_positions()):
    return [(f(x) if i in positions else x) for i,x in enumerate(row)]

def rub_to_thousand(x: int):
    return str(round(0.001 * float(x)))

def mln_to_thousand(x: int):
    return str(1000 * int(x))

def adjust_rub(row):
    u  = get_unit(row)
    if u == '384':
        return row
    elif u =='383':
        return change_data_fields(rub_to_thousand, row)
    elif u == '385':
        return change_data_fields(mln_to_thousand, row)
    else:
        raise ValueError(f"Unit {u} not supported. Row:\n{row}")
        
# testing        

assert which_positions("bc", "abc") == [1, 2]

assert change_data_fields(lambda x: x+1, [0,0,0], [0,1]) == [1, 1, 0]

def mkrow(code='384'):
    txt = """Общество с ограниченной ответственностью "Донагрогаз";03619705;12165;16;01.11.1;3432013860;384;2;0;0;0;0;0;0;0;0;360231;158069;0;0;0;0;0;0;794379;233797;1154610;391866;286668;108601;2393;6133;97306;573101;16280;1300;477;85;1667;616;404791;689836;1559401;1081702;347000;347000;0;0;0;0;872;872;0;0;39714;29750;387586;377622;1044343;573648;0;0;0;0;41720;41720;1086063;615368;36935;26034;48706;62678;0;0;111;0;0;0;85752;88712;1559401;1081702;67386;48878;198204;47184;-130818;1694;0;0;0;0;-130818;1694;3;3;0;0;8437;3609;155093;7305;5185;4078;10656;1315;692;0;0;0;0;0;0;0;0;0;9964;1315;0;0;0;0;9964;1315;347000;0;872;0;29750;377622;0;0;0;0;9964;9964;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;347000;0;872;0;39714;387586;387586;377622;265755;94375;5502;0;165878;261445;201326;17398;7302;73;35346;4310;100;30;0;67;3;0;498980;393187;0;119;90674;15000;-498880;521262;516862;0;0;0;4400;26300;0;0;26300;0;494962;392;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;20130610"""
    row = txt.split(";")
    row[6] = code
    return row

assert adjust_rub(mkrow(code='384')) == mkrow(code='384')