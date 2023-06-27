import streamlit as st
from utils import *
import streamlit.components.v1 as components
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import pyttsx3
from mail import send_sms
from geopy.geocoders import Nominatim
locator = Nominatim(user_agent="myGeocoder")
r = sr.Recognizer()
def STT():
    try:
        with sr.AudioFile("audio.wav") as source2:
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
 
            return MyText
             
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        print("unknown error occurred")
        
        

def main():
    st.header('Life')
    #condition = st.text_input('Enter Your Status')
    audio_bytes = audio_recorder()
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        wav_file = open("audio.wav", "wb")
        wav_file.write(audio_bytes)
        type_res = STT()
        st.write(type_res)
        
        
    if st.button('Find hospitals'):
        my_lat, my_long = get_my_loc()
        location = locator.reverse((my_lat, my_long))
        address = location.address
        nearest_hospitals = get_nearest(my_lat, my_long)
        
        names, address, location, distance = get_names(nearest_hospitals)
        
        choice = st.selectbox('Select Hospital', options=names, index=0)
        if choice:
            indx = names.index(choice)
            route = get_route(my_lat, my_long, *location[indx])
            
            m = create_map(route)
            
            m.save('map.html')
            
            HtmlFile = open("map.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            components.html(source_code)
            st.warning(
                '''
                Name: {}
                Address: {}
                Distance: {} Km
                '''.format(names[indx], address[indx], distance[indx]/1000)
            )
            try:
                msg = '''
                Location: {}
                Type: {}
                Address: {}
                '''.format((my_lat,my_long), type_res, address[0])
                send_sms(msg)
            except:
                print("SMS NOT SENT")
        
    
    
main()