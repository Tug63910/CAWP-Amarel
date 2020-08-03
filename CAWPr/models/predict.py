import random

def classifier(text):
	level=['federal','state','local']
	office=['governor','attorney general','senator','representative','judge','mayor','councilman','other federal','other state','other local']
	profession=['doctor','lawyer','teacher','military','activist','academia','business','retired','entertainment','journalism','other']
	state=['AL','AK','AZ','AR','CA','CO','CT','DC','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
	predict={}
	predict['text']=text
	predict['state']=state[random.randint(0,len(state)-1)]
	predict['level']=level[random.randint(0,len(level)-1)]
	predict['office']=office[random.randint(0,len(office)-1)]
	predict['profession']=profession[random.randint(0,len(profession)-1)]
	return predict
