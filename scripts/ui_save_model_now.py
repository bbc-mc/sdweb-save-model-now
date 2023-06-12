# Save Model Now
#
# extension of AUTOMATIC1111 web ui
#
# 2023/06/13 bbc_mc
#

import os
import gradio as gr
import torch
import safetensors.torch

from modules import sd_models
from modules import script_callbacks


DEBUG = False


def dprint(mes, flg=False):
    if DEBUG or flg:
        print(mes)


def save_model(theta_0, output_filename):
    if output_filename is not None and output_filename != "":
        output_filepath = os.path.join(sd_models.model_path, output_filename)
        if not os.path.exists(output_filepath):
            dprint("Saving...")
            _, extension = os.path.splitext(output_filepath)
            if extension.lower() == ".safetensors":
                dprint("  save as safetensors ...")
                safetensors.torch.save_file(theta_0, output_filepath, metadata={"format": "pt"})
            else:
                dprint("  save as ckpt ...")
                if extension != ".ckpt":
                    output_filepath = output_filepath + ".ckpt"
                if "state_dict" not in theta_0:
                    theta_0 = {"state_dict": theta_0}
                torch.save(theta_0, output_filepath)
            _ret = f"\rSaved. {output_filepath}"
            dprint(_ret)
            return _ret
        else:
            dprint("Same name model file already exists. abort.")
            return "already exits"


def on_ui_tabs():

    with gr.Blocks() as main_block:
        with gr.Column():
            with gr.Row():
                txt_model_name = gr.Text(label="ModelName", placeholder="new model name")
            with gr.Row():
                chk_debug = gr.Checkbox(label="debug print")
            with gr.Row():
                btn_save_now = gr.Button("Save Now!", variant="primary")
            with gr.Row():
                html_result = gr.HTML()

        #
        # Events
        #
        def on_btn_save_now(model_name):
            l_model = sd_models.model_data.get_sd_model()
            try:
                dprint(type(l_model))  # ldm.models.diffusion.ddpm.LatentDiffusion
                dprint(type(l_model.cond_stage_model))  # modules.sd_hijack_clip.FrozenCLIPEmbedderWithCustomWords
                dprint(type(l_model.cond_stage_model.wrapped))
                dprint(type(l_model.first_stage_model))  # ldm.models.autoencoder.AutoencoderKL
                dprint(type(l_model.state_dict()))  # collections.OrderedDict
                for key in l_model.state_dict().keys():
                    dprint(key)

                model_name = model_name if ".safetensors" in model_name else model_name + ".safetensors"
                ret = save_model(l_model.state_dict(), model_name)
                dprint(ret)
            except Exception as e:
                print(e)
            return gr.update()
        btn_save_now.click(
            fn=on_btn_save_now,
            inputs=[txt_model_name],
            outputs=[html_result]
        )

    # return required as (gradio_component, title, elem_id)
    return (main_block, "Save Model Now", "save_model_now"),

# on_UI
script_callbacks.on_ui_tabs(on_ui_tabs)
