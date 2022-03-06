import os
import discord
from dotenv import load_dotenv
import numpy as np
import sklearn
from sklearn import linear_model
import numpy as np
from sklearn.linear_model import LinearRegression
import random
from keep_alive import keep_alive
import pandas as pd
import json
import requests
import math
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
funfact=["Fact: Most of the increase in global temperatures since 1950 has been caused by human activity", "Fact: The average temperature of the Earth is determined by the greenhouse effect", "Fact: Global temperatures have increased by about 1° Celsius in the past century", "Fact: The United States is the second largest contributor to carbon dioxide (CO2) in our atmosphere","Fact: Arctic sea ice and glaciers are melting", "Fact: Average sea level is expected to rise between 0.5 and 1.5 metres before the end of the century","Fact: Rainforest destruction is a major cause of carbon dioxide release","Fact: Coral reefs are being destroyed", "Fact 10: As global temperatures increase, our societies will find it harder to adapt to the changes this brings, and some species are more likely to go extinct", "Fact: kyle>rahul"]
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

trivia=False
city_name = ""

#prediction function
def globalwarmpredicter(values):
  #reading the data in (we had to limit the data in order for the line to more accurate)
  #https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt
  #https://climate.nasa.gov/vital-signs/global-temperature/
  fname="datasample.txt"
  file=open(fname,"r")
  Lines=file.readlines()
  file.close()
  x=[]
  y=[]
  for i in range(len(Lines)):
      line=[float(j) for j in Lines[i].split()]
      x.append(line[0])
      y.append(line[2])
  x=np.array(x).reshape(-1,1)
  y=np.array(y)
  x2 = PolynomialFeatures(degree=2, include_bias=False).fit_transform(x)
  model = LinearRegression().fit(x2, y)
  values=np.array(values).reshape(-1,1)
  numbers=x2 = PolynomialFeatures(degree=2, include_bias=False).fit_transform(values)
  val=model.predict(numbers)
  stringout=""
  for i in val:
      stringout+=str(i)+" "
  return stringout





# i must leave sorry ill be back
def checkweather2(location,full_city_name):
  URL="https://api.openweathermap.org/data/2.5/weather?q="+location+"&APPID=837c48c536f45a99223c6d061c033031"
  page = requests.get(URL)
  try:
    page = requests.get(URL)
  except:
    exit()
  arr=np.array(page.text.split(","))
  file=open("filewebsite.txt","w")
  file.write(page.text)
  file.close()
  f=open("filewebsite.txt","r")
  Lines=f.readlines()
  f.close()
  description=Lines[0]
  d=json.loads(description)
  des = d["weather"][0]["description"].title()
  temperature = round(1.8 * float(d["main"]["temp"]-273.1) + 32)
  feels_like= round(1.8 * float(d["main"]["feels_like"]-273.1) + 32)
  temp_min = math.floor(1.8 * float(d["main"]["temp_min"]-273.1) + 32)
  temp_max = math.ceil(1.8 * float(d["main"]["temp_max"]-273.1) + 32)
  humidity = int(d["main"]["humidity"])
  visibility = int(d["visibility"]) / 1000
  wind_speed = float(d["wind"]["speed"])
  city_name = d["name"]
  degree_sign = u'\N{DEGREE SIGN}'
  return f"""
  {city_name}
  {des}
  The temperature is about {temperature}{degree_sign} Fahrenheit right now
  It feels like {feels_like}{degree_sign} Fahrenheit
  The minimum temperature today is {temp_min}{degree_sign} Fahrenheit
  The maximum temperature today is {temp_max}{degree_sign} Fahrenheit
  The precentage of humidity is {humidity}%
  The visibility is {visibility} kilometers
  The wind speed is {wind_speed} meters per second
  """

  


"""def checkweather(location, full_city_name):
  import requests
  import numpy as np
  import time
  URL="https://api.openweathermap.org/data/2.5/weather?q="+location+"&APPID=837c48c536f45a99223c6d061c033031"
  print(URL)
  page = requests.get(URL)
  try:
    page = requests.get(URL)
  except:
    exit()
  file=open("filewebsite.json","w")
  #file.write(page.text)
  with open('filewebsite.json') as json_file:
    dic = json.load(json_file)
  description = str(dic["weather"]["description"])
  des=""
  for i in description:
    if(i=='"'):
      continue
    des = des + i
  des = des.title()
  # in fahrenheit
  temperature = float(dic["main"]["temp"])
  temperature = 1.8*(temperature - 273.15) + 32
  temperature = round(temperature)
  # in fahrenheit
  feels_like = float(dic["main"]["feels_like"])
  feels_like = 1.8*(feels_like - 273.15) + 32
  feels_like = round(feels_like)
  # in percentage
  humidity = dic["main"]["humidity"]
  humidity = int(humidity[:-1])
  # in km
  visibility = int(dic["visibility"])
  visibility = visibility / 1000
  # In meters per second
  wind_speed = float(dic["wind"]["speed"])
  file.write(page.text)
  file.close()
  return f
  ```
  {full_city_name}
  {des}
  The temperature is about {temperature} Fahrenheit
  It feels like {feels_like} Fahrenheit
  The precentage of humidity is {humidity}%
  The visibility is {visibility} kilometers
  The wind speed is {wind_speed} meters per second```
  ```
  """



@client.event
async def on_ready():
    print(f'{client.user}has connected')
