# This is a sample Python script.
from fastapi import FastAPI,BackgroundTasks
from pydantic import BaseModel,validator
import tasks

app=FastAPI()

languages=["English","French","German","Romanian"]


class Translation(BaseModel):
    text: str
    base_lang:str
    final_lang:str
    @validator('base_lang','final_lang')
    def valid_lang(cls,lang):
        if lang not in languages:
            raise ValueError("Invalid Language")
        return lang
#route1:
#testing if everything is working
@app.get("/")
def get_root():
    return {"message": "Hello world"}

@app.post("/translate")
def post_translation(t: Translation, background_tasks: BackgroundTasks):
    t_id = tasks.store_translation(t)
    background_tasks.add_task(tasks.run_translation, t_id)
    return {"task_id": t_id}


@app.get("/results")
def get_translation(t_id: int):
    return {"translation": tasks.find_translation(t_id)}

@app.get("/history")
def get_translation_history():
    return {"history": tasks.get_translation_history()}

#route 2:/translate
##take in a translation request and store in database
## return a translation id
## route 3:/results
## take translational id
## return the translated text
