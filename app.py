import streamlit as st
import pandas as pd
import pickle

st.title("Gelecek Ay Satış Tahmini (Kasım 2015) :  🛒:")
st.write("Mağaza ve ürün seçin; model o ürünün o mağazada 2015 Kasım ayında kaç adet satılacağını tahmin etsin.")

model=pickle.load(open('satis_modeli.pkl','rb'))
ozellik=pickle.load(open('kasim_ozellik.pkl','rb'))
isimler=pickle.load(open('isimler.pkl','rb'))

magaza_idler=sorted(ozellik.index.get_level_values('shop_id').unique())
magaza=st.selectbox('Mağaza',magaza_idler,format_func=lambda i: f"{i} - {isimler['magaza'].get(i,'')}")
urun_idler=sorted(ozellik.xs(magaza,level='shop_id').index)
urun=st.selectbox('Ürün',urun_idler,format_func=lambda i: f"{i} - {isimler['urun'].get(i,'')}")

if st.button('Tahmin et'):
    satir=ozellik.loc[(magaza,urun)]
    x=pd.DataFrame([[magaza,urun]+satir[isimler['ozellikler'][2:]].tolist()],columns=isimler['ozellikler'])
    tahmin=float(model.predict(x)[0])
    tahmin=min(max(tahmin,0),20)
    st.success(f'Tahmini satış adedi (Kasım 2015): {tahmin:.2f}')
    st.write('Geçmiş satışlar:')
    st.write(pd.DataFrame({'Ekim 2015 (lag1)':[satir['lag1']],'Eylül 2015 (lag2)':[satir['lag2']],'Ağustos 2015 (lag3)':[satir['lag3']],'Kasım 2014 (lag12)':[satir['lag12']]}))