'''
formatting messages
'''

def prepare_center_name(center_idx, center):

    #prepare center banner
    center_name = '''\
Vaccination Center for 18-44Group:
{count}) {center_name} - {block_name}
{district_name}
{state_name}-{pincode}
Timing :{time_from} - {to}
Free/Paid : {fee_type}
--------------------------------
\
'''.format(count=center_idx,center_name=center["name"], block_name=center["block_name"],district_name=center["district_name"], state_name=center["state_name"], pincode=center["pincode"],time_from=center['from'], to=center['to'], fee_type=center["fee_type"])

    return center_name

def prepare_center_sessions(session):

    #prepare session data
    session_name ='''\
Date: {date}
Slots: {available_capacity}
Vaccine: {vaccine}
Min. Age: {min_age}
\n\
'''.format(date=session["date"], available_capacity=session["available_capacity"], vaccine=session["vaccine"], min_age=session["min_age_limit"])

    return session_name

def prepare_center_price(vaccine, fee):

    #prepare vaccination  price
    text_body = '''\
Vaccines Avail:
{vaccine} : ₹{price}
\
'''.format(vaccine=vaccine, price=fee)

    return text_body