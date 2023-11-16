from fastapi import Body, Response
from fastapi.responses import JSONResponse
from datetime import datetime

from main import app, HTTP_RESPONSE_MESSAGE, HTTP_RESPONSE_CODE
from api.mail import send_mail

html_template = ''
row_template = ''
with open('templates/mail/index.html', 'r') as f:
    html_template = f.read()
with open('templates/mail/row.html', 'r') as f:
    row_template = f.read()

def paste_value_to_html_template(s:str, **kwargs):
    for arg in kwargs:
        s=s.replace('{'+arg+'}', str(kwargs[arg]))
    return s

@app.post('/api/mail')
def send_message_to_mail(
    fio=Body(embed=True),
    email=Body(embed=True),
    phone=Body(embed=True),
    order=Body(embed=True),
    delivery_address=Body(embed=True),
    order_price=Body(embed=True)
      ):
    table = ''
    try:
        for key in order:
            thing = order.get(key, {})
            p = paste_value_to_html_template(
                row_template, name=thing.get('name'),
                article=thing.get('article'),
                count=thing.get('count'),
                price=thing.get('price'),
                img_path=thing.get('img_path'),
                href=thing.get('href')
            )
            table += p
        html=paste_value_to_html_template(
            html_template, table=table,
            fio=fio, 
            mail=email, 
            number=phone, 
            total_price=order_price,
            delivery_address=delivery_address,
            date=datetime.now().date().strftime('%d.%m.%Y')
          )
        send_mail(html=html)
        return JSONResponse({
            'msg': HTTP_RESPONSE_MESSAGE.SUCCESSFUL_SENT}, 
            status_code=HTTP_RESPONSE_CODE.SUCCESSFUL_SENT
        )
    except:
        return JSONResponse({
            'err': HTTP_RESPONSE_MESSAGE.INCORRECT_DATA
          }, status_code=HTTP_RESPONSE_CODE.INCORRECT_DATA)
