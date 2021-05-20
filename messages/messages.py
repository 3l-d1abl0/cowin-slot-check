'''
formatting messages
'''

def prepare_center_name(center_idx, center):

    #prepare center banner
    center_name = '''\
Vaccination Center for 18-44 Group:
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
{date}
{vaccine}
Slots: {available_capacity}
Dose 1: {dose1} Dose 2: {dose2}
\n\
'''.format(date=session["date"], available_capacity=session["available_capacity"], vaccine=session["vaccine"], min_age=session["min_age_limit"], dose1=session["available_capacity_dose1"], dose2=session["available_capacity_dose2"])

    return session_name

def prepare_center_price(vaccine, fee):

    #prepare vaccination  price
    text_body = '''\
{vaccine} : ₹{price}
\
'''.format(vaccine=vaccine, price=fee)

    return text_body

def add_cowin_link():
    return '''\
<a href='https://selfregistration.cowin.gov.in'>CoWin</a> \
'''