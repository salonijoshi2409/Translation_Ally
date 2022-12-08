# import required modules
from os import path
from tkinter.font import names
from pydub import AudioSegment
import speech_recognition as sr
# assign files
import subprocess
import googletrans
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
import nltk
from googletrans import Translator
from gtts import gTTS
import os
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes



x="temp"
def audiopath(request):
    global x
    lang =googletrans.LANGUAGES
    if request.method == 'POST':
        myfile = request.FILES['myfile'] 
        src1 = request.POST['src']   
        dest1 = request.POST['dest']
        out=request.POST['output']
        print(out)
        fs= FileSystemStorage()

        names=myfile.name.split('.')
        upfile=fs.save('files/'+myfile.name, myfile)

        subprocess.call(['ffmpeg', '-i', 'media/files/'+myfile.name,
                   'media/files/'+names[0]+'.wav'])


        engine=sr.Recognizer()
        with sr.AudioFile('media/files/'+names[0]+'.wav') as source:
            print("Analysing.....")
            audio=engine.record(source)

        
        text=engine.recognize_google(audio, language=src1)
        #print(text)
        #print(f'Text:{text}')
       
        translator=Translator()
        with open('media/files/'+names[0]+'_translated.txt','w',encoding="utf-8") as op: 
                        translation = translator.translate(text, src=src1, dest=dest1).text
                        print(translation)
                        op.write(translation+' ')
                    #print(line+'\n')
        x=names[0]+"_translated.txt"
        
        if out=='audio':
            file = open('media/files/'+names[0]+'_translated.txt', encoding="utf-8").read()
            myobj=gTTS(text=file,lang=dest1,slow=False)
            
            myobj.save("media/files/"+names[0]+"_translated.mp3")
            x=names[0]+"_translated.mp3"
   
    return render(request,'try.html',{'lang':lang})
def downloadaudio(request):
    global x
    print("Hello")
    if x=="temp":
        messages.add_message(request, messages.INFO, 'File not uploaded. Please upload the file')
        return HttpResponseRedirect('/')
    else:
        #print(x,"helloo")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = base_dir + '/media/files/' + x
        thefile = filepath
        filename = os.path.basename(thefile)
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(open(thefile,'rb'),chunk_size),content_type=mimetypes.guess_type(thefile)[0])
        response['Content-Length'] = os.path.getsize(thefile)
        response['Content-Disposition'] = "Attachment;filename=%s" % filename
        return response

    return render(request, 'try.html')