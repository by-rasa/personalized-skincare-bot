## Setup
* Set `RASA_PRO_LICENSE` and `OPENAI_API_KEY` in `.env` file
* Install dependecies with `pip install -r requirements.txt`
* Terminal 1: Run the action server with `rasa run actions`
* Terminal 2: Train the assistant locally with `rasa train` and run the Rasa server with `rasa run`
* Terminal 3: Run the Gradio server with `python gradio_ui.py`
* Go to `http://0.0.0.0:7860/` and try your bot

## Possible Improvements
* History management, now it's blocking the UI
* Add streaming to improve the UX
* Add buttons for categorical values (e.g. skin_type)
