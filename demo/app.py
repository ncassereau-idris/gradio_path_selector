
import gradio as gr
from gradio_fileexplorer import FileExplorer

from pathlib import Path


with gr.Blocks() as demo:
    component = FileExplorer()
    # component.change(component.refresh_value, component, component)
    # component.subscribe()
    # component.submit(get_listdir, component, component)
    # component.submit(test)
    button = gr.Button("Refresh")
    # button.click(component.refresh_value, component, component)
    
    comp = gr.TextArea("ceci est un test")
    comp2 = gr.Textbox("aze")
    comp.change(lambda x: x * 2, comp, comp2)


if __name__ == "__main__":
    demo.launch()