@client.event
async def on_message(message):
  global trivia
  if (message.author == client.user):
        return

  elif(message.content.split()[0]=='!predict'):
    try:
      inputval=message.content.split()[1:]
      inputval=[float(i) for i in inputval]
      await message.channel.send('predicting...')
      embedVar = discord.Embed(title="Prediction", description="Global Warming Prediction", color=0x00ff00)
      output=globalwarmpredicter(inputval).split()
      for i in range(len(inputval)):
        embedVar.add_field(name="Year: "+str(int(inputval[i])), value="Temperature rise: "+str(output[i])+" degrees celcius", inline=False)
      embedVar.add_field(name="Sources for Data(prediction done by bot but there is a need for temperature rise over the past years in order to predict)",value="""
https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt

https://climate.nasa.gov/vital-signs/global-temperature/"""
      ,inline=False)
      await message.channel.send(embed=embedVar)
    except:
      await message.channel.send("Please enter a year or years separated by space after typing !predict")
      


  elif(message.content=="!funfact"):
    random1=random.randrange(0,9)
    embedVar = discord.Embed(title="Fun Fact", description=str(funfact[random1]), color=0x00ff00)
    await message.channel.send(embed=embedVar)




  elif(message.content=="!help"):
    embedVar = discord.Embed(title="Commands", description="https://requiredinfinitewordprocessor.saaraskodali.repl.co", color=0x00ff00)
    await message.channel.send(embed=embedVar)


  elif(message.content=="!creators"):
    await message.channel.send("Advik Garg, William Cheng(Chilliam Weng), Tarun Jaikumar,Saaras Kodali")
    
  
  

  elif(message.content.split()[0]=="!weather"):
   try:
    location_lst=message.content.split()[1:]
    city_name = " ".join(location_lst).title()
    location_input = "+".join(location_lst)
    embedVar=discord.Embed(title="Weather",description=checkweather2(location_input, city_name),color=0x00ff00)
    embedVar.add_field(name="Source",value="https://api.openweathermap.org/data/2.5/weather?q="+location_input+"&APPID=837c48c536f45a99223c6d061c033031",inline=False)
    await message.channel.send(embed=embedVar)
   except:
     await message.channel.send("Please enter an actual city")


  elif(message.content.split()[0]=="!trivia"):
    questions = ["The condition of the atmosphere in a certain place at a certain time is known as (A: Solubility, B: Weather, C: Water Cycle, D: Matter)", "The general weather of an area over a long period of time is known as the (A: Climate, B: Community, C: Barometer, D: Cold Front)", "The air that surrounds the earth is the (A: Biome, B: Weather, C: Radar Map, D: Atmosphere)", "A ____________ is an instrument that measures rainfall (A: Hygrometer, B: Anenometer, C: Rain Guage, D: Spoon)", "A ________ is a place where one air mass meets and pushes aside another air mass. This often results as a change in the weather (A: Front, B: Satellite, C: Hurricane, D: Cloud)", "_____ is moving air (A: Percipitation, B: Wind, C: Condensation, D: Tempature)", "Air Pressure is the weight of air pushing on everything around it. (A: True, B: False)"
    ]
    answers = ["B", "A", "D", "C", "A", "B", "A"]   
    trivia = True
    dice=random.randrange(0, len(questions))
    await message.channel.send("Question: "+questions[dice] + "\n"+"Format: (!answer;letter)")
    author=str(message.author)
    filename=author[len(author)-4:]+".txt"
    filename=filename[:8]
    try:
      reader=open(filename,'r')
      Lines=reader.readlines()
      reader.close()
      points=int(Lines[1])
    except:
      points=0
    file=open(filename,"w")
    file.write(str(dice)+"\n")
    file.write(str(questions[dice])+"\n")
    file.write(str(answers[dice])+"\n")
    file.write(str(points))
    file.close()


  elif(message.content.split(";")[0]=="!answer"):
   try:
    ans=message.content.split(";")[1]
    auth=str(message.author)
    openname=auth[len(auth)-4:]+".txt"
    f=open(openname,"r")
    Lines=f.readlines()
    f.close()
    points=Lines[len(Lines)-1]
    if(Lines[2][0].upper()==ans.upper()):
      await message.channel.send("Correct!")
      points=int(points)
      points+=1
      points=str(points)
      file=open(openname,"w")
      file.write(str(points))
      [file.write(i) for i in Lines]
      file.close()
    else:
      await message.channel.send("Incorrect! The correct answer is "+ Lines[2])
    fwrite=open(openname,"w")
    fwrite.write("ANSWERED"+"\n")
    fwrite.write(str(points))
    fwrite.close()
   except:
     await message.channel.send("Do the Trivia command for more questions")
     
    
      
  elif(message.content=="!ovcc"):
    await message.channel.send("This was made by students of ovms in ovcc")
  elif(message.content=="!showpoints"):
   try:
    author=str(message.author)
    filename=author[len(author)-4:]+".txt"
    filename=filename[:8]
    freader=open(filename,"r")
    Lines=freader.readlines()
    freader.close()
    await message.channel.send(Lines[len(Lines)-1])
   except:
     await message.channel.send("Do the trivia command(!trivia)")
  elif(message.content=="!stopglobal"):
    await message.channel.send(file=discord.File('Infographic1.png'))
    await message.channel.send('The credit for this goes to Planet of Love Co.')
    
client.run('OTEyOTMyMjk0OTIxMTkxNDY1.YZ3IdA._reqNz5zShfmcuix2L5snJ7zhI8')
#https://discord.com/api/oauth2/authorize?client_id=912932294921191465&permissions=8&scope=bot
