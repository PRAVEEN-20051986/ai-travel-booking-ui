import streamlit as st
import requests
import urllib.parse
import random

st.set_page_config(page_title="AI Travel Booking", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
body { background:#f5f7fb; }
.card {
 background:white;
 border-radius:14px;
 padding:12px;
 box-shadow:0 4px 14px rgba(0,0,0,0.08);
 margin-bottom:20px;
}
.card img {
 width:100%;
 height:180px;
 object-fit:cover;
 border-radius:12px;
}
.price { color:#2b7cff; font-weight:bold; }
.btn {
 background:#2b7cff;
 color:white;
 padding:6px 12px;
 border-radius:6px;
 display:inline-block;
 margin-top:8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def osm_details(q):
    url="https://nominatim.openstreetmap.org/search"
    p={"q":q,"format":"json","extratags":1,"limit":1}
    h={"User-Agent":"AI-Travel"}
    r=requests.get(url,params=p,headers=h).json()
    if not r: return None
    e=r[0].get("extratags") if isinstance(r[0].get("extratags"),dict) else {}
    return {
        "phone":e.get("phone","Not available"),
        "website":e.get("website","Not available"),
        "map":f"https://www.openstreetmap.org/{r[0]['osm_type']}/{r[0]['osm_id']}"
    }

def wiki_image_desc(name):
    url="https://en.wikipedia.org/api/rest_v1/page/summary/"+name.replace(" ","%20")
    r=requests.get(url)
    img="https://via.placeholder.com/600x350?text=Hotel"
    desc="Comfortable stay with modern amenities."
    if r.status_code==200:
        j=r.json()
        img=j.get("thumbnail",{}).get("source",img)
        desc=j.get("extract",desc)
    return img,desc

def ai_price_rating():
    rating=round(random.uniform(3.6,4.8),1)
    one=random.randint(1800,4500)
    return rating,one,one*2

# ---------------- HEADER ----------------
st.markdown("## 🏨 Choose your destination")

c1,c2,c3,c4,c5=st.columns([2,1,1,1,1])
with c1: hotel=st.text_input("Hotel / Location")
with c2: st.date_input("Check-in")
with c3: st.date_input("Check-out")
with c4: st.selectbox("Guests",["1 Adult","2 Adults","3 Adults"])
with c5: search=st.button("Search")

tabs=st.tabs(["🏨 Room Stays","🗺️ Route","🚗 Car Rentals","🏍️ Bike Rentals"])

# ---------------- ROOM STAYS ----------------
with tabs[0]:
    if search and hotel:
        osm=osm_details(hotel)
        img,desc=wiki_image_desc(hotel)
        rating,one,two=ai_price_rating()

        if osm:
            st.markdown(f"""
            <div class="card">
            <img src="{img}">
            <h3>{hotel}</h3>
            ⭐ {rating} / 5<br>
            <span class="price">₹{one} / night</span><br>
            <span class="price">₹{two} / 2 nights</span>
            <p>{desc[:300]}...</p>
            📞 {osm['phone']}<br>
            🌐 {osm['website']}<br>
            <a href="{osm['map']}" target="_blank">📍 View Location</a><br>
            <div class="btn">View more</div>
            </div>
            """, unsafe_allow_html=True)

# ---------------- ROUTE ----------------
with tabs[1]:
    start=st.text_input("Start location")
    if start and hotel:
        s=urllib.parse.quote(start)
        d=urllib.parse.quote(hotel)
        url=f"https://www.google.com/maps/dir/?api=1&origin={s}&destination={d}&travelmode=driving"
        st.markdown(f"[Open Google Maps Route]({url})")

# ---------------- CAR & BIKE ----------------
with tabs[2]:
    st.write("Nearby car rentals will be listed here")

with tabs[3]:
    st.write("Nearby bike rentals will be listed here")
